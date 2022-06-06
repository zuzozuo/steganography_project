from PIL import Image

class LSB():

    def encode(self, img, message):
        encoded_img_name = './img/encoded_LSB.png'
        img = Image.open(img, 'r')
        width, height = img.size
        pixel_values = list(img.getdata())
        message_bits = [str(bin(ord(c)))[2:] for c in message] #changing chars into binary 
        message_bits = "".join(message_bits) 

        # checking length of the message it see if it fits into picture
        if(len(pixel_values) > len(message_bits)):
            for x in range(0, len(message_bits)): 
                R,G,B = pixel_values[x] 
                B = str(bin(B)) 

                if(len(B[2:]) < 8): 
                    zeros = "0" * (8 - len(B[2:])) # example:  taking 6bit value and extending it to 8 bits
                    B = '0b' + zeros + B[2:]

                B = B[:-1] + message_bits[x] # inserting message bits
                B = int(B,2)
                pixel_values[x] = (R,G,B)

        

        out_img = Image.new('RGB', (width, height)) # creating new file 
        out_img.putdata(pixel_values)
        out_img.save(encoded_img_name)
        return encoded_img_name


    def decode(self, img):
        img = Image.open(img, 'r')
        # width, height = img.size
        pixel_values = list(img.getdata())
        bits = ""

        for pixel in pixel_values: 
            R,G,B = pixel
            bits += str(bin(B))[-1] # converting B tuple into binary

        #joining message bits together
        chars = [chr(int('0b'+ bits[i:i+7], 2)) for i in range(0, len(bits), 7)]
        for i in range(0, len(chars)):
            if chars[i] == '$':
                chars = chars[0:i]
                break
        return(''.join(chars))

# EoF

