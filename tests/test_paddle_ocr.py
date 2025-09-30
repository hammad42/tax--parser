import pytest
from unittest.mock import patch, MagicMock
from ocr_testing.src.paddle_ocr import perform_paddle_ocr

# Sample data to be returned by the mocked PaddleOCR
mock_ocr_result = [
    [
        ([[10, 20], [100, 20], [100, 50], [10, 50]], ('Hello', 0.95)),
        ([[60, 70], [150, 70], [150, 100], [60, 100]], ('World', 0.92))
    ]
]

# This fixture will mock the PaddleOCR class
@pytest.fixture
def mock_paddle_ocr():
    with patch('ocr_testing.src.paddle_ocr.PaddleOCR') as mock:
        # Configure the mock to return a specific result when ocr() is called
        instance = mock.return_value
        instance.ocr.return_value = mock_ocr_result
        yield mock

def test_perform_paddle_ocr_success(mock_paddle_ocr):
    """
    Test successful OCR processing with mocked PaddleOCR.
    """
    image_path = "dummy_path.png"

    # Call the function to be tested
    result = perform_paddle_ocr(image_path)

    # Assert that the result is as expected
    expected_result = [
        {'bounding_box': [[10, 20], [100, 20], [100, 50], [10, 50]], 'text': 'Hello', 'confidence': 0.95},
        {'bounding_box': [[60, 70], [150, 70], [150, 100], [60, 100]], 'text': 'World', 'confidence': 0.92}
    ]

    assert result == expected_result

    # Verify that PaddleOCR was initialized and ocr was called correctly
    mock_paddle_ocr.assert_called_once_with(use_gpu=True, lang='en', show_log=False)
    mock_paddle_ocr.return_value.ocr.assert_called_once_with(image_path, cls=False)

def test_perform_paddle_ocr_file_not_found(mock_paddle_ocr):
    """
    Test the case where the image file is not found.
    """
    image_path = "non_existent_file.png"

    # Configure the mock to raise FileNotFoundError
    mock_paddle_ocr.return_value.ocr.side_effect = FileNotFoundError

    # Call the function and assert that it returns an empty list
    result = perform_paddle_ocr(image_path)

    assert result == []

def test_perform_paddle_ocr_other_exception(mock_paddle_ocr):
    """
    Test handling of other exceptions during OCR processing.
    """
    image_path = "dummy_path.png"

    # Configure the mock to raise a generic exception
    mock_paddle_ocr.return_value.ocr.side_effect = Exception("Some OCR error")

    # Call the function and assert that it returns an empty list
    result = perform_paddle_ocr(image_path)

    assert result == []