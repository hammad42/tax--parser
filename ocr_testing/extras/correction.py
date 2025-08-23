import streamlit as st
import cv2
import json
import numpy as np

# Initialize session state
if 'ocr_data' not in st.session_state:
    # Your initial OCR data
    st.session_state.ocr_data = [{"bounding_box":[[21,12],[172,12],[172,29],[21,29]],"text":"Invoice Number:","confidence":0.975},{"bounding_box":[[21,47],[226,47],[226,65],[21,66]],"text":"17256224121322859780","confidence":0.978},{"bounding_box":[[23,94],[183,94],[183,112],[23,112]],"text":"Total Sales Value:","confidence":0.994},{"bounding_box":[[21,130],[87,131],[87,148],[21,148]],"text":"3333.91","confidence":0.995},{"bounding_box":[[23,176],[155,177],[155,198],[23,197]],"text":"Total Quantity:","confidence":0.994},{"bounding_box":[[23,214],[61,214],[62,231],[23,230]],"text":"9.00","confidence":0.993},{"bounding_box":[[21,259],[195,260],[194,280],[21,279]],"text":"Total Tax Charged:","confidence":0.994},{"bounding_box":[[23,296],[84,296],[84,313],[23,313]],"text":"600.09","confidence":0.994},{"bounding_box":[[22,342],[108,342],[108,360],[22,360]],"text":"Discount:","confidence":0.994},{"bounding_box":[[22,379],[61,379],[61,396],[22,395]],"text":"0.00","confidence":0.993},{"bounding_box":[[22,425],[181,425],[181,443],[22,442]],"text":"Total Bill Amount:","confidence":0.989},{"bounding_box":[[21,462],[95,462],[95,479],[22,479]],"text":"3935.62","confidence":0.997},{"bounding_box":[[22,508],[122,508],[122,526],[22,525]],"text":"Date Time:","confidence":0.993},{"bounding_box":[[22,544],[262,544],[262,562],[22,562]],"text":"2024-12-13T22:05:00+05:00","confidence":0.848},{"bounding_box":[[22,592],[61,590],[62,607],[22,607]],"text":"NTN:","confidence":0.989},{"bounding_box":[[23,627],[123,627],[123,645],[23,644]],"text":"8009003-2","confidence":0.991},{"bounding_box":[[22,674],[166,675],[166,691],[21,690]],"text":"Business Name:","confidence":0.994},{"bounding_box":[[22,710],[217,710],[217,727],[22,728]],"text":"C PLUS SUPER MARKET","confidence":0.991},{"bounding_box":[[22,757],[153,757],[153,774],[22,774]],"text":"Branch Name:","confidence":0.994},{"bounding_box":[[21,790],[308,790],[308,813],[21,813]],"text":"C PLUS SUPER MARKET (UP Morr)","confidence":0.989},{"bounding_box":[[21,838],[171,839],[171,858],[21,857]],"text":"Branch Address:","confidence":0.994},{"bounding_box":[[22,873],[405,873],[405,895],[22,895]],"text":"Plot A-01 (ST-09) sector 11-1 north karachi","confidence":0.928},{"bounding_box":[[22,921],[144,922],[143,940],[22,939]],"text":"POS Counter:","confidence":0.994},{"bounding_box":[[22,957],[84,957],[84,976],[21,975]],"text":"172562","confidence":0.994}]  # Paste your JSON data here

if 'original_image' not in st.session_state:
    st.session_state.original_image = cv2.imread(r"E:\Projects\samples\color_images\Screenshot_20250211-234427_1.png")

def draw_boxes_on_image(image, json_data):
    # Convert image to RGB for Streamlit display
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_copy = image.copy()
    
    for idx, item in enumerate(json_data):
        bbox = item["bounding_box"]
        text = str(item["text"]) + f' (C: {item["confidence"]:.2f})'
        
        xs = [pt[0] for pt in bbox]
        ys = [pt[1] for pt in bbox]
        top_left = (int(min(xs)), int(min(ys)))
        bottom_right = (int(max(xs)), int(max(ys)))
        
        # Draw rectangle
        cv2.rectangle(image_copy, top_left, bottom_right, (0, 255, 0), 2)
        
        # Draw text
        cv2.putText(image_copy, text, (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    return image_copy

def main():
    st.title("OCR Correction Interface")
    
    # Create two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Image with OCR Results")
        # Draw boxes on the original image
        annotated_image = draw_boxes_on_image(st.session_state.original_image.copy(), st.session_state.ocr_data)
        st.image(annotated_image, use_column_width=True)
    
    with col2:
        st.subheader("Correct OCR Results")
        # Create editable fields for each OCR result
        for idx, item in enumerate(st.session_state.ocr_data):
            with st.container(border=True):
                col_a, col_b = st.columns([0.7, 0.3])
                with col_a:
                    new_text = st.text_input(
                        label=f"Text {idx+1}",
                        value=item['text'],
                        key=f"text_{idx}"
                    )
                with col_b:
                    st.write(f"Confidence: {item['confidence']:.2f}")
                    st.write(f"Position: {item['bounding_box'][0]}")
                
                # Update the OCR data when text changes
                if new_text != item['text']:
                    st.session_state.ocr_data[idx]['text'] = new_text
                    st.rerun()
        
        # Add download button for corrected JSON
        st.download_button(
            label="Download Corrected JSON",
            data=json.dumps(st.session_state.ocr_data, indent=2),
            file_name="corrected_ocr.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()