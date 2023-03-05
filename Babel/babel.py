#Babel 1.0
#Lumen

import os
import uuid
import hashlib
from tqdm import tqdm

def file_hash(file_path):
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536) # arbitrary number to reduce RAM usage
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()



print("BABEL, by Lumen")
print("-------------------------\n")

path = input("Enter Path: ")

print("\n-------------------------\n")

dest = input("Enter destination: ")

print("\n-------------------------\n")

print("""1: Series
2: UUID
3: Hash (sha256)\n""")

print("-------------------------\n")

mode = int(input("Enter mode: "))

print("\n-------------------------\n")

try:
    os.mkdir(dest)
    print("Made {}".format(dest))
except:
    pass

totalItems = os.listdir(path)
print(f"{len(totalItems)} images found")

if (mode == 1):
    i = 0
    for each in tqdm(totalItems):
        filename, file_extension = os.path.splitext(each)
        new_file = os.path.join(dest, str(i) + file_extension)
        os.rename(path + "\\" + each, new_file)
        i += 1

if (mode == 2):
    for each in tqdm(totalItems):
        filename, file_extension = os.path.splitext(each)
        new_file = os.path.join(dest, str(uuid.uuid4()) + file_extension)
        os.rename(path + "\\" + each, new_file)

if (mode == 3):
    for each in tqdm(totalItems):
        myHash = file_hash(path + "\\" + each)

        filename, file_extension = os.path.splitext(each)
        new_file = os.path.join(dest, str(myHash) + file_extension)
        try:
            os.rename(path + "\\" + each, new_file)
        except:
            print(f"Possible duplicate of {myHash}")