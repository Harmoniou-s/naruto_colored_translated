import os
from os.path import expanduser
import zipfile
from PIL import Image

# i is the volume/chapter you are starting at, it is for naming purposes
VOLUME_START = 0
VOLUME_END = 72

#this will replace every cbz file with a zip or vise versa so it can be unzipped
def replace_extension(extension): 
    i=VOLUME_START
    for volume_name in os.listdir("./solution_zipped"):
        base = os.path.splitext(volume_name)[0]
        os.rename("./solution_zipped/" + volume_name, "./solution_zipped/VOL_" + str(i) + extension)
        i+=1
    i=VOLUME_START
    for volume_name in os.listdir("./solution_cbz"):
        base = os.path.splitext(volume_name)[0]
        os.rename("./solution_zipped/" + volume_name, "./solution_zipped/VOL_" + str(i) + extension)
        i+=1


#this zips or extracts all of the volume folders, this should be done after you have replace the extension from cbz to zip, I dont remember if this works or if I used winrar
def zip_extract_files(zip=False):
    type = "r"
    if zip:
        type = "w"
    for volume_name in os.listdir("./colored"):
        with zipfile.ZipFile("./colored/" + volume_name, type) as zip_ref:
            os.makedirs("./colored/" + volume_name.replace(".zip", ""))
            zip_ref.extractall("./colored/" + volume_name.replace(".zip", ""))
    
    for volume_name in os.listdir("./solution_zipped/"):
        with zipfile.ZipFile("./solution_zipped/" + volume_name, type) as zip_ref:
            os.makedirs("./solution_zipped/" + volume_name.replace(".zip", ""))
            zip_ref.extractall("./solution_zipped/" + volume_name.replace(".zip", ""))


#Renames all of the pages to be the same, 1 2 3 4 5 etc
def rename_pages():
    for volume_name in os.listdir("./colored"):
        
        i=1
        dir = "./colored/" + volume_name.replace(".zip", "") + "/"
        for page in os.listdir(dir):
            #this is for numbering the pages as 001 because sorting the pictures goes 1 10 11 12 2 20 normally
            pre = ""
            if i <100:
                pre = "0"
                if i < 10:
                    pre = "00"
            os.rename(dir + page, dir + pre + str(i) + ".jpg")
            i+=1
    
    j=VOLUME_START
    for volume_name in os.listdir("./non_colored"):
        1
        dir = "./non_colored/" + volume_name.replace(".zip", "") + "/Naruto v" + str(j) + "/"
        for page in os.listdir(dir):
            #this is for numbering the pages as 001 because sorting the pictures goes 1 10 11 12 2 20 normally
            pre = ""
            if i <100:
                pre = "0"
                if i < 10:
                    pre = "00"
            os.rename(dir + page, dir + pre + str(i) + ".jpg")
            i+=1
        j+=1


#Makes the completed Folders, this should be done first
def mk_dirs():
    for i in range(VOLUME_START, VOLUME_END):
        os.makedirs("./solution/VOL_" + str(i))


#This is to delete the 2nd and 3rd page from the colored version because they are not useful and it lets me align the pictures so that page 20 in the colored is page 20 in the uncolored
def del_extra():
    j=VOLUME_START
    for volume_name in os.listdir("./non_colored"):
        dir = "./non_colored/" + volume_name.replace(".zip", "") + "/Naruto v" + str(j) + "/"
        pages = os.listdir(dir)
        #1 is the second page, Arrays in coding languages start at 0. 
        #pages[1] = page 2
        os.remove(dir + pages[1])
        os.remove(dir + pages[2])
        j+=1


#this combines the images into 1 image with colored on left, uncolored on right
def combine_images():
    j=VOLUME_START
    for dirname in os.listdir("./colored"):
        for page in os.listdir("./colored/" + dirname):
            img1 = Image.open("./colored/" + dirname + "/" + page)
            try:
                #You normally wont have to do this, im too lazy to pull all the pictures out into their volume forlder, so I leave them in the "naruto v" folder inside the VOL_ folder
                img2 = Image.open("./non_colored/" + dirname + "/Naruto v" + str(j) + "/" + page)
                img2 = img2.resize(img1.size)
                img3 = Image.new("RGB", (img1.size[0] + img2.size[0], min(img1.size[1], img2.size[1])), color="white")
                img3.paste(img1, (0,0))
                img3.paste(img2, (img1.size[0], 0))
                img3.save('./solution/'+ dirname + "/" + os.path.basename(img1.filename))
            except:
                continue
        print("Volume " + str(j) + " Done")
        j+=1
        


#change the functions around here, remove the # to use it
if __name__ == "__main__":
    mk_dirs()
    replace_extension(".zip")
    zip_extract_files()
    rename_pages()
    #only use below if you edited it to whatever you need
    #del_extra()
    combine_images()
    zip_extract_files(True)