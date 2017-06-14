from example.configuration import ExampleConfiguration
from lib.kickoff import kickoff


if __name__ == '__main__':
    configuration = ExampleConfiguration()
    kickoff(configuration=configuration)