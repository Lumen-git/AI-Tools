#Imports
from PIL import Image
from tqdm import tqdm
import os
import uuid

#Source and destinations, can be changed here
src = "./images"
dst = "./data/"
dstTrain = "./data/train/"
dstTest = "./data/test/"

#Var setup
convertWidth = 0
convertHeight = 0
testSplitPercent = 0

#Simple UI
convertWidth = int(input("Enter Width: "))
convertHeight = int(input("Enter Height: "))
testSplitPercent = float(input("Enter percentage to separate as testing data: "))

#Make folders
if (testSplitPercent == 0):
    try:
        os.mkdir(dst)
        print("Made {}".format(dst))
    except:
        pass
else:
    try:
        os.mkdir(dst)
        print("Made {}".format(dst))
        os.mkdir(dstTrain)
        print("Made {}".format(dstTrain))
        os.mkdir(dstTest)
        print("Made {}".format(dstTest))
    except:
        pass


#Maths for file split (if needed)
totalItems = len(os.listdir(src))
print(f"{totalItems} images found")

percent = 0
moveForTest = 0
counter = 0
if (testSplitPercent != 0):
    if testSplitPercent <= 1:
        percent = testSplitPercent
    else:
        percent = testSplitPercent / 100
    moveForTest = int(totalItems * percent)
    everyNth = int(totalItems / moveForTest)


for each in tqdm(os.listdir(src)):
    if (".DS_Store" in each): continue
    ## Resize image to have a height of convertHeight
    png = Image.open(os.path.join(src,each))
    width, height = png.size

    ## Basing scale off smallest side stops black bars from appearing on the images
    if height <= width:
        ##Resize if height is smallest side
        hpercent = (convertHeight / float(png.size[1]))
        wsize = int((float(png.size[0]) * float(hpercent)))
        png = png.resize((wsize, convertHeight), Image.Resampling.LANCZOS)
    elif width < height:
        ##Resize if width is smallest side
        wpercent = (convertWidth / float(png.size[0]))
        hsize = int((float(png.size[1]) * float(wpercent)))
        png = png.resize((convertWidth, hsize), Image.Resampling.LANCZOS)

    ## Crop from center
    width, height = png.size
    left = (width - convertWidth)/2
    top = (height - convertHeight)/2
    right = (width + convertWidth)/2
    bottom = (height + convertHeight)/2

    png = png.crop((left, top, right, bottom))

    ##save each
    if (testSplitPercent == 0):
        if png.mode == 'RGBA':
            png.load() # required for png.split()
            background = Image.new("RGB", png.size, (0,0,0))
            background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
            background.save(os.path.join(dst,str(uuid.uuid4().hex) + '.jpg'), 'JPEG')
        else:
            png = png.convert('RGB')
            png.convert('RGB').save(os.path.join(dst,uuid.uuid4().hex) + '.jpg', 'JPEG')
    else:
        if (counter == everyNth):
            saveTo = dstTest
            counter = 0
        else:
            saveTo = dstTrain
            counter += 1
        if png.mode == 'RGBA':
            png.load() # required for png.split()
            background = Image.new("RGB", png.size, (0,0,0))
            background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
            background.save(os.path.join(saveTo,str(uuid.uuid4().hex) + '.jpg'), 'JPEG')
        else:
            png = png.convert('RGB')
            png.convert('RGB').save(os.path.join(saveTo,uuid.uuid4().hex) + '.jpg', 'JPEG')
