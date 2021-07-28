import source.data.image2text as i2t

def main():
    print("ALPHA-FLOW-FREE")
    print("Start solving the puzzle ...")

    ## Get image path in root directory
    # image_path = "./data/image/7x7_1.PNG"
    image_path = "./data/image/13x13_1.PNG"

    ## Convert data in root directory from image to text
    text_path = i2t.image2text(image_path)

    print("Done!")

if __name__ == "__main__":
    main()
