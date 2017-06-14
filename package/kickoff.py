import os.path
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.callbacks import ModelIntervalCheckpoint
from rl.core import Agent

from models import KickoffModes, AbstractConfiguration


def kickoff(configuration):
    # type: (AbstractConfiguration) -> ()

    dqn = DQNAgent(
        model=configuration.create_cnn_model(),
        nb_actions=configuration.environment.action_space.number_of_actions,
        policy=configuration.policy,
        memory=configuration.memory,
        processor=configuration.processor,
        nb_steps_warmup=configuration.warmup_steps,
        gamma=configuration.gamma,
        target_model_update=configuration.target_model_update,
        train_interval=configuration.train_interval,
        delta_clip=configuration.delta_clip)

    dqn.compile(Adam(lr=configuration.learning_rate), metrics=configuration.metrics)

    if configuration.mode == KickoffModes.train:
        run_in_train_mode(dqn, configuration)

    elif configuration.mode == KickoffModes.test:
        run_in_test_mode(dqn, configuration)

def run_in_train_mode(dqn, configuration):
    # type: (Agent, AbstractConfiguration) -> ()

    checkpoint_weights_filename = configuration.checkpoint_weights_filename_base.format(step='')

    if os.path.isfile(configuration.weights_filename):
        dqn.load_weights(configuration.weights_filename)

    configuration.environment.make()

    callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=configuration.checkpoint_interval_steps)]

    dqn.fit(configuration.environment, callbacks=callbacks, nb_steps=configuration.number_of_steps, nb_max_episode_steps=1000)
    dqn.save_weights(configuration.weights_filename, overwrite=True)
    configuration.environment.selenium_docker_wrapper.clean()

def run_in_test_mode(dqn, configuration):
    # type: (Agent, AbstractConfiguration) -> ()

    if not os.path.isfile(configuration.weights_filename):
        raise ValueError('No Previous Weights Found')

    configuration.environment.make()

    dqn.load_weights(configuration.weights_filename)
    dqn.test(configuration.environment, nb_episodes=configuration.number_test_episodes, nb_max_episode_steps=1000)