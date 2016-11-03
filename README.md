# mariadb

[![Build Status](https://travis-ci.org/infOpen/ansible-role-mariadb.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-mariadb)

Install mariadb package.

## Requirements

This role requires Ansible 2.1 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role has some testing methods.

To use locally testing methods, you need to install Docker and/or Vagrant and Python requirements:

* Create and activate a virtualenv
* Install requirements

```
pip install -r requirements_dev.txt
```

### Automatically with Travis

Tests runs automatically on Travis on push, release, pr, ... using docker testing containers

### Locally with Docker

You can use Docker to run tests on ephemeral containers.

```
make test-docker
```

### Locally with Vagrant

You can use Vagrant to run tests on virtual machines.

```
make test-vagrant
```

## Role Variables

### Default role variables

``` yaml
# True: use system packages, else use mariadb.org repositories
mariadb_use_system_repository: True

# General repositories informations
mariadb_packages: "{{ _mariadb_packages }}"
mariadb_prerequisites_packages: "{{ _mariadb_prerequisites_packages }}"

#  Debian family specific variables
mariadb_apt_cache_valid_time: "{{ _mariadb_apt_cache_valid_time }}"
mariadb_apt_key_id: "{{ _mariadb_apt_key_id[(ansible_distribution_release | lower)] }}"
mariadb_apt_key_server: "{{ _mariadb_apt_key_server }}"
mariadb_apt_repository_arch: "{{ _mariadb_apt_repository_arch }}"
mariadb_apt_repository_url: "{{ _mariadb_apt_repository_url }}"
mariadb_apt_sources_list_mode: "{{ _mariadb_apt_sources_list_mode }}"
mariadb_apt_sources_list_path: "{{ _mariadb_apt_sources_list_path }}"
mariadb_apt_update_cache: "{{ _mariadb_apt_update_cache }}"

# If not use system repository, need more informations
mariadb_version: '10.1'

# Configuration management
mariadb_config_files:
  - path: "{{ _mariadb_config_main_file_path }}"
    items:
      - section: 'mysqld'
        option: 'plugin-load-add'
        value: 'unix_socket=auth_socket.so'
mariadb_socket_path: '/var/run/mysqld/mysqld.sock'

# Service management
mariadb_service_enabled: True
mariadb_service_name: "{{ _mariadb_service_name }}"
mariadb_service_state: 'started'

# Root account credentials
mariadb_root_old_password: ''
mariadb_root_password: ''

# Root account connection management
mariadb_root_use_socket: True

# Accounts management
mariadb_remove_unmanaged_accounts: True
mariadb_accounts:
  - name: 'root'
    password: "{{ mariadb_root_password }}"
    hosts:
      - 'localhost'
    files:
      - dest: '/root/.my.cnf'
        owner: 'root'
        group: 'root'
        mode: '0400'
  - name: 'debian-sys-maint'
    hosts:
      - 'localhost'

# Databases management
mariadb_remove_unmanaged_databases: True
mariadb_protected_databases:
  - 'information_schema'
  - 'mysql'
  - 'performance_schema'
mariadb_databases: []
```

## How ...

### Define users

Users can be managed with ***mariadb_accounts*** array variable.

If ***mariadb_remove_unmanaged_accounts*** variable is set to True (default value), all users not managed by ***mariadb_accounts*** will be removed !

An account structure is:
```yaml
- name: 'foo'
  password: 'bar'    # Default: omit
  encrypted: 'False' # Default: False
  priv: '*.*:USAGE'  # Default: omit
  append_privs: True # Default: False
  state: 'present'   # Default: 'present'
  hosts:
    - 'host1'
    - 'host2'
  files: # Credentials files
    - dest: '/home/foo/.my.cnf'
      owner: 'foo'
      group: 'foo'
      mode: '0400'
```

### Define databases

Databases can be managed with ***mariadb_databases*** array variable.

If ***mariadb_remove_unmanaged_databases*** variable is set to True (default value), all databases not managed by ***mariadb_databases*** will be removed (except protected databases) !

A database structure is:
```yaml
- name: 'my_database'
  collation: 'utf8_general_ci' # Default: omit
  encoding: 'utf8' # Default: omit
```

## Dependencies

None

## Example Playbook

    - hosts: servers
      roles:
         - { role: infOpen.mariadb }

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
