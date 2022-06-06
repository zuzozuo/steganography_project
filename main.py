import numpy as np
import matplotlib.pylab as plt
from helpers import calculate_MSE
from PIL import Image
import dct
import cv2
import lsb
import dwt


print("######################################################")
print("#        Securing Data Transmission Project          #")
print("#   Implementation of 3  image encoding algorithms   #")
print("#                    Authors:                        #")
print("#    Bartosz Kowal, Zuzanna Dabrowa, Marcin Maj      #")
print("######################################################")



dct_obj = dct.DCT()
lsb_obj = lsb.LSB()
dwt_obj = dwt.DWT()
img_png = "./img/LENNA.png"
img_jpg = "./img/lenna.jpg"
secret_msg = "secretmessage$$"

print("Launching LSB method.....")
encoded_img_name = lsb_obj.encode(img_jpg, secret_msg)
decoded_message = lsb_obj.decode(encoded_img_name)
print("LSB decoded message: " + decoded_message)

# ------------------------------------------------------------------
print("Launching DCT method.....")


img_encoded, img_original, dec_msg = dct_obj.encode(img_png, secret_msg)
img_encoded = Image.fromarray(img_encoded)
img_encoded = img_encoded.convert('RGB')
img_encoded.save("./img/encoded_DCT.png")

message, img = dct_obj.decode("./img/encoded_DCT.png")
img_decoded = Image.fromarray(img)
img_decoded = img_decoded.convert('RGB')
img_decoded.save("./img/decoded_DCT.png")

print(f'encoded message: {secret_msg}')
print(f'decoded message (before saving the image): {dec_msg}') 
print(f'decoded message (after reading saved image): {message}')

plt.subplot(311), plt.imshow(img_original), plt.axis('off'), plt.title('original image', size=15)
plt.subplot(312), plt.imshow(img_encoded), plt.axis('off'), plt.title('encoded image', size=15)
plt.subplot(313), plt.imshow(img), plt.axis('off'), plt.title('decoded image', size=15)
plt.show()

# --------------------------------------------------------------

print("Launching DWT method.....")
dwt_obj.encode_img(img_png, secret_msg)
dwt_msg = dwt_obj.decode_img("./img/encoded_DWT.png")
print("\n\nDecoded message (first 300 chars): \n" + dwt_msg)

# -------------------------------------------------------------
#   GATHERING ALL ORIGINAL AND ENCODED IMAGES AND CONVERTING THEM INTO NDARRAYS

LSB_original = np.array(Image.open(img_jpg))
LSB_encoded =  np.array(Image.open(encoded_img_name))

DCT_original = np.array(Image.open(img_png))
DCT_encoded = np.array(Image.open("./img/encoded_DCT.png"))

DWT_original = np.array(Image.open(img_png))
DWT_encoded = np.array(Image.open("./img/encoded_DWT.png"))
#--------------------------------------------------------------
print("-------------------------------------------------------")
print("Calculating MSE: \n")
print("MSE LSB:  " + str(calculate_MSE(LSB_original, LSB_encoded)) + 'dB')
print("MSE DCT:  " + str(calculate_MSE(DCT_original, DCT_encoded)) + 'dB')
print("MSE DWT:  " + str(calculate_MSE(DWT_original, DWT_encoded)) + 'dB')

print("\nCalculating PSNR: \n")
print("PSNR LSB:  " + str(cv2.PSNR(cv2.imread(img_jpg), cv2.imread('./img/encoded_LSB.png'))) + ' dB')
print("PSNR DCT:  " + str(cv2.PSNR(cv2.imread(img_png), cv2.imread('./img/encoded_DCT.png'))) + ' dB')
print("PSNR DWT:  " + str(cv2.PSNR(cv2.imread(img_png), cv2.imread('./img/encoded_DWT.png'))) + ' dB')


# EoF


