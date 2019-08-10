 
import cv2
import os
import shutil
import sys 

from PIL import Image
from pathlib import Path

#load dataset

dest = "tmp"

def resize(path_in_str, dest, nw, nh):
    dest = dest+"/NR_"+os.path.basename(path_in_str)
    # print( path_in_str, dest, nw, nh) 


    img = cv2.imread(path_in_str) 
    cv2.resize(img, ( nw, nh), interpolation = cv2.INTER_AREA)  
    # cv2.imshow("cropped", crop_img)
    
    cv2.imwrite( dest, img)


     



def load_datasets_dir( pathVar ):
    print(pathVar)
    global dest;
    
    # dest = os.path.dirname(pathVar)+"_copy"
    dest = pathVar+"_copy"
    try :
        os.mkdir( dest  )
    except :
        # print(NameError)
        rert=0
 

    pathlist = Path(pathVar).glob('**/*.jpg')
    nw = 0
    nh = 0
    ip = 0
    for path in pathlist:

        path_in_str = str(path)
        # print(path_in_str)

        # because path is object not string
        if(ip == 0):
            img = cv2.imread(path_in_str) 
            nh, nw, channels = img.shape

        ip +=1

        resize(path_in_str, dest, nw, nh)




def load_datasets(args):
    args = args[1:]

    global dest;
 
  

    for eachDir in args: 

        dataset=[]
        if(os.path.isdir(eachDir)):

            eachDir =  os.path.abspath(eachDir) 
            load_datasets_dir( eachDir  )  
        
            try :
                os.rename(eachDir, eachDir+".back")
                os.rename(dest, eachDir) 
            except :
                # print(NameError)
                rert=0
                      
        else :
            print("can't find dir : "+ eachDir)

  


# load_datasets( sys.argv )
