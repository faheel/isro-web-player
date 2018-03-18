import wget
from tqdm import tqdm

YEAR = '2018'
MONTH = 'JAN'


for date in tqdm(range(1, 31)):
    hour = 0
    minute = 00
    while(1):
        #print('DATE:{0:02d} TIME:{1:02d}{2:02d} '.format(date, hour, minute))
        
        url = 'https://www.mosdac.gov.in/data/servlet/Image?image=preview&loc=/web/mosdac_preview/3D_IMG/preview/{0}/{1:02d}{2}/3DIMG_{1:02d}{2}{0}_{3:02d}{4:02d}_L1C_ASIA_MER_IR1.jpg'.format(YEAR, date, MONTH, hour, minute)
        #print(url)
        minute += 30
        if minute >= 60:
            hour += 1
            minute %= 60
        
        if hour >= 24:
            break
        
        #time.sleep(1)
        try:
            path = '/home/huzaifa/sih/data/sih/'
            output = '3DIMG_{1:02d}{2}{0}_{3:02d}{4:02d}_L1C_ASIA_MER_IR1.jpg'.format(YEAR, date, MONTH, hour, minute)
            filename = wget.download(url, out=path+output)
        except:
            pass