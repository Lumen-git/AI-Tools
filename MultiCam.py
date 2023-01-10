import cv2 as cv
import time
import os
import uuid

vers = 1.1

print('''                                   
 _____     _ _   _ _____           
|     |_ _| | |_|_|     |___ _____ 
| | | | | | |  _| |   --| .'|     |
|_|_|_|___|_|_| |_|_____|__,|_|_|_| 
                           by lumen''')


print("\nLoading configs and camera...")
# Configs
cam_port = 0                #Change this if you have multiple cameras
multishot = 8               #Change this if multiple shots of the same image
delay = 1.875                #Delay of the images above, in seconds
storage = "./multicam/"     #Root of storage
setUUID = True              #If true, images will have UUID rather than names

# Make Storage
try:
    os.mkdir(storage)
except:
    pass

# Init camera
try:
    cam = cv.VideoCapture(cam_port)
except:
    print("Error: Camera Could not open")
    input("Press enter to exit")
    exit()

print("\n")

# Get image settings
settings_set = "n"
label = ""
batches = 1
iterations = 1
print(f"Welcome to the MultiCam dataset utility tool, version {vers}")

print("\n")
print("Now configuring labels, batches, and iterations")
print("Label: Determines the file name of each image")
print("Batches: First level of separation, think of this as number of objects")
print("Iterations: Second level of separation, think of this as number of photos of each object")
print("Each photo is saved as label-batch#-iteration#")
print("For example, taking a photo of both sides of 6 coins would be 6 batches, 2 iterations")
print("(6 objects, 2 photos of each, 12 photos total)")
print("\n")


while settings_set != "y":
    label = input("Enter label: ")
    batches = int(input("Enter number of batches: "))
    iterations = int(input("Enter number of iterations: "))
    predicted = iterations*multishot*batches
    failed = 0
    print("\n")
    print(f"These settings with produce {iterations*multishot} pictures of {batches} batches, for a total of {predicted} pictures")
    print("If these settings look incorrect, view the configurations at the top of the code or try again")
    settings_set = input("Continue with these settings? (y/n): ")

# Cam Test

print("MultiCam will now show a live preview of the camera. Align the object and camera properly")
print("then hit escape on the preview window\n")

width = int(cam.get(3))
height = int(cam.get(4))

cv.namedWindow("preview")

if cam.isOpened(): # try to get the first frame
    rval, frame = cam.read()
else:
    rval = False

while rval:
    cv.line(frame, pt1=(0,int(height/2)), pt2=(width,int(height/2)), color=(0,255,0), thickness=1)
    cv.line(frame, pt1=(int(width/2),0), pt2=(int(width/2),height), color=(0,255,0), thickness=1)
    cv.imshow("preview", frame)
    rval, frame = cam.read()
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break

cam.release()
cv.destroyWindow("preview")

# Cycle

print("\nMultiCam will now start taking photos. There will be a pause between each iteration to adjust the object.")
input("Press enter to take the first photo of batch 1...\n")

cam = cv.VideoCapture(cam_port)

for z in range(batches):
    for y in range(iterations):
        # This x loop represents, usually, 1 photo
        # If multishot is enabled (>1), it will take multiple photos in one go
        for x in range(multishot):
            result, image = cam.read()

            if result:
                if setUUID == False:
                    if (multishot == 1): cv.imwrite(f"{storage}{label}{z}-{y}.png", image)
                    else: cv.imwrite(f"{storage}{label}{z}-{y}-{x}.png", image)
                else:
                    try:
                        fullPath = storage + "/" + label + "/"
                        os.mkdir(fullPath)
                    except:
                        pass
                    cv.imwrite(f"{fullPath}{uuid.uuid4()}.png", image)
            else:
                print(f"Failed to capture image")
                failed += 1

            time.sleep(delay)

        if (y != iterations-1): input("Click! Press enter for next photo...")
    if (z != batches-1):  input(f"End of batch {z+1}, press enter for first photo of next batch ")

print(f"Finished taking {predicted-failed} photos, with {failed} photos failed!")
input("Press enter to exit MultiCam")
exit()
