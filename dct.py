from scipy.fftpack import dct, idct
import skimage.util
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import bitstring
from helpers import dct2, idct2, embed_message, get_embedded_message, stitch


# IMAGE SAVED IN AC COMPONENTS

# QUANTIZATION TABLE from wikipedia
QUANTIZATION_TABLE = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                               [12, 12, 14, 19, 26, 58, 60, 55],
                               [14, 13, 16, 24, 40, 57, 69, 56],
                               [14, 17, 22, 29, 51, 87, 80, 62],
                               [18, 22, 37, 56, 68, 109, 103, 77],
                               [24, 35, 55, 64, 81, 104, 113, 92],
                               [49, 64, 78, 87, 103, 121, 120, 101],
                               [72, 92, 95, 98, 112, 100, 103, 99]], dtype=np.float32)


# ------------ HELPERS ------------


# ----- DCT CLASS

class DCT:
    def encode(self, image, SECRET_MESSAGE):
        # get image as YCbCr
        img = Image.open(image)
        img = np.array(img)
        img_original = np.array(Image.open(image))
        
        # get dimensions of image
        c, r, _ = img.shape  # shape: columns x rows x channels where channel 0 is luminance (R)

        # get Red color channel
        B = img[:,:,2]

        # get 8x8 blocks
        B_blocks = skimage.util.view_as_blocks(B, block_shape=(8, 8))

        # shift values form a positiva range to one centered on zero
        B_blocks = B_blocks - 128

        # perform DCT on blocks
        dct_blocks_B = dct2(B_blocks)

        # quantization
        dct_blocks_B = np.int32(np.around(dct_blocks_B / QUANTIZATION_TABLE))

        # embed data in luminance layer
        secret_data = ""
        for char in SECRET_MESSAGE.encode('ascii'):
            secret_data += bitstring.pack('uint:8', char)

        embedded_blocks = embed_message(secret_data, np.int32(dct_blocks_B))

        var0 = get_embedded_message(embedded_blocks) # test if embedding was succesful

        # idct
        idct_blocks_B = idct2(embedded_blocks)

        # stitch 8x8 block into one array
        B_stitch = stitch(idct_blocks_B, c, r)

        # insert new blue color layer into image
        img[:, :, 2] = B_stitch

        return img, img_original, var0


    def decode(self, image):

        # Read image
        img = Image.open(image)
        img = np.array(img)

        # get dimensions of image
        c, r, _ = img.shape

        B = img[:, :, 2]

        # get 8x8 blocks
        B_blocks = skimage.util.view_as_blocks(B, block_shape=(8, 8))

        # shift values form a positive range to one centered on zero
        dct_blocks_B = np.around(dct2(B_blocks))


        # get message from image
        message = get_embedded_message(dct_blocks_B)

        # inverse DCT
        idct_blocks_B = idct2(dct_blocks_B)

        # stitch 8x8 block into one array
        B_stitch = stitch(idct_blocks_B, c, r)

        # insert new luminance layer into image
        img[:, :, 2] = B_stitch


        return message, img

# EoF


