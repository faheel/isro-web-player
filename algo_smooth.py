from PIL import Image, ImageOps
import os
from dateutil.parser import *
from datetime import *
#from voxel_flow_train import train
#http://161.202.224.194:1111/tree
import shutil
months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
def crops(SRC, DEST, ids=[i for i in range(9)]):
    print(SRC, DEST)
    #print(ids)
    img = Image.open(SRC)
    cropped_img = img.crop((30, 80, 676, 726))
    
    margin  = ImageOps.expand(cropped_img,border=61,fill='black')
     
    z = 256
    a = 0 #to distinguish the 9 parts, used in filename
    names = []
    for i in range(0,3):
        for j in range(0,3):
            cropped_img = margin.crop((i*z + i, j*z + j, (i+1)*z + i, (j+1)*z + j))
            #cropped_img.show()
            name = os.path.join(DEST,os.path.basename(SRC)[:-4] +'_' + str(a) + '.jpg' )           
            if a in ids: 
                #cropped_img.show()           
                #print(name)
                cropped_img.save(name)
                names.append(os.path.basename(name))
                a += 1  
    return names

#pass the address for directory the image where predicted images are stored in src
def join_img(SRC_DIR, dnt):
    try:
        os.makedirs(SRC_DIR+'fd')
        os.makedirs(SRC_DIR+'fe')
        
    except:
        print('folders already exist')
    a = 0
    new = Image.new('RGB', (768,768))
    name = 'fd/xyz_'
    for i in range(0,700,256):
        for j in range(0,700,256):
            im = Image.open( SRC_DIR + name + str(a)+ '.png')
            new.paste(im, (i,j))
            a += 0
    
    new = new.crop((61,61,708,708))
    #change new to image name
    new.save(SRC_DIR + 'fe/' + dnt + '.png')
	
def smooth(src_dir='/home/huzaifa/sih/test_Data/'):
    global months
    times = []
    
    for img_name in os.listdir(src_dir):
        try:
            path = os.path.join(src_dir, img_name) 
            img = Image.open(path)
            tokens = img_name.split('_')
            hour = int(tokens[2][:2])
 
            minute = int(tokens[2][2:])
            #print(img_name)
            day = int(tokens[1][:2])
              
            year = int(tokens[1][5:])
            for i in range(12):
                 if months[i] in img_name:
                    month = i + 1
                    break
            parsed_date = parse('{0}-{1}-{2} {3}:{4}'.format(year, months[month-1],day, hour,minute))
            times.append([parsed_date, path])
              #print('2')
        except:
            pass
    times.sort(key=lambda x:x[0])
    for stime1, stime2 in zip(times, times[1:]):
        print(stime1[0].strftime('%Y-%m-%d %H:%M'))
        print(stime2[0].strftime('%Y-%m-%d %H:%M'))
      #print(stime3[0].strftime('%Y-%m-%d %H:%M'))
        if (stime2[0]-stime1[0]> timedelta(minutes=30)):
              
              try:
                os.makedirs(src_dir+'fc')
                os.makedirs(src_dir+'fb')
                #sleep(1)
              except:
                break
              
              try:
                 #print('ehllo')

                  crops(stime1[1], src_dir+'fb')
                  crops(stime2[1], src_dir+'fc')
                  pred_time = (stime2[0]-stime1[0])//2 + stime1[0]
                  
                  MONTH = months[(pred_time.month)-1]
                  output = '3DIMG_{1:02d}{2}{0}_{3:02d}{4:02d}_L1C_ASIA_MER_IR1.jpg'.format(pred_time.year, pred_time.day, MONTH, pred_time.hour, pred_time.minute)
                  join_img(src_dir, output)
	          #print(stime1[0] + timedelta(minutes=
                  break
              except Exception as e:
                  print(e)
                  shutil.rmtree(src_dir+'fc')
                  shutil.rmtree(src_dir+'fb')
        
                  


smooth()
