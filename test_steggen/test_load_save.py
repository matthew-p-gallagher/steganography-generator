import pytest
import numpy as np

from steggen.helpers import load_image, save_image

@pytest.fixture
def image_array():
    return np.random.randint(2, size=(100, 100, 3, 8), dtype="uint8")

def test_save_and_load(image_array):
    save_image(image_array, "test_image.png")
    image_array_in = load_image("test_image.png")
    assert np.array_equal(image_array, image_array_in)
