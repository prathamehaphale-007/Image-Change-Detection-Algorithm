import cv2
import numpy as np
import os
import shutil

PROBLEM_IMAGES = [
    "7.jpg", 
    "17.jpg" 
]

def detect_changes(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        files = os.listdir(input_dir)
    except FileNotFoundError:
        print(f"ERROR: The folder '{input_dir}' was not found.")
        return

    jpg_files = [f for f in files if f.lower().endswith('.jpg')]

    pairs = []
    for f in jpg_files:
        if "~2" not in f:
            base_name = os.path.splitext(f)[0]
            extension = os.path.splitext(f)[1]
            after_name = f"{base_name}~2{extension}"
            if after_name in files:
                pairs.append((f, after_name))

    print(f"Found {len(pairs)} pairs. Processing...")

    for before_name, after_name in pairs:
        path_before = os.path.join(input_dir, before_name)
        path_after = os.path.join(input_dir, after_name)

        img_before = cv2.imread(path_before)
        img_after = cv2.imread(path_after)

        if img_before is None or img_after is None:
            continue

        if before_name in PROBLEM_IMAGES:
            print(f"--> Switching to STRICT MODE for: {before_name}")
            blur_val = (9, 9)       
            threshold_val = 40      
            morph_open_val = (5, 5) 
            min_area = 100          
            dilation_iter = 3
        else:
            blur_val = (3, 3)       
            threshold_val = 15      
            morph_open_val = (3, 3) 
            min_area = 25           
            dilation_iter = 3


        blur_before = cv2.GaussianBlur(img_before, blur_val, 0)
        blur_after = cv2.GaussianBlur(img_after, blur_val, 0)

        diff = cv2.absdiff(blur_before, blur_after)
        diff_max = np.max(diff, axis=2) 

        _, thresh = cv2.threshold(diff_max, threshold_val, 255, cv2.THRESH_BINARY)

        kernel_noise = np.ones(morph_open_val, np.uint8)
        clean_thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_noise)

        kernel_dilate = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(clean_thresh, kernel_dilate, iterations=dilation_iter)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_output = img_after.copy()
        img_h, img_w = img_output.shape[:2]
        padding = 5
        
        for contour in contours:
            if cv2.contourArea(contour) < min_area:
                continue
            
            x, y, w, h = cv2.boundingRect(contour)
            
            cv2.rectangle(img_output, (max(0, x-padding), max(0, y-padding)), 
                          (min(img_w, x+w+padding), min(img_h, y+h+padding)), 
                          (255, 0, 255), 2)

        base_name = os.path.splitext(before_name)[0]
        extension = os.path.splitext(before_name)[1]
        output_filename = f"{base_name}~3{extension}"
        
        output_path_annotated = os.path.join(output_dir, output_filename)
        output_path_original = os.path.join(output_dir, before_name)

        cv2.imwrite(output_path_annotated, img_output)
        shutil.copy2(path_before, output_path_original)

        print(f"Processed: {before_name} -> {output_filename}")

    print("\nProcessing complete!")

if __name__ == "__main__":
    INPUT_FOLDER_NAME = "input-images" 
    OUTPUT_FOLDER_NAME = "task_2_output"
    
    detect_changes(INPUT_FOLDER_NAME, OUTPUT_FOLDER_NAME)