import pytest
from unittest.mock import patch, MagicMock
from ocr_testing.src.ocr_selection import perform_ocr

@patch('ocr_testing.src.ocr_selection.ms_ocr.perform_ocr')
def test_perform_ocr_with_azure(mock_ms_ocr):
    """
    Test that the azure ocr tool is called when specified.
    """
    # Configure the mock to return a specific value
    mock_ms_ocr.return_value = "Azure OCR Result"

    # Call the function with 'azure' as the tool
    result = perform_ocr("dummy_image.png", "azure")

    # Assert that the mock was called and the result is correct
    mock_ms_ocr.assert_called_once_with("dummy_image.png")
    assert result == "Azure OCR Result"

@patch('ocr_testing.src.ocr_selection.p_ocr.perform_paddle_ocr')
def test_perform_ocr_with_paddle(mock_paddle_ocr):
    """
    Test that the paddle ocr tool is called when specified.
    """
    # Configure the mock to return a specific value
    mock_paddle_ocr.return_value = "Paddle OCR Result"

    # Call the function with 'paddle' as the tool
    result = perform_ocr("dummy_image.png", "paddle")

    # Assert that the mock was called and the result is correct
    mock_paddle_ocr.assert_called_once_with("dummy_image.png")
    assert result == "Paddle OCR Result"

def test_perform_ocr_with_invalid_tool():
    """
    Test that a ValueError is raised for an invalid ocr tool.
    """
    # Assert that a ValueError is raised for an invalid tool
    with pytest.raises(ValueError, match="Invalid OCR tool specified. Choose either 'azure' or 'paddle'."):
        perform_ocr("dummy_image.png", "invalid_tool")