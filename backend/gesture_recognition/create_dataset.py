import os
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

# This is the handtracking model from media pipe
mp_hands = mp.solutions.hands 

# This is used to draw the hand landmarks on images for visualization.
mp_drawings = mp.solutions.drawing_utils

# This offers styling options for the landmarks drawn on the images, such as different colors or line thicknesses.
mp_drawing_styles = mp.solutions.drawing_styles

# Setting true means that Im running hand detection on every individual image.
# Detections below 30% confidence will be ignored.
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Getting the directory where this script file is located
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Setting the directory where the data is stored, relative to this script file
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# Loop through each subdirectory in the data directory
for dir_ in os.listdir(DATA_DIR):
    # Construct the full path to the subdirectory
    class_dir = os.path.join(DATA_DIR, dir_)
    # Make sure it's a directory
    if os.path.isdir(class_dir):
        # Loop through each image in the subdirectory
        for img_path in os.listdir(class_dir)[:1]: # Using slicing to ensure I'm only showing 1
            # Construct the full path to the image
            img_full_path = os.path.join(class_dir, img_path)
            # Make sure it's a file before reading
            if os.path.isfile(img_full_path):
                # Read the image using OpenCV
                img = cv2.imread(img_full_path)
                # Changes the image data into rgb so that matplotlib can actually comprehend whats happening
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Iterate over all the landmarks I'v detected in this image
                results = hands.process(img_rgb) 
                # Have to make sure we are detecing at least one hand before continuing:
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # For each result we are going to draw the landmarks on top of the image essentially.
                        mp_drawings.draw_landmarks(
                            img_rgb,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS, # The predefined connections between hand landmarks (i.e., how the landmarks are linked to each other).
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )

                plt.figure()
                plt.imshow(img_rgb) # Loading the image for each image in the path

# Using MatplotLib to show the images!
plt.show()
 
