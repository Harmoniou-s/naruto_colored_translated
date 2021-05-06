from PIL import Image,ImageEnhance,ImageChops
from cv2 import cv2, countNonZero, cvtColor
import numpy as np

def mask_non_colored_image():
    img1 = Image.open(r"C:/Users/Work/Git/naruto_colored_translated/non_color/Naruto v01/Naruto v1-022.jpg")
    img2 = Image.open(r"C:/Users/Work/Git/naruto_colored_translated/Naruto color v01-10/Vol 1/00022.jpg")
    if img2.size[0]/img2.size[1] < 0.7:
        resized_im_1 = img1.resize((780, 1200))
        resized_im_2 = img2.resize((780, 1200))
        resized_im_1 = crop_left_right(resized_im_1)
        resized_im_2 = crop_left_right_rgb(resized_im_2)
        resized_im_1 = resized_im_1.resize((780, 1200))
        resized_im_2 = resized_im_2.resize((780, 1200))
        resized_im_2.save('img2.jpg')
        image_data_1 = resized_im_1.load()
        masked_image = resized_im_2
        masked_image_data = masked_image.load()
        for width in range(masked_image.size[0]):
            for height in range(masked_image.size[1]):
                r,g,b = masked_image_data[width, height]
                if (r == b and b == g) or (r > 252 and g > 252 and b > 252):
                    w = image_data_1[width, height]
                    masked_image_data[width, height] = w,w,w
        resized_im_1.save('img1.jpg')
        
        masked_image.save('masked_image.jpg')

def crop_left_right(img):
    left_to_remove = 0
    img_data = img.load()
   
    for width in range(img.size[0]):
        w = 0
        for height in range(img.size[1]):
            if width == 0 and img_data[width, img.size[1]-height - 1] != 255:
                break
            w +=  img_data[width, height]
        if w < 283333:
            left_to_remove = width
            break


    right_to_remove = 0
    for width in range(img.size[0]):
        w = 0
        for height in range(img.size[1]):
            w +=  img_data[img.size[0]-width - 1, img.size[1]-height - 1]
            if width == 0 and img_data[img.size[0]-width - 1, img.size[1]-height - 1] != 255:
                break
        if w < 283333:
            right_to_remove = width
            break

    top_to_remove = 0
    for height in range(img.size[1]):
        w = 0
        for width in range(img.size[0]):
            w +=  img_data[width, height]
            if height == 0 and img_data[width, height] != 255:
                print(img_data[width, height])
                break
        if w < 185000:
            top_to_remove = height
            break


    bottom_to_remove = 0
    for height in range(img.size[1]):
        w = 0
        for width in range(img.size[0]):
            w += img_data[width, img.size[1]-height - 1]
            if height == 0 and img_data[width, img.size[1]-height - 1] != 255:
                break
        if w < 185000:
            bottom_to_remove = height
            break


    img = img.crop((left_to_remove, 0, img.width, img.height-bottom_to_remove))
    img = img.crop((0, top_to_remove, img.width - right_to_remove, img.height))
    print(img.size)
    return img

def crop_left_right_rgb(img):
    left_to_remove = 0
    img_data = img.load()
   
    for width in range(img.size[0]):
        w = 0
        for height in range(img.size[1]):
            r,g,b = img_data[width, height]
            w += (r + g + b)
            if height == 0 and (r + g + b) != 765:
                break
        if w < 900000:
            left_to_remove = width
            break


    right_to_remove = 0
    for width in range(img.size[0]):
        w = 0
        for height in range(img.size[1]):
            r,g,b = img_data[img.size[0]-width - 1, img.size[1]-height - 1]
            w += (r + g + b)
            if width == 0 and (r + g + b) != 765:
                break
        print(w)
        if w < 900000:
            right_to_remove = width
            break

    top_to_remove = 0
    for height in range(img.size[1]):
        w = 0
        for width in range(img.size[0]):
            r,g,b = img_data[width, height]
            w += (r + g + b)
        if w < 450000:
            top_to_remove = height
            break
        


    bottom_to_remove = 0
    for height in range(img.size[1]):
        w = 0
        for width in range(img.size[0]):
            r,g,b = img_data[width, img.size[1]-height - 1]
            w += (r + g + b)
        if w < 450000:
            bottom_to_remove = height
            break


    img = img.crop((left_to_remove, 0, img.width, img.height-bottom_to_remove))
    img = img.crop((0, top_to_remove, img.width - right_to_remove, img.height)) 
    return img

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
if __name__ == "__main__":
    mask_non_colored_image()
