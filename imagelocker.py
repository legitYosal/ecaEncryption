from base import *
from random import seed, randint
from copy import copy
import cv2 as cv

def main():
    im = cv.imread('lena.gif', 0)
    print(im)



if __name__ == '__main__':
    main()
