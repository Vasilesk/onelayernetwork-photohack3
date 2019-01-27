import cv2
import numpy as np
import sys
from utils import create_gif
from skimage import io
import ssl

def gifer(vampire, clean, vampirized, forest, out_path):
    ssl._create_default_https_context = ssl._create_unverified_context

    # biting vampire
    img = io.imread(vampire)
    lover_1 = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2RGB)
    mask_1 = cv2.threshold( cv2.cvtColor(img[:,:,3], cv2.COLOR_GRAY2RGB),127,255,cv2.THRESH_BINARY)[1]

    # person
    img = io.imread(clean)
    lover_2 = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2RGB)
    mask_2 = cv2.threshold( cv2.cvtColor(img[:,:,3], cv2.COLOR_GRAY2RGB),127,255,cv2.THRESH_BINARY)[1]

    # person became a vampire
    img = io.imread(vampirized)
    vampire_2 = cv2.cvtColor(img[:,:,:3], cv2.COLOR_BGR2RGB)
    mask_3 = cv2.threshold( cv2.cvtColor(img[:,:,3], cv2.COLOR_GRAY2RGB),127,255,cv2.THRESH_BINARY)[1]


    # path to save gif
    gif_path = out_path

    mask_1 = cv2.threshold(mask_1,127,255,cv2.THRESH_BINARY)[1]
    mask_2 = cv2.threshold(mask_2,127,255,cv2.THRESH_BINARY)[1]

    background = cv2.imread(forest)

    create_gif(background, lover_1, lover_2, vampire_2, mask_1, mask_2, mask_3, gif_path)

if __name__ == '__main__':
    gifer(sys.argv[1], sys.argv[2], sys.argv[3], 'forest.jpg', sys.argv[4])
