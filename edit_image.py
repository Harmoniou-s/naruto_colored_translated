from PIL import Image,ImageEnhance,ImageChops
from cv2 import cv2, countNonZero, cvtColor
import numpy as np

def mask_non_colored_image():
    img1 = Image.open(r"C:/Users/Work/Git/naruto_colored_translated/non_color/Naruto v01/Naruto v1-032.jpg")
    img2 = Image.open(r"C:/Users/Work/Git/naruto_colored_translated/Naruto color v01-10/Vol 1/00032.jpg")
    if img2.size[0]/img2.size[1] < 0.7:
        resized_im_1 = img1.resize((780, 1200))
        print(resized_im_1.size[0], resized_im_1.size[1 ])
        resized_im_2 = img2.resize((780, 1200))
        resized_im_1 = crop_left_right(resized_im_1)
        resized_im_2 = crop_left_right_rgb(resized_im_2)
        resized_im_2.save('img2.jpg')
        image_data_1 = resized_im_1.load()
        masked_image = resized_im_2
        masked_image_data = masked_image.load()
        #masked_image = masked_image.transform(masked_image.size, Image.AFFINE, (1, 0, -22, 0, 1, 2))
        for width in range(resized_im_2.size[0]):
            for height in range(resized_im_2.size[1]):
                r,g,b = masked_image_data[width, height]
                if (r == b and b == g) or (r > 252 and g > 252 and b > 252):
                    clamph = clamp(height, 0, resized_im_1.height - 1)
                    clampw = clamp(width, 0, resized_im_1.width - 1)
                    w = image_data_1[clampw, clamph]
                    masked_image_data[width, height] = w,w,w
        resized_im_1.save('img1.jpg')
        
        masked_image.save('masked_image.jpg')

def crop_left_right(img):
    left_to_remove = 0
    img_data = img.load()
    last_line = False
    for width in range(img.size[0]):
        if last_line:
            break
        else:
            left_to_remove = width
        for height in range(img.size[1]):
            w = img_data[width, height]
            if w < 20  :
                last_line = True
                break
            
    right_to_remove = 0
    last_line = False
    for width in range(img.size[0]):
        if last_line:
            print(img.size[0]-width - 1, img.size[1]-height - 1)
            print(img_data[img.size[0]-width - 1, img.size[1]-height - 1])
            break
        else:
            right_to_remove = width
        for height in range(img.size[1]):
            w = img_data[img.size[0]-width - 1, img.size[1]-height - 1]
            if w < 20 :
                last_line = True
                break
    print (right_to_remove)
    img = img.crop((left_to_remove, 0, img.width, img.height))
    img = img.crop((0, 0, img.width - right_to_remove, img.height)) 
    return img

def crop_left_right_rgb(img):
    left_to_remove = 0
    img_data = img.convert("RGB").load()
    last_line = False
    for width in range(img.size[0]):
        if last_line:
            break
        else:
            left_to_remove = width + 6
        for height in range(img.size[1]):
            r,g,b = img_data[width, height]
            if not(r == b and b == g):
                print (r,g,b)
                last_line = True
                break


    right_to_remove = 0
    last_line = False
    for width in range(img.size[0]):
        if last_line:
            break
        else:
            right_to_remove = width
        for height in range(img.size[1]):
            r,g,b = img_data[img.size[0]-width - 1, img.size[1]-height - 1]
            if not(r == b and b == g ):
                last_line = True
                break
    img = img.crop((left_to_remove, 0, img.width, img.height))
    img = img.crop((0, 0, img.width - right_to_remove, img.height)) 
    return img

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
if __name__ == "__main__":
    mask_non_colored_image()
