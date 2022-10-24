import numpy as np
from PIL import Image

from steggen.helpers import *

def encode_length(length: int, image_array: np.ndarray) -> np.ndarray:
    """
    Encodes the length of the data into the image array
    """
    # Get length as 24 bit array
    length_bits = np.array([ int(c) for c in np.binary_repr(length, width=24)], dtype="uint8")

    # Set some arbitrary bits in the image as the length bits
    # These bits will not be touched by the data encryption
    image_array[0,:24,0,3] = length_bits

    return image_array

def pull_length(image_array: np.ndarray) -> int:
    """
    Pulls the length of the data from the image array
    """
    # Get the length bits from the image
    length_bits = image_array[0,:24,0,3]

    # Convert the length bits to an integer
    length = bits_to_int(length_bits)

    return length

def encode_data(data_bits: np.ndarray, image_array: np.ndarray) -> np.ndarray:
    """
    Encodes the data into the image array from the LSB up
    """
    # Number of bits available at each slice of image array
    slice_size = image_array.size // 8

    # The encryption only uses the first 5 bits of each byte
    # If the data is too large an error will be thrown
    slices_needed = (len(data_bits) // slice_size) + 1
    if slices_needed > 4:
        raise Exception("Data too large to encrypt")
    
    # Pad the data and shape into slices of the array shape
    shaped_data = np.append( np.zeros((slice_size - ( len(data_bits) % slice_size ),),dtype="uint8") , [data_bits] ).reshape( (slices_needed,) + image_array.shape[:3])

    # Place the data into the image array for the LSB up
    for i in range(slices_needed):
        image_array[:,:,:,7-i] = shaped_data[i]

    return image_array

def pull_data(image_array: np.ndarray) -> str:
    """
    Pulls the data into string format from the image array
    """

    # Get the length of the data
    length = pull_length(image_array)
    len_bits = length * 8

    # Get the number of slices to iterate through
    slices_needed = (len_bits // (image_array.size // 8)) + 1

    # Pull the data from the image array
    shaped_data = np.empty((slices_needed,) + image_array.shape[:3], dtype="uint8")
    for i in range(slices_needed):
        shaped_data[i] = image_array[:,:,:,7-i]

    # Flatten the data and remove the padding
    data_bits = shaped_data.flatten()[-len_bits:]

    # Convert the data bits to a string
    return bits_to_string(data_bits)
