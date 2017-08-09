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
module: cisco_imc_firmware_update
short_description: Updates firmware via HUU utility
version_added: "2.4"
description:
    - Updates CIMC firmware
Input Params:
    remote_share:
        description: full path to the firmware image file
        required: True

    share_type:
        description: share protocol
        required: True
        choices: ["nfs", "www", "cifs"]

    remote_ip:
        description: ip address of the remote host
        required: True

    username:
        description: remote host username

    password:
        description: remote host password

    update_component:
        description: component to be updated
        default: "all"

    stop_on_error:
        description: stops update on error
        default: "yes"
        choices: ["yes", "no"]

    verify_update:
        description: verifies update
        default: "yes"
        choices: ["yes", "no"]

    cimc_secure_boot:
        description: secure boot flag
        default: "yes"
        choices: ["yes", "no"]

    timeout:
        description: timeout in minutes
        default: 60

    force:
        description: if True, update without checking existing version
        default: False

    interval:
        description: frequency of monitoring in seconds
        default: 60

    server_id:
        description: Server Id to be specified for C3260 platforms
        default: 1

requirements:
    - 'imcsdk'
    - 'python2 >= 2.7.9 or python3 >= 3.2'
    - 'openssl version >= 1.0.1'

author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name: update cimc firmware
  cisco_imc_firmware_update:
    remote_share: /ucs-c240m4-huu-3.0.2b.iso
    share_type: www
    remote_ip: 10.65.33.165
'''

RETURN = ''' # '''


def _argument_mo():
    return dict(
        remote_share=dict(
            required=True,
            type='str'),
        share_type=dict(
            required=True,
            type='str',
            choices=["nfs", "www", "cifs"]),
        remote_ip=dict(
            required=True,
            type='str'),
        username=dict(
            type='str'),
        password=dict(
            type='str',
            no_log=True),
        update_component=dict(
            type='str',
            default='all'),
        stop_on_error=dict(
            type='str',
            choices=["yes", "no"],
            default="yes"),
        verify_update=dict(
            type='str',
            choices=["yes", "no"],
            default="yes"),
        cimc_secure_boot=dict(
            type='str',
            choices=["yes", "no"],
            default="yes"),
        timeout=dict(
            type='int',
            default=60),
        interval=dict(
            type='int',
            default=60),
        force=dict(
            type='bool',
            default=False),
        server_id=dict(
            type='int',
            default=60),
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
    from imcsdk.utils.imcfirmwareinstall import firmware_update
    from imcsdk.utils.imcfirmwareinstall import firmware_exists
    from imcsdk.utils.imcfirmwareinstall import version_extract

    ansible = module.params
    args_mo = _get_mo_params(ansible)
    version = version_extract(args_mo['remote_share'])
    exists, mo = firmware_exists(server, version,
                                 args_mo['server_id'], args_mo['force'])

    if module.check_mode or exists:
        return not exists
    firmware_update(handle=server, **args_mo)

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
