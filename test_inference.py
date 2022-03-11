import pandas
import numpy as np
from rembg.bg import remove
import io
from PIL import Image
import cv2


def main():

    # Load the image using Image
    img = Image.open('test_images/test1.jpg')

    #remove background
    img = remove(img)

    img= Image.open(io.BytesIO(img)).convert("RGBA")

    #convert rgb to bgr
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGRA)

    #save images in test folder
    cv2.imwrite('test_images/test1_out.png', img)

if __name__ == "__main__":
    main()

