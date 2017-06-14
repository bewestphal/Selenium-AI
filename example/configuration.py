from environment import SeleniumEnvironment
from processor import SeleniumObservationProcessor
import keras.backend as K
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from keras.layers.convolutional import Conv2D
from keras.models import Sequential
import numpy as np
from models import AbstractConfiguration, KickoffModes
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from srcdir import srcdir
import os


class ExampleConfiguration(AbstractConfiguration):
    mode = KickoffModes.train  # type: KickoffModes

    use_preset_training = True
    render = True # Default true when testing

    number_test_episodes = 1000

    window_width = 375
    window_height = 1020
    window_length = 4

    number_of_steps = 10000

    gamma = 0.99
    target_model_update = 10000
    train_interval = 4
    delta_clip = 1.
    learning_rate = .00025

    metrics = ['mae']

    processor = SeleniumObservationProcessor(window_height, window_width)
    memory = SequentialMemory(limit=1000000, window_length=window_length)

    warmup_steps = 5000

    weights_filename = 'dqn_selenium_ai_weights.h5f'

    checkpoint_interval_steps = 250000
    checkpoint_weights_filename_base = 'dqn_selenium_ai_weights_{step}.h5f'

    base_policy = LinearAnnealedPolicy(
        EpsGreedyQPolicy(),
        attr='eps',
        value_max=1.,
        value_min=.1,
        value_test=.05,
        nb_steps=number_of_steps)

    def __init__(self):
        self.environment = SeleniumEnvironment(self)

    @property
    def policy(self):
        if self.use_preset_training:
            self.base_policy.select_action = lambda **_: self.get_preset_training_step()

        return self.base_policy

    def create_cnn_model(self):
        input_shape = (self.window_length,) + (self.window_height, self.window_width)

        model = Sequential()
        if K.image_dim_ordering() == 'tf': # Tensorflow
            # (width, height, channels)
            model.add(Permute((2, 3, 1), input_shape=input_shape))
        elif K.image_dim_ordering() == 'th': # Theano
            # (channels, width, height)
            model.add(Permute((1, 2, 3), input_shape=input_shape))
        else:
            raise RuntimeError('Unknown image_dim_ordering.')

        model.add(Conv2D(32, 8, 8, subsample=(4, 4)))
        model.add(Activation('relu'))
        model.add(Convolution2D(32, 4, 4, subsample=(2, 2)))
        model.add(Activation('relu'))
        model.add(Convolution2D(32, 3, 3, subsample=(1, 1)))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dense(self.environment.action_space.number_of_actions))
        model.add(Activation('linear'))

        return model

    def on_step_reset(self, driver):
        # Scroll to random point on the page
        page_height = driver.execute_script("return document.documentElement.scrollHeight")
        np_random = np.random.RandomState()
        # scroll_position = np_random.randint(low=0, high=page_height) - self.window_height
        scroll_position = np_random.randint(low=0, high=self.window_height-250)

        driver.execute_script("window.scrollBy(0,{scroll_position});".format(scroll_position=scroll_position))

    def on_environment_creation(self):
        # Create file within the docker container to use as the test web page
        filepath = srcdir + '/example/test.html'
        self.environment.selenium_docker_wrapper.upload_file_to_container(filepath)
        self.starting_url = 'file://' + '/' + os.path.basename(filepath)

    def get_preset_training_step(self):
        if self.environment.driver.current_url ==  'file:///gp/aw/c/ref=mw_dp_buy_crt':
            return 0

        targeted_element_xpath = '//input[contains(@id, "add-to-cart-button")]'
        target_element = self.environment.driver.find_element_by_xpath(targeted_element_xpath)

        target_element_top = target_element.location["y"]
        target_element_bottom = target_element_top + target_element.size["height"]

        scroll_amount = self.environment.driver.execute_script("return window.pageYOffset;")
        window_size = self.environment.driver.get_window_size()
        inner_height = self.environment.driver.execute_script("return window.innerHeight;")

        if scroll_amount > target_element_top:
            action = self.environment.action_space.mouse_scroll_up
        elif scroll_amount + inner_height < target_element_bottom:
            action = self.environment.action_space.mouse_scroll_down
        else:
            target_element_left = target_element.location["x"]
            target_element_right = target_element_left + target_element.size["width"]

            if self.environment.action_space.mouse_position_x > target_element_right:
                action = self.environment.action_space.move_mouse_left
            elif self.environment.action_space.mouse_position_x < target_element_left:
                action = self.environment.action_space.move_mouse_right
            elif self.environment.action_space.mouse_position_y - (window_size["height"] - inner_height) + scroll_amount \
                    > target_element_bottom:
                action = self.environment.action_space.move_mouse_up
            elif self.environment.action_space.mouse_position_y - (window_size["height"] - inner_height) + scroll_amount \
                    < target_element_top:
                action = self.environment.action_space.move_mouse_down
            else:
                action = self.environment.action_space.mouse_press

        return self.environment.action_space.available_actions.index(action)

    def determine_reward(self, driver, action_index):
        reward_indicator_url = 'file:///gp/aw/c/ref=mw_dp_buy_crt'

        if driver.current_url == reward_indicator_url:
            reward = 1
            done = True
        elif action_index == 0 and driver.current_url != reward_indicator_url:
            reward = -1
            done = True
        else:
            reward = 0
            done = False

        return done, reward