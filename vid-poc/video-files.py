import cv2
import imagehash
from PIL import Image
import os
import numpy as np


def remove_duplicates(images_folder):
    hash_list = []
    unique_images = []
    for img_file in os.listdir(images_folder):
        img_path = os.path.join(images_folder, img_file)
        if os.path.isfile(img_path):
            img_hash = imagehash.average_hash(Image.open(img_path))
            if img_hash not in hash_list:
                hash_list.append(img_hash)
                unique_images.append(img_path)
            else:
                os.remove(img_path)  # Remove duplicate image


def remove_duplicates_new(images_folder):
    hash_list = []
    unique_images = []
    previous_image = None

    for img_file in sorted(os.listdir(images_folder)):
        img_path = os.path.join(images_folder, img_file)
        if os.path.isfile(img_path):
            current_image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if previous_image is not None:
                # Calculate structural similarity index (SSI)
                ssi = cv2.matchTemplate(previous_image, current_image, cv2.TM_CCOEFF_NORMED)
                similarity = np.max(ssi)
                if similarity > 0.95:  # If similarity is high, consider it a duplicate
                    os.remove(img_path)
                    continue
            previous_image = current_image
            unique_images.append(img_path)


def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    success, frame = cap.read()
    
    while success:
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1
        success, frame = cap.read()
    
    cap.release()


if __name__ == "__main__":
    video_file = "/Users/vishvaraj/projects/img-obj-detection-service/20240528_162359.mp4"  # Replace with your video file path
    output_directory = "/Users/vishvaraj/projects/img-obj-detection-service/exp-test/extracted_file2"

    # extract_frames(video_file, output_directory)

    # remove_duplicates(output_directory)
    remove_duplicates_new(output_directory)

    print("Extraction and duplicate removal complete.")
