import os
import argparse

import numpy as np
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", type=str, help="Image Path")
    parser.add_argument("--word", type=str, default='1024',
                        help="Sentence to show on Image")
    parser.add_argument('--width', type=int, default=100,
                        help='Width of the output (number of character per line).')
    parser.add_argument('--whratio', type=float, default=0.5,
                        help='width / height of one character.')
    parser.add_argument('--mode', type=str, choices=['raw', 'binary', 'morse', 'caesar'],
                        help='Whether use morse code to encry the word.', default='raw')

    args = parser.parse_args()
    return args


class DrawImage:
    def __init__(self, binary=True):
        args = get_args()
        img = self.read_img(args.img_path, args.width)

        str = self.transform(args.word, args.mode) if binary else args.word
        print('String is:', str)
        self.words = list('*'.join([str for _ in range(img.shape[0] * img.shape[1] // len(str))]))
        self.show(img)
        # print(img.shape, img)

    def read_img(self, img_path, target_w, whratio=0.5):
        img = Image.open(img_path)
        w, h = img.size
        w /= whratio
        resize = w / target_w
        img = img.resize((int(w / resize), int(h / resize)))

        img = np.array(img)
        if img_path.endswith('.png'):
            img = img[:, :, 3:4]

        return img

    @staticmethod
    def transform(str, mode):
        CODE = {'A': '.-', 'B': '-...', 'C': '-.-.',
                'D': '-..', 'E': '.', 'F': '..-.',
                'G': '--.', 'H': '....', 'I': '..',
                'J': '.---', 'K': '-.-', 'L': '.-..',
                'M': '--', 'N': '-.', 'O': '---',
                'P': '.--.', 'Q': '--.-', 'R': '.-.',
                'S': '...', 'T': '-', 'U': '..-',
                'V': '...-', 'W': '.--', 'X': '-..-',
                'Y': '-.--', 'Z': '--..',

                '0': '-----', '1': '.----', '2': '..---',
                '3': '...--', '4': '....-', '5': '.....',
                '6': '-....', '7': '--...', '8': '---..',
                '9': '----.'
                }
        if mode == 'binary':
            str = ''.join(format(ord(x), 'b') for x in str.upper())
        elif mode == 'morse':
            str = '*'.join(CODE[x] for x in str.upper() if x in CODE) + '*.-.-.'
            str = str.replace('.', '0')
            str = str.replace('-', '1')
        elif mode == 'caesar':
            kaisa = {chr(x): chr(x+1) for x in range(ord('A'), ord('Z'))}
            kaisa.update({'Z': 'AA'})
            str = '*'.join([CODE[kaisa[x] if ord('A') <= ord(x) <= ord('Z') else x]
                           for x in str.upper() if x in CODE]) + '*.-.-.'
            str = str.replace('.', '0')
            str = str.replace('-', '1')
        return str

    def show(self, img):
        img = img.sum(2)
        print(img.shape)
        shape = img.shape
        for i in range(shape[0]):
            tmp = [self.words.pop(0) if img[i, j] > 50 else ' ' for j in range(shape[1])]
            print(''.join(tmp))


if __name__ == '__main__':
    draw = DrawImage()
