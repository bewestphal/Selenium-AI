from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

links = []
requires = []

requirements = parse_requirements('requirements.txt', session=PipSession())

for item in requirements:
    # we want to handle package names and also repo urls
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None): # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))

setup(name='seleniumai',
      description='An openAI environment that uses Selenium to create web automation agents',
      version='0.0.5',
      url='https://github.com/bewestphal/SeleniumAI',
      author='Brian Westphal',
      author_email='coding@brianwestphal.com',
      license='MIT',
      download_url='https://github.com/bewestphal/SeleniumAI',
      keywords=[
          'selenium',
          'artificial intelligence',
          'openai',
          'environment'
      ],
      packages = ['package'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      dependency_links=links,
      install_requires=requires)