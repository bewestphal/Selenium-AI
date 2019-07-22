import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../package'))
from example.configuration import ExampleConfiguration
from package.kickoff import kickoff


if __name__ == '__main__':
    configuration = ExampleConfiguration()
    kickoff(configuration=configuration)
