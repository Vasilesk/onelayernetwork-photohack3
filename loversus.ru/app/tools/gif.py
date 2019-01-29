import cv2
import numpy as np
import sys
from skimage import io
import ssl
import imageio


def paste_img(background, img, mask):
    h, w, _ = background.shape
    overlay = background.copy()

    fx = h / img.shape[0]
    img = cv2.resize(img.copy(), (0,0), fx = fx, fy = fx)
    mask = cv2.resize(mask.copy(), (0,0), fx = fx, fy = fx)
    h1, w1, _ = img.shape

    x1 = min(max(w // 2 - w1//2, 0), w)
    x2 = min(max(x1 + w1,0), w)

    ind = mask != 0
    overlay[:,x1:x2][ind] = img[ind]


    return overlay

def overlay_images(background, lover_1, lover_2, mask_1, mask_2, dist_c = 100):
    h, w, _ = background.shape
    overlay = background.copy()

    h_0 = int(h*1)
    y = int(h*0.5)

    fx = h_0 / lover_1.shape[0]
    lover_1 = cv2.resize(lover_1.copy(), (0,0), fx = fx, fy = fx)
    mask_1 = cv2.resize(mask_1.copy(), (0,0), fx = fx, fy = fx)
    h1, w1, _ = lover_1.shape

    fx =  h_0 / lover_2.shape[0]
    lover_2 = cv2.resize(lover_2.copy(), (0,0), fx = fx, fy = fx)
    mask_2 = cv2.resize(mask_2.copy(), (0,0), fx = fx, fy = fx)
    h2, w2, _ = lover_2.shape

    point_1 = (int(w1*0.5),int(h1*0.5))
    point_2 = (int(w2*0.5),int(h2*0.5))


    x2 = min(max(w // 2 - dist_c + (w1 - point_1[0]),0), w)
    x1 = min(max(x2 - w1,0), w)
    y1 = min(max(y - point_1[1],0), h)
    y1_0 = max(point_1[1] - y, 0)
    y2 = min(max(y1 + h1 - y1_0,0),h)
    y2_0 = min(max(y1_0 + y2 - y1,0),h1)
    ind = mask_1[y1_0:y2_0,-(x2-x1):] != 0
    overlay[y1:y2,x1:x2][ind] = lover_1[y1_0:y2_0,-(x2-x1):][ind]


    x1 = min(max(w // 2 + dist_c - (w2 - point_2[0]),0), w)
    x2 = min(max(x1 + w2,0), w)
    y1 = min(max(y - point_2[1],0), h)
    y1_0 = max(point_2[1] - y, 0)
    y2 = min(max(y1 + h2 - y1_0,0),h)
    y2_0 =  min(max(y1_0 + y2 - y1,0),h2)
    ind = mask_2[y1_0:y2_0,:(x2-x1)] != 0
    overlay[y1:y2,x1:x2][ind] = lover_2[y1_0:y2_0,:(x2-x1)][ind]

    return overlay

def create_gif(background, lover_1, lover_2, vampire_2, mask_1, mask_2, mask_3, gif_path):
    h, w, _ = background.shape

    images = []
    n_steps = 15

    # white = np.full(background.shape, 255).astype(np.uint8)
    white = cv2.resize(cv2.imread("../static/texture.jpg"), (800,600))

    dists = (np.logspace(2, 3, num=n_steps)/1000 * w//2 + 200).astype(int) [::-1]


    for i in range(n_steps):
        img = overlay_images(background, lover_1, lover_2, mask_1, mask_2, dists[i])
        if i>7:
            alpha = 1 - (i - 7)/8
            img = cv2.addWeighted(img, alpha, white, 1 - alpha, 0)

        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


    # white = np.full(background.shape, 255).astype(np.uint8)
    white = cv2.resize(cv2.imread("../static/texture.jpg"), (800,600))

    # for i in range(4):
    #     images.append(cv2.addWeighted(images[-1], 0.5, white, 0.5, 0))

    for i in range(4):
        images.append(cv2.addWeighted(images[-1], 0.5, cv2.cvtColor(white, cv2.COLOR_BGR2RGB), 0.5, 0))

    img = paste_img(white, vampire_2, mask_3)

    for i in range(3):
        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    imageio.mimsave(gif_path, images, format='GIF')


def get_smart_point(image):
    return (image.shape[1] // 2, image.shape[0] // 2)

def get_offsets(height, image1, image1_mask, image2, image2_mask, base_offset=0.1):
    top1 = np.min(np.where(np.any(image1_mask > 0, axis=1))[0])
    smart1 = get_smart_point(image1)

    top2 = np.min(np.where(np.any(image2_mask > 0, axis=1))[0])
    smart2 = get_smart_point(image2)

    movie_line = base_offset * height + max(smart1 - top1, smart2 - top2)
    return movie_line, movie_line - smart1, movie_line - smart2


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

    # background = cv2.imread(forest)
    background = cv2.resize(cv2.imread(forest), (800,600))

    create_gif(background, lover_1, lover_2, vampire_2, mask_1, mask_2, mask_3, gif_path)

if __name__ == '__main__':
    gifer(sys.argv[1], sys.argv[2], sys.argv[3], 'forest.jpg', sys.argv[4])
