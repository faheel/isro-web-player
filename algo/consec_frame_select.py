import os
import csv
from PIL import Image, ImageOps
from datetime import datetime,date,timedelta
writer=csv.writer(open('consecutive_timestamp_triplets.csv','w'))
month_text=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
img_datetime = []

#Loop for Date-Time Disintegration from filename and Storing it as a list

def crops(SRC, DEST_DIR):
    img = Image.open(SRC)
    cropped_img = img.crop((30, 80, 676, 726))
    margin  = ImageOps.expand(cropped_img,border=61,fill='black')
   
    z = 256
    a = 0 #to distinguish the 9 parts, used in filename
    names = []
    for i in range(0,3):
        for j in range(0,3):
            cropped_img = margin.crop((i*z + i, j*z + j, (i+1)*z + i, (j+1)*z + j))
            name = os.path.join(DEST_DIR, os.path.basename(SRC))
            name = str(a) + '_' + name             
            cropped_img.save(name)
            names.append(os.path.basename(name))
    
    return names
    

def do_stuff(src_dir, dst_dir):
    
    try:
        os.mkdir(dst_dir)    
    except:
        pass
    
    for img_name in sorted(os.listdir(src_dir)):
        if img_name.endswith(".jpg"):
            tokens = img_name.split('_')
            hour = int(tokens[2][:2])
            minute = int(tokens[2][2:]])
            day = int(tokens[1][:2])
            
            for i in xrange(12):
                if month_text[i] in img_name:
                    month = i+1
                    break
            
            year = int(tokens[1][5:])
            img_datetime.append((year,month,day,hour,minute,img_name))
    
    img_datetime = sorted(img_datetime)
    
    #TimeStamp1 and TimeStamp2 explicit calculation
    
    timestamp1=timestamp2=timestamp3=0
    
    for i in xrange(2):
        year,month,day,hour,minute = img_datetime[i][0],img_datetime[i][1],img_datetime[i][2],img_datetime[i][3],img_datetime[i][4]
        img_dt = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + '-' + str(minute)
        if(i==0):
            timestamp1 = datetime.strptime(img_dt, "%Y-%m-%d-%H-%M")
        else:
            timestamp2 = datetime.strptime(img_dt, "%Y-%m-%d-%H-%M")
    
    #Lower and Upper Bound of acceptable consecutive image time difference (tdelta)
    lower_tdelta = timedelta(minutes=28)
    upper_tdelta = timedelta(minutes=32)
    
    #Filtering out set of image triplet satisfying above criteria
    for i in xrange(2,len(img_datetime),1):
        year,month,day,hour,minute = img_datetime[i][0],img_datetime[i][1],img_datetime[i][2],img_datetime[i][3],img_datetime[i][4]
        img_dt = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + '-' + str(minute)
        timestamp3 = datetime.strptime(img_dt, "%Y-%m-%d-%H-%M")
        tdelta1 = timestamp2 - timestamp1
        tdelta2 = timestamp3 - timestamp2
        
        if(tdelta1 >= lower_tdelta and tdelta1 <= upper_tdelta and tdelta2 >= lower_tdelta and tdelta2 <= upper_tdelta):

            x,y,z=img_datetime[i-2:i+1]
            crops(os.path.join(src_dir,x[5]), dst_dir)                
            crops(os.path.join(src_dir,y[5]), dst_dir)
            crops(os.path.join(src_dir,z[5]), dst_dir)
            
            for i in range(9):
                a = str(i) + '_'
                writer.writerow([a+x,a+z,a+y])
        timestamp1 = timestamp2
        timestamp2 = timestamp3
