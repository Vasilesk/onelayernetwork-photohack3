import cv2
import numpy as np
import sys
from utils import create_gif

if __name__ == '__main__':
    
    lover_1 = cv2.imread(sys.argv[1])
    lover_2 = cv2.imread(sys.argv[2])
    mask_1 = cv2.imread(sys.argv[3])
    mask_2 = cv2.imread(sys.argv[4])
    
    gif_path = sys.argv[5]
    
    mask_1 = cv2.threshold(mask_1,127,255,cv2.THRESH_BINARY)[1]
    mask_2 = cv2.threshold(mask_2,127,255,cv2.THRESH_BINARY)[1]

    background = cv2.imread('forest.jpg')

    create_gif(background, lover_1, lover_2, mask_1, mask_2, gif_path)
