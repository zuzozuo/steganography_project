# steganography_project
Python Implementation of  DCT, DWT and LSB  algorithms for embedding text message in images.
The project was done for Securing Data Transmission subject.

## HOW TO launch the project
- You need python 3.9 > installed on your enviroment.
- Launch your terminal
- Go to the directory with the cloned repo
- Type python main.py

![notitle](https://user-images.githubusercontent.com/32846803/172250802-8ce674d1-35fa-4f8e-b4fc-50056dac189d.png)


### What was done?
- [x] LSB text message encoding
- [x] LSB text message decoding
- [x] DWT text message encoding
- [ ] DWT text message decoding
- [x] DCT text message encoding
- [ ] DCT text message decoding

### What is not working?
- DCT decoding: reading message after opening image with encoded message. The data is lost due to the compression.
- DWT decoding: reading message after opening image with encoded message. The data is lost due to the compression.

Additionaly in DCT we tested if you can read embedded message before saving the image - it can be done.


Authors:
Zuzanna Dąbrowa, Marcin Maj, Bartosz Kowal
