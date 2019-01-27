import cv2
import numpy as np
import sys
from utils import create_gif

if __name__ == '__main__':
    
    # biting vampire
    lover_1 = cv2.imread(sys.argv[1])
    
    # person
    lover_2 = cv2.imread(sys.argv[2])
    
    # person became a vampire
    vampire_2 = cv2.imread(sys.argv[3])
    
    # mask of first vampire
    mask_1 = cv2.imread(sys.argv[4])
    
    # mask of new vampire
    mask_2 = cv2.imread(sys.argv[5])
    
    # path to save gif
    gif_path = sys.argv[6]
    
    mask_1 = cv2.threshold(mask_1,127,255,cv2.THRESH_BINARY)[1]
    mask_2 = cv2.threshold(mask_2,127,255,cv2.THRESH_BINARY)[1]

    background = cv2.imread('forest.jpg')

    create_gif(background, lover_1, lover_2, vampire_2, mask_1, mask_2, gif_path)
