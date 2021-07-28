import cv2

## Defined macros
IMAGE_SCALE         = 0.5

## Image to text function
def image2text(input_image_path):
    print(">> image2text")

    ## Read input image in root directory
    original_image = cv2.imread(input_image_path)
    # cv2.imshow("Original Image", original_image)

    ## Show image
    show_image(original_image)

    print("<< image2text")
    return "output_text_path"

def show_image(input_image):
    ## Scale input image
    height = int(input_image.shape[0] * IMAGE_SCALE)
    width = int(input_image.shape[1] * IMAGE_SCALE)

    output_image = cv2.resize(input_image, (width, height))
    cv2.imshow("Output Image", output_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
