import pytest
import numpy as np
import os

from steggen.helpers import load_image, save_image
from steggen.encoding import encode_length, pull_length

@pytest.fixture
def data_length():
    return 100

@pytest.fixture
def image_array():
    return np.zeros((100, 100, 3, 8), dtype="uint8")

def test_encode_pull_length(image_array, data_length):

    image_array = encode_length(data_length, image_array)
    save_image(image_array, "test_image.png")
    image_w_length = load_image("test_image.png")
    length = pull_length(image_w_length)
    assert length == data_length




