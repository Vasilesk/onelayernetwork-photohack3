import cv2
import numpy as np
import sys
from utils import create_gif
from skimage import io
import ssl


if __name__ == '__main__':
    
    ssl._create_default_https_context = ssl._create_unverified_context
    
    
    # biting vampire
    img = io.imread(sys.argv[1])
    lover_1 = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2RGB)
    mask_1 = cv2.threshold( cv2.cvtColor(img[:,:,3], cv2.COLOR_GRAY2RGB),127,255,cv2.THRESH_BINARY)[1]
    
    # person
    img = io.imread(sys.argv[2])
    lover_2 = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2RGB)
    mask_2 = cv2.threshold( cv2.cvtColor(img[:,:,3], cv2.COLOR_GRAY2RGB),127,255,cv2.THRESH_BINARY)[1]

    # person became a vampire
    img = io.imread(sys.argv[3])
    vampire_2 = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2RGB)
    mask_3 = cv2.threshold( cv2.cvtColor(img[:,:,3], cv2.COLOR_GRAY2RGB),127,255,cv2.THRESH_BINARY)[1]
    
    
    # path to save gif
    gif_path = sys.argv[4]
    
    mask_1 = cv2.threshold(mask_1,127,255,cv2.THRESH_BINARY)[1]
    mask_2 = cv2.threshold(mask_2,127,255,cv2.THRESH_BINARY)[1]

    background = cv2.imread('forest.jpg')

    create_gif(background, lover_1, lover_2, vampire_2, mask_1, mask_2, mask_3, gif_path)
