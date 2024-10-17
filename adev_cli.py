import os
import subprocess
from tkinter import filedialog
from tkinter import Tk

def select_folder(prompt):
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=prompt)
    root.destroy()
    return folder_path

def get_user_inputs():
    action = input("Enter the action (encode or decode): ").strip()
    watermark_type = input("Enter the watermark type (bytes, b16, bits, uuid, ipv4): ").strip()
    method = input("Enter the encoding/decoding method (dwtDct, dwtDctSvd, rivaGan): ").strip()
    watermark_text = ""
    length = ""
    if action == "encode":
        watermark_text = input("Enter the watermark text: ").strip()
    elif action == "decode" and watermark_type in ["bytes", "b16", "bits"]:
        length = input("Enter the length of watermark bits: ").strip()
    return action, watermark_type, method, watermark_text, length

input_folder = select_folder("Select the folder containing the images to watermark or decode")
action, watermark_type, method, watermark_text, length = get_user_inputs()
if action == "encode":
    
    output_folder = select_folder("Select the folder to save the processed images")
    
invisible_watermark_script_path = "invisible-watermark.py"

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')): 
        input_path = os.path.join(input_folder, filename)
        command = [
            "python", invisible_watermark_script_path, "-v",
            "-a", action,
            "-t", watermark_type,
            "-m", method
        ]
        if action == "encode":
            output_filename = os.path.splitext(filename)[0] + "_processed" + os.path.splitext(filename)[1]
            output_path = os.path.join(output_folder, output_filename)
            command.extend(["-w", watermark_text, "-o", output_path])
        elif action == "decode" and length:
            command.extend(["-l", length])
        command.append(input_path)
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            if action == "decode":
                print(f"Decoded watermark from {filename}: {result.stdout.strip()}")
            else:
                print(f"Successfully processed: {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to process: {filename}, Error: {str(e)}")
            
print("All images have been processed.")
