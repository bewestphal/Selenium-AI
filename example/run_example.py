from example.configuration import ExampleConfiguration
from kickoff import kickoff


if __name__ == '__main__':
    configuration = ExampleConfiguration()
    kickoff(configuration=configuration)