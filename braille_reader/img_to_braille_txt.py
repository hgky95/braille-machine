import cv2
import numpy as np


def process_image(image_path):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to separate circles from background
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("thresh.png", thresh)

    # Find contours of the circles
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by y-coordinate first, and by x-coordinate in case of a tie
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    print("Countors found:", len(contours))

    # Define a threshold for grouping contours into rows (based on y-coordinates)
    row_threshold = 10
    rows = []
    current_row = []
    last_y = None

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        # If first contour or within threshold, add to the current row
        if last_y is None or abs(y - last_y) <= row_threshold:
            current_row.append((x, y, w, h))
        else:
            # Append the completed row and start a new one
            rows.append(current_row)
            current_row = [(x, y, w, h)]

        # Update last_y for the next contour
        last_y = y

    # Append the last row if there are any remaining contours
    if current_row:
        rows.append(current_row)

    print(rows)
    sorted_lists = [sorted(sublist, key=lambda x: x[0]) for sublist in rows]
    print(sorted_lists)

    encoding = []
    for row in sorted_lists:
        for dot in row:
            x, y, w, h = dot
            center_x = int(x + (w / 2))
            center_y = int(y + (h / 2))

            # print("center_x center_y:", center_x, center_y)
            # Check if the center point is white or black
            center_pixel_value = thresh[center_y, center_x]
            # print("center_pixel_value:", center_pixel_value)

            if center_pixel_value == 255:
                encoding.append(1)
            else:
                encoding.append(0)

    return tuple(encoding)

braille_map = {
    (1, 0, 0, 0, 0, 0): 'a',
    (1, 0, 1, 0, 0, 0): 'b',
    (1, 1, 0, 0, 0, 0): 'c',
    (1, 0, 1, 1, 0, 0): 'd',
    (1, 0, 0, 1, 0, 0): 'e',
    (1, 1, 1, 0, 0, 0): 'f',
    (1, 1, 1, 1, 0, 0): 'g',
    (1, 1, 0, 1, 0, 0): 'h',
    (0, 1, 1, 0, 0, 0): 'i',
    (0, 1, 1, 1, 0, 0): 'j',
    (1, 0, 0, 0, 1, 0): 'k',
    (1, 1, 0, 0, 1, 0): 'l',
    (1, 0, 1, 0, 1, 0): 'm',
    (1, 0, 1, 1, 1, 0): 'n',
    (1, 0, 0, 1, 1, 0): 'o',
    (1, 1, 1, 0, 1, 0): 'p',
    (1, 1, 1, 1, 1, 0): 'q',
    (1, 1, 0, 1, 1, 0): 'r',
    (0, 1, 1, 0, 1, 0): 's',
    (0, 1, 1, 1, 1, 0): 't',
    (1, 0, 0, 0, 1, 1): 'u',
    (1, 1, 0, 0, 1, 1): 'v',
    (0, 1, 1, 1, 0, 1): 'w',
    (1, 0, 1, 0, 1, 1): 'x',
    (1, 0, 1, 1, 1, 1): 'y',
    (1, 0, 0, 1, 1, 1): 'z'
}

# Example usage:
image_path = r"..\images\Braille_G.jpg"  # Replace with your image path
encoding = process_image(image_path)
print("encoding of character:", encoding)
print("converted text:", braille_map[encoding])