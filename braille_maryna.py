from imutils.perspective import four_point_transform as FPT
from collections import Counter
from skimage import io
import numpy as np
import imutils
import cv2
import re


# Braille Unicode patterns (6-dot)
braille_patterns = {
    '100000': '⠁', '001000': '⠂', '101000': '⠃', '000010': '⠄',
    '100010': '⠅', '001010': '⠆', '101010': '⠇', '010000': '⠈',
    '110000': '⠉', '011000': '⠊', '111000': '⠋', '010010': '⠌',
    '110010': '⠍', '011010': '⠎', '111010': '⠏', '000100': '⠐',
    '100100': '⠑', '001100': '⠒', '101100': '⠓', '000110': '⠔',
    '100110': '⠕', '001110': '⠖', '101110': '⠗', '010100': '⠘',
    '110100': '⠙', '011100': '⠚', '111100': '⠛', '010110': '⠜',
    '110110': '⠝', '011110': '⠞', '111110': '⠟', '000001': '⠠',
    '100001': '⠡', '001001': '⠢', '101001': '⠣', '000011': '⠤',
    '100011': '⠥', '001011': '⠦', '101011': '⠧', '010001': '⠨',
    '110001': '⠩', '011001': '⠪', '111001': '⠫', '010011': '⠬',
    '110011': '⠭', '011011': '⠮', '111011': '⠯', '000101': '⠰',
    '100101': '⠱', '001101': '⠲', '101101': '⠳', '000111': '⠴',
    '100111': '⠵', '001111': '⠶', '101111': '⠷', '010101': '⠸',
    '110101': '⠹', '011101': '⠺', '111101': '⠻', '010111': '⠼',
    '110111': '⠽', '011111': '⠾', '111111': '⠿', '000000': ' '
}

