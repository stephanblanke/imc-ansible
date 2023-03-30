#!/usr/bin/python

# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: cisco_imc_vmedia_mapping
short_description: Mounts vMedia on a Cisco IMC server
version_added: "2.4"
description:
    - Adds and Removes vMedia mapping on a Cisco IMC server
Input Params:
    state:
        description:
         - if C(present), adds vMedia mapping
         - if C(absent), removed vMedia mapping
        choices: ['present', 'absent']
        default: "present"

    volume_name:
        description: volume name
        required: true

    remote_share:
        description: remote share address
        required: true

    remote_file:
        description: remote file name
        required: true

    map:
        description: mount protocol
        choices: ["cifs", "nfs", "www"]
        default: "www"

    mount_options:
        description: mount options
        default: "nolock"

    username:
        description: username for remote share

    password:
        description: password for remote share

    server_id:
        description: Server Id to be specified for C3260 platforms
        default: 1

    timeout:
        description: waits for the timeout seconds for mapping to finish
        default: 60

requirements:
    - 'imcsdk'
    - 'python2 >= 2.7.9 or python3 >= 3.2'
    - 'openssl version >= 1.0.1'

author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name: create vmedia mapping
  cisco_imc_vmedia_mapping:
    volume_name: c
    remote_share: http://1.1.1.1/files/
    remote_file: ubuntu-14.04.2-server-amd64.iso
    map: www
    mount_options: nolock
    state: present
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''

RETURN = ''' # '''


def _argument_mo():
    return dict(
        volume_name=dict(
            required=True,
            type='str'),
        remote_share=dict(
            required=True,
            type='str'),
        remote_file=dict(
            required=True,
            type='str'),
        map=dict(
            type='str',
            choices=["cifs", "nfs", "www"],
            default="www"),
        mount_options=dict(
            type='str',
            default="nolock"),
        username=dict(
            type='str',
            default=""),
        password=dict(
            type='str',
            default="",
            no_log=True),
        server_id=dict(type='int',
                       default=1),
        timeout=dict(type='int',
                       default=60),
    )


def _argument_custom():
    return dict(
        state=dict(default="present",
                   choices=['present', 'absent'],
                   type='str'),
    )


def _argument_connection():
    return dict(
        # ImcHandle
        imc_server=dict(type='dict'),

        # Imc server credentials
        imc_ip=dict(type='str'),
        imc_username=dict(default="admin", type='str'),
        imc_password=dict(type='str', no_log=True),
        imc_port=dict(default=None),
        imc_secure=dict(default=None),
        imc_proxy=dict(default=None)
    )


def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_custom())
    argument_spec.update(_argument_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
    args = {}
    for key in _argument_mo():
        if params.get(key) is None:
            continue
        args[key] = params.get(key)
    return args


def setup_module(server, module):
    from imcsdk.apis.server.vmedia import vmedia_mount_create
    from imcsdk.apis.server.vmedia import vmedia_mount_delete
    from imcsdk.apis.server.vmedia import vmedia_mount_exists

    ansible = module.params
    args_mo = _get_mo_params(ansible)
    exists, mo = vmedia_mount_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists
        vmedia_mount_create(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        vmedia_mount_delete(server,
                            args_mo['volume_name'],
                            args_mo['server_id'])
    return True


def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_module(server, module)
    except Exception as e:
        err = True
        result["msg"] = "setup error: %s " % str(e)
        result["changed"] = False

    return result, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection

    module = _ansible_module_create()
    conn = ImcConnection(module)
    server = conn.login()
    result, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**result)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
