#Initializations
import os
import csv
import random
from PIL import Image, ImageOps
from datetime import datetime,date,timedelta
month_text=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
img_datetime = []

#Concerned Directories
src_dir = '/home/huzaifa/sih/data/together'
dest_dir = '/home/huzaifa/sih/dataset_final'

try:
    os.mkdir(dest_dir) 
except:
    pass
writer=csv.writer(open(os.path.join(dest_dir, 'lol.csv'),'w'))


#Loop for Date-Time Disintegration from filename and Storing it as a list
for img_name in sorted(os.listdir(src_dir)):
    if img_name.endswith(".jpg"):
        hour = int(img_name[16:18])
        minute = int(img_name[18:20])
        day = int(img_name[6:8])
        for i in range(12):
            if(month_text[i] == img_name[8:11]):
                month = i+1
                break
        year = int(img_name[11:15])
        img_datetime.append((year,month,day,hour,minute,img_name))
img_datetime = sorted(img_datetime)

#TimeStamp1 and TimeStamp2 explicit calculation
timestamp1=timestamp2=timestamp3=0
for i in range(2):
    timex = img_datetime[i]
    year,month,day,hour,minute = timex[0],timex[1],timex[2],timex[3],timex[4]
    img_dt = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + '-' + str(minute)
    if(i==0):
        timestamp1 = datetime.strptime(img_dt, "%Y-%m-%d-%H-%M")
    else:
        timestamp2 = datetime.strptime(img_dt, "%Y-%m-%d-%H-%M")

#Lower and Upper Bound of acceptable consecutive image time difference (tdelta)
lower_tdelta = timedelta(minutes=28)
upper_tdelta = timedelta(minutes=32)


#Function for Cropping image into 9 parts of size 256x256
def crops(SRC, DEST, ids):
    img = Image.open(SRC)
    cropped_img = img.crop((30, 80, 676, 726))
    margin  = ImageOps.expand(cropped_img,border=61,fill='black')
   
    z = 256
    a = 0 #to distinguish the 9 parts, used in filename
    names = []
    for i in range(0,3):
        for j in range(0,3):
                        
            cropped_img = margin.crop((i*z + i, j*z + j, (i+1)*z + i, (j+1)*z + j))
            name = os.path.join(DEST,str(a) + '_' + os.path.basename(SRC))           
            if a in ids:            
                cropped_img.save(name)
            names.append(os.path.basename(name))
            a += 1  
    return names
    

#Filtering out set of image triplet satisfying above criteria
for i in range(2,len(img_datetime),1):
    timex = img_datetime[i]
    year,month,day,hour,minute = timex[0],timex[1],timex[2],timex[3],timex[4]
    img_dt = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + '-' + str(minute)
    timestamp3 = datetime.strptime(img_dt, "%Y-%m-%d-%H-%M")
    tdelta1 = timestamp2 - timestamp1
    tdelta2 = timestamp3 - timestamp2
    if(tdelta1 >= lower_tdelta and tdelta1 <= upper_tdelta and tdelta2 >= lower_tdelta and tdelta2 <= upper_tdelta):
        x,y,z=img_datetime[i-2:i+1]

        ids = random.sample(range(9),3)
        crops(os.path.join(src_dir,x[5]), dest_dir, ids)                
        crops(os.path.join(src_dir,y[5]), dest_dir, ids)
        crops(os.path.join(src_dir,z[5]), dest_dir, ids)
        for i in ids:
            a = str(i) + '_'
            writer.writerow([a+str(x[5]),a+str(z[5]),a+str(y[5])])        
    timestamp1 = timestamp2
    timestamp2 = timestamp3

    if len(os.listdir(dest_dir)) > 10000:
        break
