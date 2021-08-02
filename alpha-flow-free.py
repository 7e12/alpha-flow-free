import source.data.image_processor as improc
import source.model.alpha as alpha

def main():
    print("ALPHA-FLOW-FREE")
    print("Start solving the puzzle ...")

    ## Get an image path in root directory
    image_path = "./data/image/7x7_1.PNG"
    # image_path = "./data/image/13x13_1.PNG"

    ## Convert data in the root directory from image to text
    text_path = improc.image2text(image_path)
    # text_path = "./data/text/7x7_1.txt"
    # text_path = "./data/text/13x13_1.txt"

    ## Load text data into the alpha model to solve
    solution_path = alpha.flow_free(text_path)

    print("Done!")

if __name__ == "__main__":
    main()
