from actions import ActionSpace
from driver import SeleniumDockerDriverWrapper
import re
from universe.envs.vnc_env import VNCEnv


class SeleniumEnvironment(VNCEnv):
    start_position_x = 0
    start_position_y = 0

    def __init__(self, configuration):
        super(VNCEnv, self).__init__()
        self.configuration = configuration
        self.action_space = ActionSpace()
        self.selenium_docker_wrapper = SeleniumDockerDriverWrapper()

    def render(self, mode='human', close=False):
        self.vnc_env._render()

    def make(self):
        self.driver = self.selenium_docker_wrapper.driver

        self.configuration.on_environment_creation and self.configuration.on_environment_creation()

        self.action_space.driver = self.driver

        container_url = self.selenium_docker_wrapper.connection_url
        container_port = int(container_url.split(':')[2])
        container_vnc_port = container_port - 1
        vnc_address = re.sub(str(container_port), str(container_vnc_port), container_url)
        vnc_address = re.sub('http', 'vnc', vnc_address)

        print 'You can view the VNC instance at ' + vnc_address, 'Password "secret"'

        self.vnc_env = VNCEnv()
        self.vnc_env._configure(remotes=str(vnc_address), vnc_kwargs={'password': 'secret'})

        self.driver.set_window_position(self.start_position_x, self.start_position_y)
        self.driver.set_window_size(self.configuration.window_width, self.configuration.window_height)

        if self.configuration.render:
            self.render()

        return self.driver

    def reset(self):
        self.driver.get(self.configuration.starting_url)
        action = self.action_space.reset_mouse_position()
        observation_array = self.vnc_env._step(action)
        self.configuration.on_step_reset and self.configuration.on_step_reset(self.driver)

        return observation_array

    def step(self, action_index):
        need_to_reset_states = [
            self.action_space.mouse_position_x > self.configuration.window_width,
            self.driver.execute_script("return window.pageYOffset;") == 0 and action_index == 1,
            self.driver.execute_script("return window.pageYOffset;") == self.driver.execute_script("return window.innerHeight;") and action_index == 2,
            self.action_space.mouse_position_x < self.start_position_x,
            self.action_space.mouse_position_y > self.configuration.window_height,
            self.action_space.mouse_position_y < self.start_position_y,
        ]

        if any(need_to_reset_state == True for need_to_reset_state in need_to_reset_states):
            done = True
            reward = -1
            observation_array = self.reset()
        else:
            action = self.action_space.available_actions[action_index]()
            done, reward = self.configuration.determine_reward(self.driver, action_index)
            observation_array = self.vnc_env._step(action)

        return observation_array, reward, done, {}