import matplotlib.pyplot as plt
import cv2
import numpy as np

# Define the Braille dictionary mapping dot patterns to English letters
braille_dict = {
    (1, 0, 0, 0, 0, 0): 'a',
    (1, 1, 0, 0, 0, 0): 'b',
    (1, 0, 1, 0, 0, 0): 'c',
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
    (1, 0, 0, 1, 1, 1): 'z',
}

# Function to load and preprocess the image
def preprocess_image(image_path):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    # Apply binary thresholding to create a binary image
    _, binary_image = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY_INV)
    return binary_image

# Function to detect Braille dots in the image
def detect_braille_dots(binary_image):
    # Find contours to detect Braille dots
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print("contours")
    print(len(contours))
    print("contour_image")
    # Draw contours on a copy of the original image
    contour_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)  # Convert to color for better visualization
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)  # Draw contours in green
    
    # Show the original image and the image with contours
    plt.subplot(1, 2, 1)
    plt.imshow(binary_image, cmap='gray')
    plt.title("Binary Image")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(contour_image)
    plt.title("Contours")
    plt.axis('off')
    plt.show()
    
    dot_positions = []

    # Loop through each contour and filter based on size to identify Braille dots
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # if 5 < w < 20 and 5 < h < 20:  # Adjust size range as needed for your image
        dot_positions.append((x, y))
    
    # Sort dots by position: first by y (vertical) and then by x (horizontal)
    dot_positions = sorted(dot_positions, key=lambda pos: (pos[1], pos[0]))
    print("dot_positions")
    print(dot_positions)
    return dot_positions

# Function to convert detected dots into Braille characters
def convert_dots_to_text(dot_positions):
    # Constants for Braille grid size (adjust as needed)
    # cell_width = 30
    # cell_height = 50

    # Calculate vertical and horizontal distances between dots
    vertical_distances = []
    horizontal_distances = []

    print("len(dot_positions)" + str(len(dot_positions)))
    
    for i in range(1, len(dot_positions)):
        x1, y1, w1, h1 = dot_positions[i-1]
        x2, y2, w2, h2 = dot_positions[i]
        
        # Check if dots are in the same column (similar x position)
        if abs(x2 - x1) < (w1 + w2) // 2:
            vertical_distances.append(y2 - y1)
        
        # Check if dots are in the same row (similar y position)
        if abs(y2 - y1) < (h1 + h2) // 2:
            horizontal_distances.append(x2 - x1)
    
    # Calculate cell width and height as the median of distances between dots
    cell_height = int(np.median(vertical_distances)) if vertical_distances else 0
    cell_width = int(np.median(horizontal_distances)) if horizontal_distances else 0

    print("cell_height: " + cell_height)
    print("cell_width: " + cell_width)

    # Organize dots into Braille cells
    braille_text = ""
    rows = {}

    # Group dots into rows
    for x, y in dot_positions:
        row = y // cell_height
        if row not in rows:
            rows[row] = []
        rows[row].append((x, y))

    # Iterate through each row to interpret Braille characters
    for row in sorted(rows.keys()):
        cells = []
        dots = sorted(rows[row], key=lambda pos: pos[0])  # Sort dots horizontally

        # Group dots into Braille cells
        for i in range(0, len(dots), 6):  # Each Braille cell has 6 dots
            cell = [0] * 6  # Initialize a 2x3 Braille cell

            for j in range(6):
                if i + j < len(dots):
                    x, y = dots[i + j]
                    # Calculate dot position in the 2x3 Braille cell
                    dot_index = (y % cell_height) // (cell_height // 3) * 2 + (x % cell_width) // (cell_width // 2)
                    if 0 <= dot_index < 6:
                        cell[dot_index] = 1

            # Convert the Braille cell to a character
            braille_char = braille_dict.get(tuple(cell), '?')  # Use '?' for unknown patterns
            cells.append(braille_char)

        braille_text += "".join(cells) + " "
    
    return braille_text.strip()

# Main function to process the image and print Braille text
def main(image_path):
    binary_image = preprocess_image(image_path)
    # Display the binary image
    plt.imshow(binary_image, cmap='gray')
    plt.title("Binary Image")
    plt.axis('off')  # Hide axes for cleaner display
    plt.show()
    dot_positions = detect_braille_dots(binary_image)
    braille_text = convert_dots_to_text(dot_positions)
    print("Extracted Braille Text:", braille_text)

# Example usage
#Uploaded the same image in images folder
image_path = r'images\Braille_Hello.png'
main(image_path)
