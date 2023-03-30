<<<<<<< HEAD
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
=======
#!/usr/bin/env python

from ansible.module_utils.basic import *
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983


DOCUMENTATION = '''
---
module: cisco_imc_vmedia
<<<<<<< HEAD
short_description: Configures vMedia on a Cisco IMC server
version_added: "2.4"
description:
    - Configures vMedia mapping on a Cisco IMC server
Input Params:
    state:
        description:
         - if C(present), enables vMedia
         - if C(absent), disables vMedia
        choices: ['present', 'absent']
        default: "present"

    encryption_state:
        description: encryption state
        choices: ['enabled', 'disabled']

    low_power_usb:
        description: low power usb state
        choices: ['enabled', 'disabled']

    server_id:
        description: Server Id to be specified for C3260 platforms
        default: 1

requirements:
    - 'imcsdk'
    - 'python2 >= 2.7.9 or python3 >= 3.2'
    - 'openssl version >= 1.0.1'

author: "Cisco Systems Inc(ucs-python@cisco.com)"
=======
short_description: Configures vmedia on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Configures the vmedia on a Cisco IMC Server
Input Params:
    encryption_state:
        description: Encrypt virtual media communications
        required: False
        choices: ['disabled', 'enabled']
        default: "disabled"
    low_power_usb:
        description: Enable low power usb
        required: False
        choices: ['disabled', 'enabled']
        default: "disabled"
    server_id:
        description: Server Id to be specified for C3260 platforms
        required: False
        default: "1"

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983
'''


EXAMPLES = '''
<<<<<<< HEAD
- name: enable vMedia
  cisco_imc_vmedia:
    encryption_state: disabled
    low_power_usb: disabled
    state: present
=======
- name:
  cisco_imc_vmedia:
    encryption_state:
    low_power_usb:
    server_id:
    state: "present"
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''

<<<<<<< HEAD
RETURN = ''' # '''


def _argument_mo():
    return dict(
        encryption_state=dict(
            type='str',
            choices=["disabled", "enabled"]),
        low_power_usb=dict(
            type='str',
            choices=["disabled", "enabled"]),
        server_id=dict(type='int',
                       default=1),
    )


def _argument_custom():
    return dict(
        state=dict(default="present",
=======

def _argument_mo():
    return dict(
                encryption_state=dict(required=False, type='str', choices=['disabled', 'enabled'], default="disabled"),
                low_power_usb=dict(required=False, type='str', choices=['disabled', 'enabled'], default="disabled"),
                server_id=dict(required=False, type='str', default="1"),
    )


def _argument_state():
    return dict(
        state=dict(required=False,
                   default="present",
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983
                   choices=['present', 'absent'],
                   type='str'),
    )


<<<<<<< HEAD
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
=======
def _argument_imc_connection():
    return  dict(
        # ImcHandle
        imc_server=dict(required=False, type='dict'),

        # Imc server credentials
        imc_ip=dict(required=False, type='str'),
        imc_username=dict(required=False, default="admin", type='str'),
        imc_password=dict(required=False, type='str', no_log=True),
        imc_port=dict(required=False, default=None),
        imc_secure=dict(required=False, default=None),
        imc_proxy=dict(required=False, default=None)
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983
    )


def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_mo())
<<<<<<< HEAD
    argument_spec.update(_argument_custom())
    argument_spec.update(_argument_connection())
=======
    argument_spec.update(_argument_state())
    argument_spec.update(_argument_imc_connection())
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
<<<<<<< HEAD
    args = {}
    for key in _argument_mo():
        if params.get(key) is None:
=======
    from ansible.module_utils.cisco_imc import ImcConnection
    args = {}
    for key in params:
        if (key == 'state' or
            ImcConnection.is_login_param(key) or
            params.get(key) is None):
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983
            continue
        args[key] = params.get(key)
    return args


<<<<<<< HEAD
def setup_module(server, module):
    from imcsdk.apis.server.vmedia import vmedia_enable
    from imcsdk.apis.server.vmedia import vmedia_disable
    from imcsdk.apis.server.vmedia import vmedia_exists

    ansible = module.params
    args_mo = _get_mo_params(ansible)
    exists, mo = vmedia_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists
        vmedia_enable(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists
        vmedia_disable(server)
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
=======
def setup_vmedia(server, module):
    from imcsdk.apis.server.remotepresence import vmedia_setup
    from imcsdk.apis.server.remotepresence import vmedia_disable
    from imcsdk.apis.server.remotepresence import is_vmedia_enabled

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = is_vmedia_enabled(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists, False
        vmedia_setup(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists, False
        vmedia_disable(server)

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_vmedia(server, module)

    except Exception as e:
        err = True
        results["msg"] = "setup error: %s " % str(e)
        results["changed"] = False

    return results, err
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983


def main():
    from ansible.module_utils.cisco_imc import ImcConnection

    module = _ansible_module_create()
    conn = ImcConnection(module)
    server = conn.login()
<<<<<<< HEAD
    result, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**result)
    module.exit_json(**result)
=======
    results, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983


if __name__ == '__main__':
    main()
<<<<<<< HEAD
=======

>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983
