from scipy.fftpack import dct, idct
import numpy as np
from PIL import Image
import bitstring
from PIL import Image
    
    
# ----- DCT HELPERS

# implement 2D DCT
def dct2(a):
    return dct(dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


# implement 2D IDCT
def idct2(a):
    return idct(idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


# resizing img to make the r and c divisable by 8
def resize_img(img, r, c):
    img = img.resize((c + (8 - c % 8), r + (8 - r % 8)), Image.LANCZOS)
    return img


# function that embeds secret message into dct blocks
def embed_message(message, dct_blocks):

    #dct_blocks = dct_blocks.astype(int)  # converts from float64 to int32
    message_index = 0 
    # write message to last coefficient of every block
    for x in range(1, dct_blocks.shape[0]):  # curr_dct_blocks dim = (64, 8, 8)
        for y in range(1, dct_blocks.shape[1]):  
                    if dct_blocks[x, y, 0, 0] > 1 and message_index < len(message):
                        coeff = bitstring.pack('int:32', dct_blocks[x, y, 0, 0])
                        coeff[-1] = message[message_index]
                        dct_blocks[x, y, 0, 0], _ = coeff.unpack('int:32, bin')
                        message_index += 1

                        if message_index == len(message):
                            break

    if message_index is not len(message):
        print("message couldn't be stored in this image, try other image or different message")

    return dct_blocks


def get_embedded_message(dct_blocks):
    #dct_blocks = dct_blocks.astype(int)  # converts from float64 to int32
    msg = ""
    bitmessage = 0
    bit_index = 0
    int_char = 0

    for x in range(1, dct_blocks.shape[0]):  # curr_dct_blocks dim = (64, 8, 8)
        for y in range(1, dct_blocks.shape[1]): 
                    if dct_blocks[x, y, 0, 0] > 1:
                        coeff = bitstring.pack('int:32', dct_blocks[x, y, 0, 0])
                        # get letter as binary value (this step can be merged with next one)
                        bitmessage = bitmessage + coeff[-1:]    

                        # first byte of bitmessage is from inital value, not message so it's ignored
                        if (bit_index == 8):
                            int_char, _ = bitmessage.unpack('uint:8, bin')  
                            bitmessage = bitstring.pack('uint:1', 0)
                            bit_index = 0
                            # to prevent reading garbage
                            if int_char >= 32 and int_char < 127:  
                                msg = msg + chr(int_char)  # convert int to letter
                        bit_index += 1

    return msg


# function stitches 4D block array to 2D array
def stitch(blocks, c, r):
    array = np.zeros((c, r))
    for x in range(0, blocks.shape[0]):
        for y in range(0, blocks.shape[1]):
            array[x * 8:x * 8 + 8, y * 8:y * 8 + 8] = blocks[x, y, :, :]
    return array

#------------------- DWT HELPERS 
#------------------- ERROR CALCULATION HELPERS

def calculate_MSE(A, B):
    return (np.square(A - B)).mean(axis=None)

# EoF