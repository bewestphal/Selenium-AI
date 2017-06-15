# SeleniumAI
An openAI environment using selenium + docker for creating web automation agents

# Installation
Install the requirements.txt file with pip

This package requires docker. You can install docker by following the instructions here: https://docs.docker.com/engine/installation/

Using the same Keras weights file, multiple docker agents can be run in parallel.

# Why do I need to use Selenium?
OpenAi Vnc agents require some guidance to get working beyond randomly clicking and sending inputs to the page.

With SeleniumAI you can program pre-trained steps to look into the browser, guiding the pointer towards the desired elements and issuing rewards based on the region clicked by the agent or the state of input elements and the browser.

# Notes
The docker container can be viewed by setting the configuration property render to True or by viewing via VNC at the port printed in the console logs. Password to the VNC viewer is 'secret'

The example provided clicks the add to cart button on the amazon mobile page. The test is initialized by setting a random amount of scroll on the page by directly interacting with the selenium browser.

Selenium AI is packaged with the reinforcement learning agents from the excellent keras-rl package. Making a configurable agent is the next step for improving this package.

# Acknowledgments
* keras-rl
* openai
