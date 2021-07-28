import os
import cv2
import numpy as np

## Defined macros
IMAGE_SCALE         = 0.5
THRESHOLD           = 100
MIN_HW_LINE         = 500
CLOSING_KERNEL      = 7
ARC_LENGTH_SCALE    = 0.01
CONTOUR_LENGTH      = 7
                    #           [ B    G    R    C ]
COLOR_BASE          = np.array([[ 64,  77, 231, "A"],  # Red
                                [ 77, 158,  95, "B"],  # Green
                                [245,  74,  57, "C"],  # Blue
                                [ 56, 176, 182, "D"],  # Yellow
                                [ 41, 115, 191, "E"],  # Orange
                                [212, 211,  97, "F"],  # Cyan
                                [200,  83, 230, "G"],  # Magenta
                                [ 80,  84, 166, "H"],  # Brown
                                [133,  36, 126, "I"],  # Purple
                                [  0,   0,   0, "J"],  # White
                                [  0,   0,   0, "K"],  # Gray
                                [  0,   0,   0, "L"],  # Lime
                                [  0,   0,   0, "M"],  # Beige
                                [  0,   0,   0, "N"],  # Navy
                                [  0,   0,   0, "O"],  # Teal
                                [  0,   0,   0, "P"]]) # Pink

COLOR_TOLERANCE     = 0.05 # 5%

## Image to text function
def image2text(input_image_path):
    print(">> image2text")

    ## Read input image in root directory
    original_image = cv2.imread(input_image_path)
    # cv2.imshow("Original Image", original_image)

    ## Extract grid image from original image
    grid_image = original2grid(original_image)
    # cv2.imshow("Grid Image", grid_image)

    ## Crop original image based on grid image
    cropped_image = grid2cropped(original_image, grid_image)
    # cv2.imshow("Cropped Image", cropped_image)

    ## Standardize cropped image for converting
    standard_image = cropped2standard(cropped_image)
    # cv2.imshow("Standard Image", standard_image)

    ## Show and save image
    # show_image(standard_image)
    save_image(standard_image, input_image_path)

    ## Convert standard image to char array
    char_array = standard2array(standard_image, cropped_image)

    ## Write char array data to output text based on input image path
    output_text_path = array2text(char_array, input_image_path)
    # print("|Text path:", output_text_path)

    print("<< image2text")
    return output_text_path

