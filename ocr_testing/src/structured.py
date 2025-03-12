
import pandas as pd
import json

def get_bbox_center(bbox):
    """Calculate the center point of a bounding box."""
    x_coords = [point[0] for point in bbox]
    y_coords = [point[1] for point in bbox]
    center_x = sum(x_coords) / 4
    center_y = sum(y_coords) / 4
    return center_x, center_y

def parse_ocr_json(ocr_data):
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
    # Initialize a dictionary to store key-value pairs for this form
    data = {key: "" for key in expected_keys}
    ocr_items = []

    
    # Store all OCR items with their centers
    for item in ocr_data:
        center_x, center_y = get_bbox_center(item["bounding_box"])
        ocr_items.append((item["text"], center_x, center_y, item["confidence"]))
    
    # Sort items by y-coordinate (top to bottom) and then x-coordinate (left to right)
    ocr_items.sort(key=lambda x: (x[2], x[1]))
    
    # Match keys and values based on proximity
    i = 0
    while i < len(ocr_items):
        text, center_x, center_y, confidence = ocr_items[i]
        text = text.strip()
        
        # Check if the text matches an expected key (ignoring ':' if present)
        key_matched = False
        for key in expected_keys:
            if text.startswith(key) or text.replace(":", "").strip() == key:
                key_matched = True
                # Look for the next text item as the value (assuming it's below or to the right)
                j = i + 1
                while j < len(ocr_items) and not ocr_items[j][0].strip().endswith(':'):
                    value_text, value_x, value_y, value_confidence = ocr_items[j]
                    # Check if the value is likely below or to the right of the key
                    if value_y > center_y or (abs(value_y - center_y) < 50 and value_x > center_x):
                        data[key] = value_text
                        i = j  # Move past the value
                        break
                    j += 1
                break
        
        # If no key is matched but it's a potential value, skip it (handled by default empty strings)
        i += 1
    df = pd.DataFrame([data])
    df = df.fillna('')
    df = df[expected_keys]
    try:
        # Try to read the existing CSV to check if it's empty
        existing_df = pd.read_csv("output.csv")
        append = True # if the file exists and is not empty, append.
    except FileNotFoundError:
        append = False # if the file doesn't exist, create it with header.
    except pd.errors.EmptyDataError:
        append = False # if the file exists, but is empty, create it with header.
        
    if append:
        df.to_csv("output.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("output.csv", index=False)
    return data
    

if __name__=="__main__":
    data_='[{"bounding_box":[[24,3],[167,3],[167,18],[24,18]],"text":"InvoiceNumber","confidence":0.9958509802818298},{"bounding_box":[[23,37],[209,37],[209,52],[23,52]],"text":"13166624120923118106","confidence":0.9952586889266968},{"bounding_box":[[22,81],[180,82],[180,100],[22,99]],"text":"Total Sales Value:","confidence":0.9517459869384766},{"bounding_box":[[21,117],[87,117],[87,136],[21,136]],"text":"1243.20","confidence":0.9989754557609558},{"bounding_box":[[21,161],[154,163],[153,185],[21,182]],"text":"Total Quantity:","confidence":0.987274706363678},{"bounding_box":[[20,198],[61,198],[61,218],[20,218]],"text":"3.00","confidence":0.9993022680282593},{"bounding_box":[[22,244],[191,244],[191,265],[22,265]],"text":"Total Tax Charged:","confidence":0.9750157594680786},{"bounding_box":[[22,280],[82,280],[82,299],[22,299]],"text":"223.60","confidence":0.9990066885948181},{"bounding_box":[[22,326],[106,326],[106,344],[22,344]],"text":"Discount:","confidence":0.991348147392273},{"bounding_box":[[21,361],[80,361],[80,380],[21,380]],"text":"274.20","confidence":0.9986280798912048},{"bounding_box":[[23,409],[176,409],[176,423],[23,423]],"text":"Total Bill Amount:","confidence":0.9183325171470642},{"bounding_box":[[21,443],[89,443],[89,462],[21,462]],"text":"1466.80","confidence":0.9996436834335327},{"bounding_box":[[22,490],[121,490],[121,507],[22,507]],"text":"Date Time:","confidence":0.9607427716255188},{"bounding_box":[[24,526],[264,526],[264,541],[24,541]],"text":"2024-12-09T22:00:00+05:00","confidence":0.9839659929275513},{"bounding_box":[[21,570],[64,570],[64,589],[21,589]],"text":"NTN:","confidence":0.9770442247390747},{"bounding_box":[[22,606],[115,606],[115,624],[22,624]],"text":"7565001-6","confidence":0.9947671890258789},{"bounding_box":[[23,652],[163,652],[163,669],[23,669]],"text":"Business Name:","confidence":0.9597359895706177},{"bounding_box":[[23,687],[278,687],[278,704],[23,704]],"text":"NOVA CARE PRIVATE)LIMITED","confidence":0.9637101888656616},{"bounding_box":[[23,732],[150,732],[150,750],[23,750]],"text":"Branch Name:","confidence":0.9449611306190491},{"bounding_box":[[24,770],[225,770],[225,784],[24,784]],"text":"037-DVAGOU-PMOOR","confidence":0.9487520456314087},{"bounding_box":[[22,813],[168,814],[168,832],[22,831]],"text":"Branch Address:","confidence":0.970155656337738},{"bounding_box":[[22,850],[488,851],[488,868],[22,867]],"text":"Sector l1C-3 Sector 11 C 1 North Karachi Twp,Karachi","confidence":0.9069525003433228},{"bounding_box":[[23,876],[191,876],[191,893],[23,893]],"text":"Karachi City,Sindh","confidence":0.9767905473709106},{"bounding_box":[[22,920],[141,920],[141,938],[22,938]],"text":"POS Counter:","confidence":0.9401414394378662},{"bounding_box":[[22,956],[77,956],[77,974],[22,974]],"text":"037-B","confidence":0.9890486598014832}]'
    data_=json.loads(data_)
    parse_ocr_json(data_)

