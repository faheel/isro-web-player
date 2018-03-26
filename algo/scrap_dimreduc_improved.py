import os
from PIL import Image, ImageOps

SRC_DIR = '/home/huzaifa/sih/data'
DEST_DIR = '/home/huzaifa/sih/padded_images'

try:
    os.mkdir(DEST_DIR)
except:
    print('folder exists')
    

for img_name in os.listdir(SRC_DIR):
    #print(img_name) 
    img = Image.open(os.path.join(SRC_DIR, img_name))
    cropped_img = img.crop((30, 80, 676, 726))
    margin  = ImageOps.expand(cropped_img,border=61,fill='black')
    
    z = 256
    a=0 #to distinguish the 9 parts, used in filename
    
    for i in range(0,3):
        for j in range(0,3):
            cropped_img = margin.crop((i*z + i, j*z + j, (i+1)*z + i, (j+1)*z + j))
            name = os.path.join(DEST_DIR, '{0}_{1}'.format(a, img_name))
            cropped_img.save(name)
            a += 1
   