def show_image(input_image):
    ## Scale input image
    height = int(input_image.shape[0] * IMAGE_SCALE)
    width = int(input_image.shape[1] * IMAGE_SCALE)

    output_image = cv2.resize(input_image, (width, height))
    cv2.imshow("Output Image", output_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image(input_image, input_image_path):
    ## Create output image path to save input image based on input image path
    output_image_path = os.path.splitext(input_image_path)[0] + "_standard" + os.path.splitext(input_image_path)[1]
    output_image_path = output_image_path.replace("image", "image/standard")
    cv2.imwrite(output_image_path, input_image)

def original2grid(input_image):
    print(" >> original2grid")

    ## Convert input color image into grayscale image
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Grayscale Image", grayscale_image)

    ## Threshold grayscale image
    ret, threshold_image = cv2.threshold(grayscale_image, THRESHOLD, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("Threshold Image", threshold_image)

    ## Apply morphological transformation(s)
    horizontal_kernel = np.ones((1, MIN_HW_LINE), np.uint8)
    horizontal_image = cv2.morphologyEx(threshold_image, cv2.MORPH_OPEN, horizontal_kernel)
    # cv2.imshow("Horizontal Image", horizontal_image)

    vertical_kernel = np.ones((MIN_HW_LINE, 1), np.uint8)
    vertical_image = cv2.morphologyEx(threshold_image, cv2.MORPH_OPEN, vertical_kernel)
    # cv2.imshow("Vertical Image", vertical_image)

    ## Calculate board size (grid size)
    global board_size
    contours, hierarchy = cv2.findContours(horizontal_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    board_size = len(contours) - 1
    # print(" |Board size:", board_size)

    ## Extract grid image from horizontal and vertical images
    output_image = horizontal_image | vertical_image
    # cv2.imshow("Output Image", output_image)

    print(" << original2grid")
    return output_image

def grid2cropped(input_image, based_image):
    print(" >> grid2cropped")
    half_height = int(based_image.shape[0] / 2)
    half_width = int(based_image.shape[1] / 2)

    ## Find up edge of grid contour
    for up in range(based_image.shape[0]):
        if based_image[up, half_width] != 0: break

    ## Find down edge of grid contour
    for down in range(based_image.shape[0] - 1, -1, -1):
        if based_image[down, half_width] != 0: break

    ## Find left edge of grid contour
    for left in range(based_image.shape[1]):
        if based_image[half_height, left] != 0: break

    ## Find right edge of grid contour
    for right in range(based_image.shape[1] - 1, -1, -1):
        if based_image[half_height, right] != 0: break

    # print(" |Up edge value: ", up)
    # print(" |Down edge value: ", down)
    # print(" |Left edge value: ", left)
    # print(" |Right edge value: ", right)

    ## Crop input image based on 4 edges and based image
    # output_image = input_image[412:1651, 0:1239]    # Manual crop
    output_image = input_image[up:down, left:right] # Auto crop
    # cv2.imshow("Output Image", output_image)

    print(" << grid2cropped")
    return output_image

def cropped2standard(input_image):
    print(" >> cropped2standard")

    ## Convert input color image into grayscale image
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Grayscale Image", grayscale_image)

    ## Threshold grayscale image
    ret, threshold_image = cv2.threshold(grayscale_image, THRESHOLD, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("Threshold Image", threshold_image)

    ## Apply morphological closing transformation(s) to standardize threshold image for converting
    closing_kernel = np.ones((CLOSING_KERNEL, CLOSING_KERNEL), np.uint8)
    output_image = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, closing_kernel)
    # cv2.imshow("Output Image", output_image)

    print(" << cropped2standard")
    return output_image

def standard2array(input_image, based_image):
    print(" >> standard2array")

    ## Create output array to store text data
    output_array = np.chararray([board_size, board_size])
    output_array[:] = "*"

    ## Find circle contours of input image
    contours, hierarchy = cv2.findContours(input_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        ## Calculate approximate contour to differentiate circles from squares
        approx_contour = cv2.approxPolyDP(contour, ARC_LENGTH_SCALE * cv2.arcLength(contour, True), True)
        # print(" |Approximate contour:", len(approx_contour))

        if len(approx_contour) > CONTOUR_LENGTH:
            # print(" |Approximate contour:", len(approx_contour))

            ## Calculate circle coordinates in board plane from circle center point coordinates in image plane
            (image_cx, image_cy), radius = cv2.minEnclosingCircle(contour)
            board_cx = int((image_cx * board_size) / input_image.shape[1])
            board_cy = int((image_cy * board_size) / input_image.shape[0])
            output_array[board_cy, board_cx] = "X" ## For debugging
            # print(" |Board Cx:", board_cx, "\t| Board Cy:", board_cy)

            ## Create mask image with white circle to detect color inside circle contour
            mask_image = np.zeros(based_image.shape[:2], np.uint8)
            cv2.drawContours(mask_image, [contour], -1, 255, -1)
            # print(" |Circle color:", cv2.mean(based_image, mask_image)[:3])

            ## Draw circle contours in based image with green color or circle color
            # cv2.drawContours(based_image, [contour], -1, (0, 255, 0), 3)
            cv2.drawContours(based_image, [contour], -1, cv2.mean(based_image, mask_image), -1)
            # print(" |Circle color:", cv2.mean(based_image, mask_image)[:3])

            ## Convert detected color inside circle contour into color abbreviation
            circle_color = cv2.mean(based_image, mask_image)[:3]

            for color_index in range(COLOR_BASE.shape[0]): ## Scan through all base colors
                counter = 0

                for bgr in range(COLOR_BASE.shape[1] - 1): ## Scan through blue-green-red attributes
                    color_base = float(COLOR_BASE[color_index][bgr])

                    ## Check if blue-green-red attribute value is in range of color base value +/- color tolerance
                    if (color_base * (1 - COLOR_TOLERANCE)) <= circle_color[bgr] <= (color_base * (1 + COLOR_TOLERANCE)):
                        counter += 1
                    else: break

                if counter == 3:
                    ## Replace output array text data on the same board plane coordinates with color abbreviation
                    output_array[board_cy, board_cx] = COLOR_BASE[color_index][3]
                    break

    # show_image(based_image)
    print(" << standard2array")
    return output_array

def array2text(input_array, input_image_path):
    print(" >> array2text")

    ## Create output text path based on input image path
    output_text_path = os.path.splitext(input_image_path)[0] + ".txt"
    output_text_path = output_text_path.replace("image", "text")

    ## Open output text to read and write data
    output_text = open(output_text_path, "w+")

    for i in range(board_size):
        input_array[i].tofile(output_text, sep = "", format = "%s")
        output_text.write("\n")

    output_text.close()

    print(" >> array2text")
    return output_text_path
