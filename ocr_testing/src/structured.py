import json
import pandas as pd
from pathlib import Path

# Directory containing your OCR JSON output files
ocr_output_directory = Path(r"E:\Projects\OCR\ocr_testing\extras\pandas.json")  # Replace with your folder path
output_excel = "invoices_data.xlsx"

# List to hold data from all forms
all_data = []

# Define expected keys (based on your OCR output)
expected_keys = [
    "Invoice Number",
    "Total Sales Value",
    "Total Quantity",
    "Total Tax Charged",
    "Discount",
    "Total Bill Amount",
    "Date Time",
    "NTN",
    "Business Name",
    "Branch Name",
    "Branch Address",
    "POS Counter"
]