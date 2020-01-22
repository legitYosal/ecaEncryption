from base import *
from random import seed, randint, choice
from copy import copy
import matplotlib.pyplot as plt
import numpy as np
import cv2

class ecacrypt:
    @staticmethod
    def __lockpixel(initstat, time, pixel):
        eca = ECARule42(initstat)
        for i in range(0, time + 1):
            pixel.bits = Pixel.xor(pixel, eca.current)
            eca.nextstat()
        return pixel

    @staticmethod
    def __unlockpixel(initstat, time, pixel):
        eca = ECARule42(initstat)
        for i in range(0, time + 1):
            eca.nextstat()
        for i in range(time + 1, Pixel.numbit):
            pixel.bits = Pixel.xor(pixel, eca.current)
            eca.nextstat()
        return pixel

    @staticmethod
    def decode(key, image):
        for row in range(len(image)):
            for colmn in range(len(image[0])):
                seed(key['Seed'] * row * colmn)
                depth = randint(0, Pixel.numbit)
                data = Pixel(image[row][colmn])
                image[row][colmn] = ecacrypt.__unlockpixel(key['InitState'], depth, data).tonumber()
        return image

    @staticmethod
    def encode(key, image): # image is of type cv2 imread
        for row in range(len(image)):
            for colmn in range(len(image[0])):
                seed(key['Seed'] * row * colmn)
                depth = randint(0, Pixel.numbit)
                data = Pixel(image[row][colmn])
                image[row][colmn] = ecacrypt.__lockpixel(key['InitState'], depth, data).tonumber()
        return image

def main():
    # generate random secret key
    attes = ECA42attractores().attractores
    secret_key = {'Rule':'Rule42', 'InitState':choice(choice(attes)), 'Seed':randint(10**10, 10**11 - 1)}
    for key in secret_key:
        if key == 'InitState':
            print(key, secret_key[key].tonumber())
        else:
            print(key, secret_key[key])

    im = cv2.imread('lena.png', 0)
    cv2.imshow('original picture', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # encode
    im = ecacrypt.encode(secret_key, im)
    cv2.imshow('encoded picture', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # decode

    im = ecacrypt.decode(secret_key, im)
    cv2.imshow('decoded picture', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
