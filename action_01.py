import cv2
import os
import sys 
import data_resize as dr
 



g_width = 64
g_heigth = 64

padding_t =20
padding_r = 20
padding_b = 20
padding_l = 20






image_id_from = 0

t_p_dir = [
    [
        [1,2],  [1,3], [1,4], [1,5], [1,6], [1,7], [1,8], [2,1], [2,2], [2,3]
    ],
    [
        [5,2],  [5,3], [5,4], [5,5], [5,6], [5,7], [5,8], [6,1], [6,2], [6,3]
    ],
    [
        [9,2],  [9,3], [9,4], [9,5], [9,6], [9,7], [9,8], [10,1], [10,2], [10,3]
    ]
]

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
  
    if width is None and height is None:
        return image 
    if width is None: 
        r = height / float(h)
        dim = (int(w * r), height)
 
    else: 
        r = width / float(w)
        dim = (width, int(h * r))
 
    resized = cv2.resize(image, dim, interpolation = inter)
 
    return resized


def crop_single_image (path, x, y, w, h, output):
    x= int(x)
    y= int(y)
    w= int(w)
    h= int(h)
    global padding_t, padding_r, padding_b, padding_l

    x+=padding_l
    y+=padding_t
    w-=padding_r
    h-=padding_b
     

    img = cv2.imread(path)
    crop_img = img[y:y+h, x:x+w]
    crop_img = image_resize(crop_img, g_width, g_heigth, cv2.INTER_AREA)
    # cv2.imshow("cropped", crop_img)
    cv2.imwrite(output, crop_img)

def get_sub_dir_name (output, image_id_from, eachxrc, eachcc) :
    global t_p_dir
    ch="A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z".split(",")

    yescreate = 0
    actualPath = "";
    dir_b = "/"
    dir_c = "/" 
    dir_b_id = 0
    dir_c_id = 'A'
    for aa in t_p_dir:  
        tmparr = 0;
        for ab in aa:  
            # print(ab, [eachxrc, eachcc], (ab == [eachxrc, eachcc]))
            if(ab == [eachxrc, eachcc]):  
                dir_c_id = ch[tmparr]   
                yescreate =1
            tmparr+=1
        if(yescreate):
            dir_b_id+=1


    dir_b = "data"+str(dir_b_id)+"/"
    dir_c = str(dir_c_id)+"/" 
    actDir = output+dir_b+dir_c
    try:
        if(yescreate):
            os.makedirs(actDir)
    except:
        rt = 0

    actualPath = actDir+str(image_id_from) + str( eachxrc ) + str( eachcc )+".jpg"
     

    return yescreate, actualPath;

def image_shape_calu (path, r, c, output) :
    global image_id_from
    try :
        os.mkdir( output  )
    except:
        rert=0
        # print("\r mkdir error, may already exists!! ["+output+" ]")


    img = cv2.imread(path)
    
    height, width, channels = img.shape

    each_height = height / r
    each_width = width / c

    x=0
    y=0
    for eachxrc in range(0, r): 
        for eachcc in range(0, c):
            yescreate, tmp_op_name = get_sub_dir_name(output, image_id_from, eachxrc+1, eachcc+1 )
            # print(x, y, each_width, each_height, tmp_op_name)
            if(yescreate):
                crop_single_image (path, x, y, each_width, each_height, tmp_op_name)
            x+=each_width 
        x=0
        y+=each_height 
    image_id_from+=1 



def collect_images_dir (path, r, c, output) :
    images = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                images.append(os.path.join(root, file))

    
    for eachImage in images: 
        image_shape_calu (eachImage, r, c, output)




dr.load_datasets( sys.argv )

 

oldpath = "data/"

if len(sys.argv) > 1:
    oldpath = sys.argv[1]
else: 
	oldpath=input("Enter path ")

if len(oldpath) <= 1:
	print("invalid input \n")
	exit()

path = os.path.abspath(oldpath)
r=12
c=8 
image_id_from = 0

output="tmp_data_output/"

 
collect_images_dir (path, r, c, output) 
print("\r process completed path : " + os.path.abspath(output))

