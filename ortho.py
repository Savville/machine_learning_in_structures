#GROK

import cv2
import numpy as np

# Load the image
img = cv2.imread('/Door5.jpg') #Change 

# Check if the image was loaded successfully
if img is None:
    print(f"Error: Image not found at '/Door3.jpg'. Please check the file path.")
else:
    # Convert to HSV for color thresholding
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for green color (adjust if necessary)
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Create mask for green dots
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours of green dots
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find centers of contours (ignoring small noise)
    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10:  # Filter out small noise
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centers.append((cx, cy))

    # Sort centers by y-coordinate
    sorted_centers = sorted(centers, key=lambda p: p[1])

    # Select top and bottom groups (ignoring the fifth dot)
    if len(sorted_centers) >= 4: # Changed from 5 to 4 to handle cases with exactly 4 dots
        # Take the first 2 as top (top-left and top-right)
        top_two = sorted_centers[:2]
        # Take the last 2 as bottom (bottom-left and bottom-right)
        bottom_two = sorted_centers[-2:]

        # Sort top_two by x-coordinate
        left_top = min(top_two, key=lambda p: p[0])
        right_top = max(top_two, key=lambda p: p[0])

        # Sort bottom_two by x-coordinate
        left_bottom = min(bottom_two, key=lambda p: p[0])
        right_bottom = max(bottom_two, key=lambda p: p[0])

        # Define source points (src_pts) for homography
        src_pts = np.array([left_top, right_top, right_bottom, left_bottom], dtype='float32')

        # Define destination points (dst_pts) with real-world dimensions
        # Height = 2 m = 2000 mm, Width = 0.8 m = 800 mm (1 pixel = 1 mm)
        dst_pts = np.array([[0, 0], [800, 0], [800, 2000], [0, 2000]], dtype='float32')

        # Compute homography matrix
        M, _ = cv2.findHomography(src_pts, dst_pts)

        # Apply homography to get orthographic view
        ortho_img = cv2.warpPerspective(img, M, (800, 2000))

        # Save orthographic image
        cv2.imwrite('ortho_img.jpg', ortho_img)
        print("Orthographic image saved successfully.")

        # Detect edges on the orthographic view
        ortho_gray = cv2.cvtColor(ortho_img, cv2.COLOR_BGR2GRAY)
        ortho_edges = cv2.Canny(ortho_gray, 50, 150)
        cv2.imwrite('ortho_edges.jpg', ortho_edges)
        print("Edge map saved successfully.")

        # Note: For CAD integration, convert ortho_edges.jpg to vector paths using Potrace
        # Example command: potrace -s ortho_edges.jpg -o door.svg
    else:
        print("Error: Not enough green dots detected. Please ensure there are at least 4 green dots.")
