from rl.core import Processor
from rl.policy import Policy
from rl.memory import Memory

from environment import SeleniumEnvironment


class AbstractConfiguration(object):
    mode = None  # type: KickoffModes

    use_preset_training = None  # type: bool
    render = None  # type: bool

    warmup_steps = None  # type: int
    number_test_episodes = None  # type: int
    number_of_steps = None  # type: int

    window_width = None  # type: int
    window_height = None  # type: int
    window_length = None  # type: int

    gamma = None  # type: int
    target_model_update = None  # type: int
    train_interval = None  # type: int
    delta_clip = None  # type: int
    learning_rate = None  # type: int

    metrics = None  # type: str

    processor = None  # type: Processor
    memory = None  # type: Memory

    weights_filename = None  # type: str

    checkpoint_interval_steps = None  # type: int
    checkpoint_weights_filename_base = None  # type: str

    environment = None  # type: SeleniumEnvironment
    policy = None  # type: Policy

    def determine_reward(self, driver, action_index):
        raise NotImplementedError()

    def create_cnn_model(self):
        pass

    def on_step_reset(self):
        pass

    def on_environment_creation(self):
        pass

    def get_preset_training_step(self):
        pass


class KickoffModes(object):
    train = 'train'
    test = 'test'