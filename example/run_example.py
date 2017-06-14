from example.configuration import ExampleConfiguration
from package.kickoff import kickoff


if __name__ == '__main__':
    configuration = ExampleConfiguration()
    kickoff(configuration=configuration)