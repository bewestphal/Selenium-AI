from setuptools import setup
from pip.req import parse_requirements

reqs = install_reqs = parse_requirements('requirements.txt')

setup(name='SeleniumAI',
      description='An openAI environment that uses Selenium to create web automation agents',
      version='0.0.2',
      url='https://github.com/bewestphal/SeleniumAI',
      author='Brian Westphal',
      author_email='coding@brianwestphal.com',
      license='MIT',
      keywords=[
          'selenium',
          'artificial intelligence',
          'openai',
          'environment'
      ],
      packages = ['lib'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      nstall_requires=reqs
)