def braille_image_to_braille_text(url, iter=0, width=3000):
    """
  Convert a Braille image to text.

  Parameters:
  url (str): URL of the image containing Braille text
  iter (int): Number of iterations for erosion/dilation (default 0)
  width (int): Target width to resize the image (default 1500)

  Returns:
  str: Translated text from the Braille image
  """

    def get_image(url, iter=0, width=None):
        image = io.imread(url)
        if width:
            image = imutils.resize(image, width)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=iter)
        thresh = cv2.dilate(thresh, kernel, iterations=iter)
        ctrs = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ctrs = imutils.grab_contours(ctrs)
        return image, ctrs, image.copy(), gray, edged, thresh

    def get_diameter(ctrs):
        boundingBoxes = [list(cv2.boundingRect(c)) for c in ctrs]
        c = Counter([i[2] for i in boundingBoxes])
        mode = c.most_common(1)[0][0]
        return mode if mode > 1 else c.most_common(2)[1][0]

    def get_circles(ctrs, diam):
        questionCtrs = []
        for c in ctrs:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if diam * 0.8 <= w <= diam * 1.2 and 0.8 <= ar <= 1.2:
                questionCtrs.append(c)
        return questionCtrs

    def sort_contours(ctrs, diam, image):
        BB = [list(cv2.boundingRect(c)) for c in ctrs]
        tol = 0.7 * diam

        def sort(i):
            S = sorted(BB, key=lambda x: x[i])
            s = [b[i] for b in S]
            m = s[0]
            for b in S:
                if m - tol < b[i] < m or m < b[i] < m + tol:
                    b[i] = m
                elif b[i] > m + diam:
                    for e in s[s.index(m):]:
                        if e > m + diam:
                            m = e
                            break
            return sorted(set(s))

        xs = sort(0)
        ys = sort(1)
        (ctrs, BB) = zip(*sorted(zip(ctrs, BB), key=lambda b: b[1][1] * len(image) + b[1][0]))
        return ctrs, BB, xs, ys

    def get_spacing(boundingBoxes, xs, diam):
        def spacing(x):
            space = []
            coor = [b[x] for b in boundingBoxes]
            for i in range(len(coor) - 1):
                c = coor[i + 1] - coor[i]
                if c > diam // 2:
                    space.append(c)
            return sorted(list(set(space)))

        spacingX = spacing(0)
        spacingY = spacing(1)

        m = min(spacingX)
        d1 = spacingX[0]
        d2 = 0
        d3 = 0

        for x in spacingX:
            if d2 == 0 and x > d1 * 1.3:
                d2 = x
            if d2 > 0 and x > d2 * 1.3:
                d3 = x
                break

        linesV = []
        prev = 0
        linesV.append(min(xs) - (d2 - diam) / 2)

        for i in range(1, len(xs)):
            diff = xs[i] - xs[i - 1]
            if i == 1 and d2 * 0.9 < diff:
                linesV.append(min(xs) - d2 - diam / 2)
                prev = 1
            if d1 * 0.8 < diff < d1 * 1.2:
                linesV.append(xs[i - 1] + diam + (d1 - diam) / 2)
                prev = 1
            elif d2 * 0.8 < diff < d2 * 1.1:
                linesV.append(xs[i - 1] + diam + (d2 - diam) / 2)
                prev = 0
            elif d3 * 0.9 < diff < d3 * 1.1:
                if prev == 1:
                    linesV.append(xs[i - 1] + diam + (d2 - diam) / 2)
                    linesV.append(xs[i - 1] + d2 + diam + (d1 - diam) / 2)
                else:
                    linesV.append(xs[i - 1] + diam + (d1 - diam) / 2)
                    linesV.append(xs[i - 1] + d1 + diam + (d2 - diam) / 2)
            elif d3 * 1.1 < diff:
                if prev == 1:
                    linesV.append(xs[i - 1] + diam + (d2 - diam) / 2)
                    linesV.append(xs[i - 1] + d2 + diam + (d1 - diam) / 2)
                    linesV.append(xs[i - 1] + d3 + diam + (d2 - diam) / 2)
                    prev = 0
                else:
                    linesV.append(xs[i - 1] + diam + (d1 - diam) / 2)
                    linesV.append(xs[i - 1] + d1 + diam + (d2 - diam) / 2)
                    linesV.append(xs[i - 1] + d1 + d2 + diam + (d1 - diam) / 2)
                    linesV.append(xs[i - 1] + d1 + d3 + diam + (d2 - diam) / 2)
                    prev = 1

        linesV.append(max(xs) + diam * 1.5)
        if len(linesV) % 2 == 0:
            linesV.append(max(xs) + d2 + diam)

        return linesV, d1, d2, d3, spacingX, spacingY

    def get_letters(boundingBoxes, spacingY, diam, linesV):
        Bxs = list(boundingBoxes)
        Bxs.append((100000, 0))

        dots = [[]]
        for y in sorted(list(set(spacingY))):
            if y > 1.3 * diam:
                minYD = y * 1.5
                break

        for b in range(len(Bxs) - 1):
            if Bxs[b][0] < Bxs[b + 1][0]:
                dots[-1].append(Bxs[b][0])
            else:
                if abs(Bxs[b + 1][1] - Bxs[b][1]) < minYD:
                    dots[-1].append(Bxs[b][0])
                    dots.append([])
                else:
                    dots[-1].append(Bxs[b][0])
                    dots.append([])
                    if len(dots) % 3 == 0 and not dots[-1]:
                        dots.append([])

        letters = []

        for r in range(len(dots)):
            if not dots[r]:
                letters.append([0 for _ in range(len(linesV) - 1)])
                continue
            else:
                letters.append([])
                c = 0
                i = 0
                while i < len(linesV) - 1:
                    if c < len(dots[r]):
                        if linesV[i] < dots[r][c] < linesV[i + 1]:
                            letters[-1].append(1)
                            c += 1
                        else:
                            letters[-1].append(0)
                    else:
                        letters[-1].append(0)
                    i += 1

        return letters

    def letters_to_braille_dot(letters):
        braille_output = ""

        for row in letters[0]:
            binary_str = ''.join(map(str, row))  # Convert list of integers to a single binary string
            braille_char = braille_patterns.get(binary_str, '?')  # Get the Braille character, or '?' if not found
            if braille_char == '?':
                print(binary_str)
            braille_output += braille_char

        return braille_output

    def translate(letters):
        """
        Translates the Braille dot matrix into a binary dot representation.

        Parameters:
        letters (list): List of Braille dot matrices

        Returns:
        list: Binary dot representation of each Braille character
        """
        # Initialize a list to hold the binary dot patterns
        braille_dots = []

        # Convert each letter matrix into binary dot patterns
        letters_converted = np.array(letters)
        for row in range(0, len(letters), 3):
            row_pattern = []
            for col in range(0, len(letters_converted[0]), 2):
                # Each cell in Braille is a 2x3 matrix
                braille_cell = letters_converted[row:row + 3, col:col + 2]
                # Flatten the matrix to get binary dot pattern
                binary_pattern = braille_cell.flatten().tolist()
                row_pattern.append(binary_pattern)
            braille_dots.append(row_pattern)

        return braille_dots

    # Main execution flow
    image, ctrs, paper, gray, edged, thresh = get_image(url, iter, width)
    diam = get_diameter(ctrs)
    dotCtrs = get_circles(ctrs, diam)
    questionCtrs, boundingBoxes, xs, ys = sort_contours(dotCtrs, diam, image)
    linesV, d1, d2, d3, spacingX, spacingY = get_spacing(boundingBoxes, xs, diam)
    letters = get_letters(boundingBoxes, spacingY, diam, linesV)
    letters_converted = translate(letters)
    braille_dot = letters_to_braille_dot(letters_converted)
    return braille_dot