import numpy as np
from project.app.functions import _data_size, create_data_points, create_lr_preds


def test_create_data():
    """
    Given data points with std 0.5,
    When we extract x and y shape
    Then the expected answers are asserted
    """
    data = create_data_points(0.5)
    x, y = data[0], data[1]
    assert x.shape == (_data_size,)
    assert y.shape == (_data_size,)
    assert x[0] == 0
    assert x[-1] == _data_size - 1



def test_create_lr_preds():
    """
    Given data points,
    When we create linear regression prediction,
    Then assert the r_sq and predictions type and shape
    """
    data = np.stack([np.arange(0, 10), np.arange(0, 10)])
    std = 0.5

    r_sq, predictions = create_lr_preds(data, std)
    assert isinstance(r_sq, float)
    assert isinstance(predictions, np.ndarray)
    assert predictions.shape == (10,)

# TODO - similarly tests could be written for each function