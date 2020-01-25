from base import *
from random import seed, randint, choice
from copy import copy
import matplotlib.pyplot as plt
import numpy as np
import cv2

class ecacrypt:
    @staticmethod
    def lockpixel(initstat, init, time, pixel):
        eca = ECARule42(initstat)
        for i in range(0, init):
            eca.nextstat()
        for i in range(0, time + 1):
            pixel.bits = Pixel.xor(pixel, eca.current)
            eca.nextstat()
        return pixel

    @staticmethod
    def unlockpixel(initstat, init, time, pixel):
        eca = ECARule42(initstat)
        for i in range(0, init):
            eca.nextstat()
        for i in range(0, time + 1):
            eca.nextstat()
        for i in range(time + 1, Pixel.numbit):
            pixel.bits = Pixel.xor(pixel, eca.current)
            eca.nextstat()
        return pixel

    @staticmethod
    def decode(key, image):
        print('** started decoding...')
        seed(key['Seed'])
        for row in range(len(image)):
            for colmn in range(len(image[0])):
                depth = randint(0, Pixel.numbit - 1)
                init = (row + colmn) % 8
                data = Pixel(image[row][colmn])
                image[row][colmn] = ecacrypt.unlockpixel(key['InitState'], init, depth, data).tonumber()
        return image

    @staticmethod
    def encode(key, image): # image is of type cv2 imread
        print('** started encoding...')
        seed(key['Seed'])
        for row in range(len(image)):
            for colmn in range(len(image[0])):
                depth = randint(0, Pixel.numbit - 1)
                init = (row + colmn) % 8
                data = Pixel(image[row][colmn])
                image[row][colmn] = ecacrypt.lockpixel(key['InitState'], init, depth, data).tonumber()
        return image


def mainrgb():
    # generate random secret key
    attes = ECA42attractores().attractores
    secret_key = {'Rule':'Rule42', 'InitState':None, 'Seed':randint(10**5, 10**6 - 1)}
    b_init = choice(choice(attes))
    g_init = choice(choice(attes))
    r_init = choice(choice(attes))
    b_init = Pixel(43)
    g_init = Pixel(27)
    r_init = Pixel(9)
    for key in secret_key:
        if key == 'InitState':
            pass
        else:
            print(key, secret_key[key])
    print('InitState for red ' , r_init.tonumber(), ' for green ', g_init.tonumber(), ' for blue ', b_init.tonumber())
    im = cv2.imread('lena_color.tiff', 1)
    b = im[:,:,0]
    g = im[:,:,1]
    r = im[:,:,2]
    en_im = copy(im)
    de_im = copy(im)

    # encode
    secret_key['InitState'] = b_init
    en_b = ecacrypt.encode(secret_key, copy(b))
    secret_key['InitState'] = g_init
    en_g = ecacrypt.encode(secret_key, copy(g))
    secret_key['InitState'] = r_init
    en_r = ecacrypt.encode(secret_key, copy(r))
    en_im[:,:,0] = en_b
    en_im[:,:,1] = en_g
    en_im[:,:,2] = en_r

    # decode
    secret_key['InitState'] = b_init
    de_b = ecacrypt.decode(secret_key, copy(en_b))
    secret_key['InitState'] = g_init
    de_g = ecacrypt.decode(secret_key, copy(en_g))
    secret_key['InitState'] = r_init
    de_r = ecacrypt.decode(secret_key, copy(en_r))
    de_im[:,:,0] = de_b
    de_im[:,:,1] = de_g
    de_im[:,:,2] = de_r

    cv2.imshow('original picture', im)
    cv2.imshow('encoded picture', en_im)
    cv2.imshow('decoded picture', de_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def main():
    # generate random secret key
    attes = ECA42attractores().attractores
    secret_key = {'Rule':'Rule42', 'InitState':choice(choice(attes)), 'Seed':randint(10**5, 10**6 - 1)}
    for key in secret_key:
        if key == 'InitState':
            print(key, secret_key[key].tonumber())
        else:
            print(key, secret_key[key])
    im = cv2.imread('lena.png', 0)
    en_im = copy(im)
    de_im = copy(im)

    # encode
    en_im = ecacrypt.encode(secret_key, copy(im))

    # decode
    de_im = ecacrypt.decode(secret_key, copy(en_im))

    cv2.imshow('original picture', im)
    cv2.imshow('encoded picture', en_im)
    cv2.imshow('decoded picture', de_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
