"""
Role tests
"""
import pytest

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images(
    'infopen/ubuntu-trusty-ssh:0.1.0',
    'infopen/ubuntu-xenial-ssh-py27:0.2.0'
)


def test_packages(Package):

    packages = [
        'mariadb-client',
        'mariadb-server',
        'python-mysqldb',
        'software-properties-common',
    ]

    for package in packages:
        assert Package(package).is_installed

        if 'mariadb-' in package:
            assert '10.1.' in Package(package).version


def test_apt_repository_file(SystemInfo, File):

    apt_file = File('/etc/apt/sources.list.d/mariadb.list')

    expected_content = (
        "deb [arch=amd64] "
        "http://fr.mirror.babylon.network/mariadb/repo/10.1/{} "
        "{} main".format(SystemInfo.distribution, SystemInfo.codename))

    assert apt_file.exists
    assert apt_file.is_file
    assert apt_file.user == 'root'
    assert apt_file.group == 'root'
    assert apt_file.mode == 0o644
    assert expected_content in apt_file.content_string
