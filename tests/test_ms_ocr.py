import pytest
from unittest.mock import patch, MagicMock, mock_open
from ocr_testing.src.ms_ocr import perform_ocr

# A mock response from the Azure OCR service
mock_azure_result = {
    'status': 'succeeded',
    'analyze_result': {
        'read_results': [
            {
                'lines': [
                    {
                        'text': 'Hello World',
                        'bounding_box': [10, 20, 100, 20, 100, 50, 10, 50],
                        'words': [{'confidence': 0.95}, {'confidence': 0.98}]
                    }
                ]
            }
        ]
    }
}

@pytest.fixture
def mock_cv_client():
    """Fixture to mock the ComputerVisionClient."""
    with patch('ocr_testing.src.ms_ocr.ComputerVisionClient') as mock_client:
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.headers = {"Operation-Location": "some/location/op_id"}

        # Mock the client instance and its methods
        instance = mock_client.return_value
        instance.read_in_stream.return_value = mock_response

        # Mock the result of get_read_result
        mock_result = MagicMock()
        mock_result.status = 'succeeded'
        mock_result.as_dict.return_value = mock_azure_result
        instance.get_read_result.return_value = mock_result

        yield mock_client

@pytest.fixture
def mock_env_vars():
    """Fixture to mock environment variables."""
    with patch.dict('os.environ', {'AZURE_ENDPOINT': 'dummy_endpoint', 'AZURE_KEY': 'dummy_key'}):
        yield

def test_perform_ocr_from_path_success(mock_cv_client, mock_env_vars):
    """Test successful OCR from a file path."""
    image_path = "dummy_path.png"

    with patch("builtins.open", mock_open(read_data=b"image_bytes")):
        result = perform_ocr(image_path)

    expected = [{
        'bounding_box': [[10, 20], [100, 20], [100, 50], [10, 50]],
        'text': 'Hello World',
        'confidence': 0.95
    }]

    assert result == expected

def test_perform_ocr_from_bytes_success(mock_cv_client, mock_env_vars):
    """Test successful OCR from image bytes."""
    image_bytes = b"some_image_bytes"

    result = perform_ocr(image_bytes)

    expected = [{
        'bounding_box': [[10, 20], [100, 20], [100, 50], [10, 50]],
        'text': 'Hello World',
        'confidence': 0.95
    }]

    assert result == expected

def test_perform_ocr_no_credentials():
    """Test OCR when Azure credentials are not set."""
    with patch.dict('os.environ', {}, clear=True):
        result = perform_ocr("dummy.png")

    assert result == []

def test_perform_ocr_file_not_found(mock_cv_client, mock_env_vars):
    """Test FileNotFoundError handling."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = perform_ocr("non_existent.png")

    assert result == []

def test_perform_ocr_general_exception(mock_cv_client, mock_env_vars):
    """Test handling of other exceptions."""
    mock_cv_client.return_value.read_in_stream.side_effect = Exception("Azure error")

    result = perform_ocr(b"image_bytes")

    assert result == []