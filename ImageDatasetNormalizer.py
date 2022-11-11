from PIL import Image
from tqdm import tqdm
import os
import uuid

src = "./images"
dst = "./data/"

power = 8

print("Enter power of 2 to scale the image to")
print("i.e. 8 will produce 2^8 square images, or 256")
print("Default is 8")
power = int(input(">> "))

try:
    os.mkdir(dst)
    print("Made {}".format(dst))
except:
    pass


for each in tqdm(os.listdir(src)):
    ## Resize image to have a height of baseHeight
    base = 2 ** power
    png = Image.open(os.path.join(src,each))
    width, height = png.size

    ## Basing scale off smallest side stops black bars from appearing on the images
    if height <= width:
        ##Resize if height is smallest side
        hpercent = (base / float(png.size[1]))
        wsize = int((float(png.size[0]) * float(hpercent)))
        png = png.resize((wsize, base), Image.Resampling.LANCZOS)
    elif width < height:
        ##Resize if width is smallest side
        wpercent = (base / float(png.size[0]))
        hsize = int((float(png.size[1]) * float(wpercent)))
        png = png.resize((base, hsize), Image.Resampling.LANCZOS)

    ## Crop from center
    width, height = png.size
    left = (width - base)/2
    top = (height - base)/2
    right = (width + base)/2
    bottom = (height + base)/2

    png = png.crop((left, top, right, bottom))
    # print each
    if png.mode == 'RGBA':
        png.load() # required for png.split()
        background = Image.new("RGB", png.size, (0,0,0))
        background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
        background.save(os.path.join(dst,str(uuid.uuid4().hex) + '.jpg'), 'JPEG')
    else:
        png = png.convert('RGB')
        png.convert('RGB').save(os.path.join(dst,uuid.uuid4().hex) + '.jpg'), 'JPEG')