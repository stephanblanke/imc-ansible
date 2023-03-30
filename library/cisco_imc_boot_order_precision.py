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
module: cisco_imc_boot_order_precision
short_description: Sets boot order precision for a Cisco IMC server.
version_added: "2.4"
description:
  - Sets boot order precision for a Cisco IMC server
Input Params:
  boot_devices:
    description: dictionary {"order":"", "device-type": "", "name":""}
    required: true

  configured_boot_mode:
    description: Configure boot mode
    default: False
    choices: ["Legacy", "None", "Uefi"]

  reapply:
    description: Configure reapply
    default: "no"
    choices: ["yes", "no"]

  reboot_on_update:
    description: Enable reboot on update
    default: "no"
    choices: ["yes", "no"]

  server_id:
    description: Specify server id for UCS C3260 modular servers
    default: 1

requirements:
    - 'imcsdk'
    - 'python2 >= 2.7.9 or python3 >= 3.2'
    - 'openssl version >= 1.0.1'

author: "Cisco Systems Inc(ucs-python@cisco.com)"
'''


EXAMPLES = '''
- name: Set the boot order precision
  cisco_imc_boot_order_precision:
    boot_devices:
      - {"order":"1", "device-type":"hdd", "name":"hdd"}
      - {"order":"2", "device-type":"pxe", "name":"pxe"}
      - {"order":"3", "device-type":"pxe", "name":"pxe2"}
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''

RETURN = ''' # '''


def _argument_mo():
    return dict(
        boot_devices=dict(
            required=True,
            type='list'),
        configured_boot_mode=dict(
            type='str',
            choices=["Legacy", "None", "Uefi"],
            default="Legacy"),
        reapply=dict(
            type='str',
            choices=["yes", "no"],
            default="no"),
        reboot_on_update=dict(
            type='str',
            choices=["yes", "no"],
            default="no"),
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
    from imcsdk.apis.server.boot import boot_order_precision_set
    from imcsdk.apis.server.boot import boot_order_precision_exists

    ansible = module.params
    args_mo = _get_mo_params(ansible)
    exists, mo = boot_order_precision_exists(handle=server, **args_mo)

    if module.check_mode or exists:
        return not exists
    boot_order_precision_set(handle=server, **args_mo)

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
<<<<<<< HEAD
=======
    module = AnsibleModule(
        argument_spec=dict(
            boot_devices=dict(required=True, type='list'),
            configured_boot_mode=dict(required=False, default="Legacy",
                                      choices=["Legacy", "None", "Uefi"],
                                      type='str'),
            reapply=dict(required=False, default="no", choices=["yes", "no"],
                         type="str"),
            reboot_on_update=dict(required=False, default="no",
                                  choices=["yes", "no"], type="str"),
            server_id=dict(required=False, default=1, type='int'),

            # ImcHandle
            imc_server=dict(required=False, type='dict'),

            # Imc server credentials
            imc_ip=dict(required=False, type='str'),
            imc_username=dict(required=False, default="admin", type='str'),
            imc_password=dict(required=False, type='str', no_log=True),
            imc_port=dict(required=False, default=None),
            imc_secure=dict(required=False, default=None),
            imc_proxy=dict(required=False, default=None)
        ),
        supports_check_mode=True
    )
>>>>>>> 408bfc50ed3ad9733335afe4958ea022df438983

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
