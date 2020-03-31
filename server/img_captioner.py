from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation

class ImageCaptioner:
  def create_cnn(self, type):
    """
    creates a CNN.
    :param type: str, ['rand' | 'trained' ]
    :return: Sequential, keras CNN
    """
    if type == 'rand':
      model = Sequential([
        Conv2D(48, kernel_size=8, input_shape=(128, 128, 1)),
        Activation('relu'),
        MaxPooling2D

      ])

