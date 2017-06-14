import numpy as np
from PIL import Image
from rl.core import Processor


class SeleniumObservationProcessor(Processor):
    def __init__(self, window_height, window_width):
        self.window_height = window_height
        self.window_width = window_width

    def process_observation(self, observation):
        #  TODO Add a text observation of the url or html?
        vision_observation = observation[0][0].get('vision', None)
        assert vision_observation.ndim == 3  # (height, width, channel)
        vision_observation = vision_observation[0:self.window_height, 0:self.window_width]
        img = Image.fromarray(vision_observation)
        img = img.convert('L')  # convert to grayscale
        processed_observation = np.array(img)
        return processed_observation.astype('uint8')  # saves storage in experience memory

    def process_state_batch(self, batch):
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return np.clip(reward, -1., 1.)