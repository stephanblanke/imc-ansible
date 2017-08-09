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
module: cisco_imc_bios_serial
short_description: Configures BIOS serial on a Cisco IMC server
version_added: "2.4"
description:
    - Configures the serial configuration of BIOS on a Cisco IMC server
Input Params:
    vp_console_redirection:
        description: console redirection
        choices: ["com-0", "com-1", "disabled"]

    vp_terminal_type:
        description: terminal type
        choices: ["pc-ansi", "platform-default", "vt-utf8", "vt100", "vt100-plus"]

    vp_baud_rate:
        description: baud rate (bits per second)
        choices: ["115200", "19200", "38400", "57600", "9600"]

    vp_flow_control:
        description: flow control
        choices: ["none", "rts-cts"]

    vp_putty_key_pad:
        description: putty kepypad
        choices: ["ESCN", "LINUX", "SCO", "VT100", "VT400", "XTERMR6"]

    vp_redirection_after_post:
        description: redirection after bios post
        choices: ["Always Enable", "Bootloader", "platform-default"]

    vp_legacy_os_redirection:
        description: legacy os redirection
        choices: ["Disabled", "Enabled", "disabled", "enabled", "platform-default"]

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
- name: enable console redirection for SOL
  cisco_imc_bios_serial:
    vp_console_redirection: "com0"
    vp_baud_rate: "115200"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''

RETURN = ''' # '''


def _argument_mo():
    return dict(
        vp_console_redirection=dict(
            type='str',
            choices=["com-0", "com-1", "disabled"]),
        vp_terminal_type=dict(
            type='str',
            choices=["pc-ansi", "platform-default", "vt-utf8", "vt100",
                     "vt100-plus"]),
        vp_baud_rate=dict(
            type='str',
            choices=["115200", "19200", "38400", "57600", "9600"]),
        vp_flow_control=dict(
            type='str',
            choices=["none", "rts-cts"]),
        vp_putty_key_pad=dict(
            type='str',
            choices=["ESCN", "LINUX", "SCO", "VT100", "VT400", "XTERMR6"]),
        vp_redirection_after_post=dict(
            type='str',
            choices=["Always Enable", "Bootloader", "platform-default"]),
        vp_legacy_os_redirection=dict(
            type='str',
            choices=["Disabled", "Enabled", "disabled", "enabled",
                     "platform-default"]),
        server_id=dict(type='int',
                       default=1),
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
    from imcsdk.apis.server.bios import bios_serial_config
    from imcsdk.apis.server.bios import bios_serial_exists

    ansible = module.params
    args_mo = _get_mo_params(ansible)
    exists, mo = bios_serial_exists(handle=server, **args_mo)

    if module.check_mode or exists:
        return not exists
    bios_serial_config(handle=server, **args_mo)

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
