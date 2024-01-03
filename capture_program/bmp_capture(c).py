import pyautogui
import time
from PIL import ImageGrab, Image
import os
import keyboard
import pyperclip

def find_next_available_filename(folder, base_filename):
    # Initialize the counter
    counter = 1

    while True:
        # Generate the next filename
        filename = f"{base_filename}_{counter:05}.bmp"
        full_path = os.path.join(folder, filename)

        # Check if the file already exists
        if not os.path.exists(full_path):
            return full_path
        
        # If the file exists, increment the counter and try again
        counter += 1

def capture_and_save_image(save_folder, file_prefix):
    while True:
        # Wait for the 'home' key or 'end' key to be pressed
        print("Press 'home' key to capture an image or 'end' key to exit...")
        event = keyboard.read_event(suppress=False)

        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'home':
                # Get the current mouse cursor position
                x, y = pyautogui.position()

                # Calculate the coordinates for the top-left and bottom-right corners of the square
                left = x
                top = y
                right = x + 20
                bottom = y + 20

                # Print the region coordinates with +10 increments
                region_info = f"region: ( {left}, {top}, {right}, {bottom} )"
                print(region_info)

                # Copy the region_info to the clipboard
                pyperclip.copy(region_info)

                # Capture the screenshot of the square region
                screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

                # Find the next available filename
                file_path = find_next_available_filename(save_folder, file_prefix)

                # Save the captured image as a BMP image with the generated filename
                screenshot.save(file_path, "BMP")

                print(f"Image saved as {file_path}")
            elif event.name == 'end':
                # Exit the loop when 'end' key is pressed
                break

# Example usage:
save_folder = "C:\\_test\\_bmp"  # 이미지를 저장할 폴더 경로를 설정하세요.
file_prefix = "captured_image"  # 저장된 이미지 파일 이름의 접두사를 설정하세요.

# Capture and save images when the 'home' key is pressed or exit with the 'end' key
capture_and_save_image(save_folder, file_prefix)
