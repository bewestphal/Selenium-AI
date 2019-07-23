import docker
from selenium import webdriver
from io import BytesIO
import tarfile
import time
import os

from srcdir import srcdir


class SeleniumDockerDriverWrapper(object):
    image_name = 'selenium/standalone-chrome-debug:3.4.0-chromium'
    container_ports = [4444, 5900]
    port_bindings = {5900 : ('127.0.0.1',), 4444 : ('127.0.0.1',)}

    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"

    session = None

    def __init__(self):
        self.container = None
        self.container_id = None
        self.driver = self._create_driver()

    def _create_docker_container(self):
        container = self.docker_client.create_container(self.image_name,
                                                   detach=True,
                                                   ports=self.container_ports,
                                                   host_config=self.docker_client.create_host_config(
                                                    port_bindings=self.port_bindings
                                                   ))
        return container

    def create_container(self):
        self.docker_client = docker.Client()

        self.docker_client.pull(self.image_name)

        self.container = self._create_docker_container()
        self.container_id = self.container.get("Id")
        self.docker_client.start(self.container_id)
        time.sleep(10)

    @property
    def connection_url(self):
        container_port_info = self.docker_client.port(self.container_id, self.container_ports[0])[0]
        connection_url = ':'.join(['http://' + container_port_info.get("HostIp"), container_port_info.get("HostPort")])
        return connection_url

    def _create_driver(self):
        self.create_container()

        selenium_url = self.connection_url  + '/wd/hub'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent=" + self.user_agent)

        driver = self._connect_to_remote_instance(chrome_options, selenium_url)

        return driver

    def _connect_to_remote_instance(self, chrome_options, selenium_url):
        return webdriver.Remote(
            command_executor=selenium_url,
            desired_capabilities=chrome_options.to_capabilities())

    def clean(self):
        print('Cleaning up Selenium driver and docker container')

        self.driver and self.driver.quit()
        self.container and self.docker_client.remove_container(self.container_id, force=True)

    def create_archive(self, filepath):
        print(filepath)
        pw_tarstream = BytesIO()
        pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode='w')
        file_data = open(filepath, 'rb').read()
        tarinfo = tarfile.TarInfo(name=os.path.basename(filepath))
        tarinfo.size = len(file_data)
        tarinfo.mtime = time.time()
        pw_tar.addfile(tarinfo, BytesIO(file_data))
        pw_tar.close()
        pw_tarstream.seek(0)
        return pw_tarstream

    def upload_file_to_container(self, filepath):
        with self.create_archive(filepath) as archive:
            return self.docker_client.put_archive(container=self.container_id, path='/', data=archive)
