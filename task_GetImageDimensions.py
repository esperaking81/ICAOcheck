import os
import cv2

dir = os.path.dirname(os.path.realpath(__file__)) + '/subjects/'

for name in os.listdir(dir):
    if not '.jpg' in name:
        continue 

    try:
        print(f'>>> {name}')

        im = cv2.imread(f"{dir}{name}", 0)

        h, w = im.shape

        print('width:  ', w)
        print('height: ', h)
    except Exception as e:
        continue
