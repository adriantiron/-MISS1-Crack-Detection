import unittest
import keras.models, keras.layers
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np, glob
from PIL import Image


class TestStringMethods(unittest.TestCase):

    def test_glob(self):
        self.assertNotEqual(glob.glob('Images/*.jpg'), [], 'No images found in the "/Images" folder')

    def test_image_open(self):
        for filename in glob.glob('Images/*.jpg'):
            Image.open(filename)

    def test_image_format(self):
        for filename in glob.glob('Images/*'):
            img = Image.open(filename)
            self.assertEqual(img.format, "JPEG", 'File ' + filename + ' has incorrect format')

    def test_matching_set(self):
        i = 0
        for filename in glob.glob('Images/*jpg'):
            img = Image.open(filename)
            if i == 0:
                test_img = Image.open(filename)
                i += 1
            self.assertEqual(test_img.size, img.size, 'Images from different sets detected')


unittest.main()
