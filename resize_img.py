from PIL import Image
import os
import shutil
import sys


basewidth = 720
baseheight = 540
path = sys.argv[1]

if path[-1] != os.path.sep:
    path += os.path.sep
for filename in os.listdir(path):
    if not os.path.isdir(os.path.join(path, filename)):
        base, extension = os.path.splitext(filename)
        old_name = os.path.join(path, filename)
        new_name = os.path.join(path, base + "_resized" + extension)

        if extension == ".txt":
            shutil.copy(old_name, new_name)
        else:
            img = Image.open(path + filename)
            widht = img.size[0]
            height = img.size[1]
            wpercent = (basewidth/float(widht))
            hsize = int((float(height)*float(wpercent)))
            img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
            img.save(new_name)
            print(new_name + ' - ok!')

