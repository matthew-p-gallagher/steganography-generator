import os
import sys

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from steggen.encoding import *
from steggen.helpers import *


def encrypt(data: str):
    """
    Runs through the encryption pipeline. In the end, an encrypted image is saved to the root directory.
    """

    # Get image as numpy array of shape (X, Y, 3, 8)
    image_array = load_image("image\\secrets.png")
    
    # Encode the length of the data into the image for decoding
    image_array = encode_length(len(data), image_array)

    # Encode the data into the suitable format with a header
    data_bits = string_to_bits(data)

    # Place the data into the image
    image_array = encode_data(data_bits, image_array)

    # Save the image
    save_image(image_array, "secrets_kept.png")

def decrypt(filename: str):
    """
    Runs through the decryption pipeline. In the end, the data is printed to the console.
    """

    # Get image with data, as numpy array of shape (X, Y, 3, 8)
    image_array = load_image(filename)

    # Get the length of the data
    length = image_array[0,:24,0,3]
    length = bits_to_int(length)

    # Decode the data from the image
    data = pull_data(image_array)

    save_data_to_file( "data\\out.txt", data)