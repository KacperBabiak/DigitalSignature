import random
import this
from typing_extensions import Self
import numpy as np
from sympy import public
from scipy.stats import entropy
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import struct
import os



class Generator:
    globalCounter=0
    globalArray=[]
    
    #///////screenshoty stron//////////////////////////////
    def screenshot():  

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        #screenshoting and saving photos
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)
        
        
        driver.get('https://sdzwildlifeexplorers.org/videos/livecam/elephant-cam')
        #sleep(1)

        for i in range(100):
            driver.get_screenshot_as_file('C:/Users/kacpe/OneDrive/Pulpit/projekt/screenshot{}.png'.format(i))
            #sleep(1)
        

        driver.quit()
        print("end...")

    def deleteScreenshots():
        #deleting photos
        for i in range(100):
            os.remove('C:/Users/kacpe/OneDrive/Pulpit/projekt/screenshot{}.png'.format(i)) 



    def block_view(A, block):
    # Reshape the array into a 2D array of 2D blocks, with the resulting axes in the
    # order of:
    #    block row number, pixel row number, block column number, pixel column number
    # And then rearrange the axes so that they are in the order:
    #    block row number, block column number, pixel row number, pixel column number
        return A.reshape(A.shape[0]//block[0], block[0], A.shape[1]//block[1], block[1])\
                .transpose(0, 2, 1, 3)
    
    def bits2int(a, axis=-1):
        return np.right_shift(np.packbits(a, axis=axis), 8 - a.shape[axis]).squeeze()


    def binarize(image):
        #histogram before postprocessing
        imArr = np.array(image)
        vals = imArr.mean(axis=2).flatten()

        #///////////////////////////////////////////////////NA SZARO
        imageAfter = image.convert('L')

        #////////////////////////////////////////////////ZBINARYZWOAC
       
        bw = imageAfter.point(lambda x: 0 if x<128 else 255, '1')  #binarization
        

        return bw

    def arnoldsCat(bw):
        #/////////////////////////////////////////////KOTEK
        # load image
        im = np.array(bw)
        N = im.shape[0]

        # create x and y components of Arnold's cat mapping
        x,y = np.meshgrid(range(N),range(N))
        xmap = (2*x+y) % N
        ymap = (x+y) % N

        for i in range(8):
            result = Image.fromarray(im)
            im = im[xmap,ymap]

        return result

    def postprocessing(result):
        #//////////////////////////////STEP 4


        result_pixels=np.asarray(result)

        # Boolean array where value is True if corresponding pixel in `image` is
        # "black" (intensity less than 0.5)
        image_bin = result_pixels < 0.5

        # Create a 2D array view of 4x4 blocks
        a = Generator.block_view(image_bin, (4, 4))

        # XOR reduce each 4x4 block (i.e. reduce over last two axis), so even number
        # of blacks is 0, else 1
        a = np.bitwise_xor.reduce(a, axis=(-2, -1))

        #print(a)


        #/////////////////////////zygzag
        zig_zag_a=np.concatenate([np.diagonal(a[::-1,:], i)[::(2*(i % 2)-1)] for i in range(1-a.shape[0], a.shape[0])])
        zig_zag = np.multiply(zig_zag_a, 1) #zmiana na 0 i 1


        res=np.split(zig_zag,2048)

        result=[]
        for i in res:
            result.append(Generator.bits2int(i))


        return result



        


    def randomBits():
        sum=[]

        #cropping and openig photos
        for i in range(100):
            image = Image.open('C:/Users/kacpe/OneDrive/Pulpit/projekt/screenshot{}.png'.format(i))

            width,height = image.size

            left = width/3
            top = height/3
            right = left+512
            bottom = top+512

            image = image.crop((left, top, right, bottom))
            #image.show()

            bw = Generator.binarize(image)
            ac = Generator.arnoldsCat(bw)
            pp = Generator.postprocessing(ac)
            sum=sum+pp

        sum=np.stack(sum)
        #x=sum.item(0)
        return sum


    def int_to_bytes(x: int) -> bytes:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')



    #rozpoczyna prace, robi screeny i je przetwarza
    def startGen():
        Generator.screenshot()
        this.globalArray =Generator.randomBits()
        this.globalCounter =2
        print("arraySize= ",len(this.globalArray))

        
        

    def oneRandomBitLoop(n):
        

        #czy wycinek tabeli wykracza poza długość, jesli tak, nowe screeny
        if((this.globalCounter+n)>len(this.globalArray)):
            Generator.startGen()
        
        #wycinek
        array = this.globalArray[this.globalCounter:(this.globalCounter+n)]
        this.globalCounter=this.globalCounter+n

        arrayOfBytes=[]

        #counter=0
        for x in array:
            
            arrayOfBytes.append(x)
           

        #Generator.delete_screenshot()
        byte_array = bytearray(arrayOfBytes)
        print(int.from_bytes(bytes(byte_array),'little'))
        return byte_array
            

        
        