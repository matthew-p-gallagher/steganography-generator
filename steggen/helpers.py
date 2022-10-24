import numpy as np
from PIL import Image

###################################
######## File input/output ########

def load_data_from_file(filename: str) -> str:
    with open(filename, "r") as f:
        data = f.read()
    return data

def save_data_to_file(filename: str, data: str):
    print("Saving data to", filename)
    with open(filename, "w") as f:
        f.write(data)



def load_image(filename: str) -> np.ndarray:
    """
    Loads image from filename and transforms into Numpy array of bits

    Returns: Numpy array of shape (X, Y, 3, 8)
    """

    im = Image.open(filename)
    image_array = expand_ints_to_bits(np.array(im))

    return image_array 

def save_image(image_array: np.ndarray, filename: str):
    """
    Changes the bit array back to int form and saves
    """
    image_array = collapse_bits_to_ints(image_array)
    im = Image.fromarray(image_array)
    
    print("Saving data to", filename)
    im.save(filename)

###################################
####### Data transformation #######

def expand_ints_to_bits(image_array: np.ndarray) -> np.ndarray:
    """
    Expands each integer in the image array to another dimension of 8 bits

    Returns: Numpy array of shape (X, Y, 3, 8)
    """
    # Create new array with 8 bits per pixel
    bit_image_array = np.zeros(image_array.shape + (8,), dtype="uint8")
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for k in range(image_array.shape[2]):
                bit_image_array[i, j, k] = np.unpackbits(image_array[i, j, k])
    return bit_image_array

def collapse_bits_to_ints(bit_image_array: np.ndarray) -> np.ndarray:
    """
    Collapses each 8 bit dimension into a single integer

    Returns: Numpy array of shape (X, Y, 3)
    """
    image_array = np.zeros(bit_image_array.shape[:-1], dtype="uint8")
    for i in range(bit_image_array.shape[0]):
        for j in range(bit_image_array.shape[1]):
            for k in range(bit_image_array.shape[2]):
                image_array[i, j, k] = np.packbits(bit_image_array[i, j, k])[0]
    return image_array

def string_to_bits(data: str) -> np.ndarray:
    """
    Transforms string into array of characters as 8 bits

    Returns: Array of 8 bit lists for each character in string
    """
    data_array = [[int(b) for b in bin(ord(c))[2:]] for c in data]
    for n, cb in enumerate(data_array):
        if len(cb) != 8:
            data_array[n] = [0] * (8 - len(cb)) + data_array[n]

    return np.array(data_array, dtype="uint8").flatten()

def bits_to_string(bits: np.ndarray) -> str:
    """
    Transforms flat numpy array of bits into string

    Returns: String
    """

    # Check array can be split into bytes
    if len(bits) % 8 != 0:
        raise ValueError("Bit array cannot be split into bytes")

    # Shape into bytes
    # -1 takes as many as needed to match the other dimension
    char_bytes = bits.reshape(-1, 8)

    out_str = "".join([chr(bits_to_int(arr)) for arr in char_bytes])
    
    return out_str

def bits_to_int(bits):
    """
    Transforms a list of bits (any length) to an integer

    Returns: Single integer
    """
    bits = list(bits)

    total = 0
    mult = 1
    while len(bits) > 0:
        bit = bits.pop()
        total += bit * mult
        mult *= 2
    return total

###################################