import pytest
import numpy as np
import os

from steggen.pipeline import encrypt, decrypt
from steggen.helpers import load_image, save_image
from steggen.encoding import encode_length, pull_length


def test_encrypt_decrypt():

    data = "abcdefg12345000"

    encrypt(data)
    decrypt("secrets_kept.png")
    with open("data\\out.txt", "r") as f:
        data_out = f.read()
    assert data == data_out




