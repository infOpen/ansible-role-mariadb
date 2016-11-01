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


def test_main_configuration_file(File):

    main_cfg_file = File('/etc/mysql/my.cnf')

    assert main_cfg_file.contains('\[galera\]') is False
    assert main_cfg_file.contains('innodb_open_files\s*=\s*500')
    assert main_cfg_file.contains('quote-names\s*=\s*1')


def test_service(Service):

    service = Service('mysql')

    assert service.is_enabled
    assert service.is_running


def test_mariadb_accounts(Command, File):

    Command('mysql -u root -ptest123 -NBe "SELECT DISTINCT User FROM mysql.user" > /tmp/mariadb_users.txt')
    mariadb_accounts = File('/tmp/mariadb_users.txt')

    assert mariadb_accounts.contains('root')
    assert mariadb_accounts.contains('debian-sys-maint')
    assert mariadb_accounts.contains('ansible-test')


def test_credentials_file(File):

    credentials_file = File('/root/.my.cnf')

    assert credentials_file.exists
    assert credentials_file.is_file
    assert credentials_file.user == 'root'
    assert credentials_file.group == 'root'
    assert credentials_file.mode == 0o400
    assert credentials_file.contains('\[client\]')
    assert credentials_file.contains('user\s*=\s*root')
    assert credentials_file.contains('password\s*=\s*test123')


def test_mariadb_databases(Command, File):

    Command('mysql -u root -ptest123 -NBe "SHOW DATABASES" > /tmp/mariadb_databases.txt')
    mariadb_databases = File('/tmp/mariadb_databases.txt')

    assert mariadb_databases.contains('information_schema')
    assert mariadb_databases.contains('mysql')
    assert mariadb_databases.contains('performance_schema')
    assert mariadb_databases.contains('foobar')
