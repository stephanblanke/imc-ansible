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
module: cisco_imc_server_power
short_description: Performs power operation on a Cisco IMC server
version_added: "2.4"
description:
    - Power on, off, cycle or gracefully shutdown the Cisco IMC server
Input Params:
    state:
        description:
         - if C(on), power on the server
         - if C(off), shutdown the server
         - if C(graceful-down), gracefully shutdown the server
         - if C(cycle), powercycle the server
        required: true
        choices: ['on', 'off', 'graceful-down', 'cycle']

    timeout:
        description: timeout in seconds
        default: 60

    interval:
        description: interval in seconds
        default: 5

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
- name: power on the server
  cisco_imc_server_power:
    timeout: 60
    interval: 10
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
    state: on
'''

RETURN = ''' # '''


def _argument_mo():
    return dict(
        timeout=dict(
            type='int',
            default=60),
        interval=dict(
            type='int',
            default=5),
        server_id=dict(
            type='int',
            default=1),
    )


def _argument_custom():
    return dict(
        state=dict(
            required=True,
            type='str',
            choices=['on', 'off', 'graceful-down', 'cycle'])
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
    from imcsdk.apis.server.serveractions import server_power_up
    from imcsdk.apis.server.serveractions import server_power_down
    from imcsdk.apis.server.serveractions import server_power_down_gracefully
    from imcsdk.apis.server.serveractions import server_power_cycle

    ansible = module.params
    args_mo = _get_mo_params(ansible)
    state = ansible["state"]

    if state == "on":
        mo, changed = server_power_up(server, **args_mo)
    elif state == "off":
        mo, changed = server_power_down(server, **args_mo)
    elif state == "graceful-down":
        mo, changed = server_power_down_gracefully(server, **args_mo)
    elif state == "cycle":
        mo, changed = server_power_cycle(server, **args_mo)

    if module.check_mode or changed:
        return changed


def setup(server, module):
    result = {}
    err = False

    try:
        result["changed"] = setup_module(server, module)
    except Exception as e:
        err = True
        result["msg"] = "setup error: %s" % str(e)
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
