from PIL import Image
a = 0
#change the address to folder where predicted images are kept
src = '/home/kzk077/Desktop/images/index_'

new = Image.new('RGB', (768,768))

#will not be used in actual script
im = Image.open('/home/kzk077/Desktop/images/github-256.png')



#in the loop write path for first image in terms of a so that it can be incremented
for i in range(0,700,256):
    for j in range(0,700,256):
        #open image here
        #im = Image.open(src + str(a) + '.png')
        new.paste(im, (i,j))
        a += 0
        new.show()

#change new to image name
new.save(src + 'new.png') 
