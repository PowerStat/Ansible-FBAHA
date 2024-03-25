#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Copyright (C) 2024 Dipl.-Inform. Kai Hofmann. All rights reserved!
# Apache License; Version 2.0, January 2004; http://www.apache.org/licenses/
"""
Ansible FRITZ!OS WebGUI login encryption module
"""


DOCUMENTATION = r'''
---
module: fbcrypto
short_description: Fritz!Box crypto for WebGUI login via pbkdf2_hmac.
description: Fritz!Box crypto for WebGUI login via pbkdf2_hmac.
version_added: 1.0.0
options:
  password:
    description: Password
    type: str
    required: true
  challenge:
    description: Challenge
    type: str
    required: true

author: Kai Hofmann (@PowerStat)
'''

EXAMPLES = r'''
  - name: login
    delegate_to: localhost
    uri:
      url: https://{{ server }}/login_sid.lua?version=2
      method: GET
      return_content: true
      validate_certs: false
    register: sessionInfo
      
  - name: get challenge
    set_fact:
      challenge: "{{ sessionInfo.content | regex_search('<Challenge>([0-9a-f$]+)</Challenge>', '\\1') }}"

  - name: calc response
    fbcrypto:
      password: "{{ fbpasswd }}"
      challenge: "{{ challenge[0] }}"
    register: response

  - name: login with response
    delegate_to: localhost
    uri:
      url: "https://{{ server }}/login_sid.lua?version=2&username={{ fbuser }}&response={{ response.response }}"
      method: GET
      return_content: true
      validate_certs: false
    register: sessionInfo2
'''

RETURN = r'''
response:
  description: Reponse to the challenge
  returned: always
  type: str
'''


from ansible.module_utils.basic import AnsibleModule
import hashlib


def run_module():

  module_args = dict(
    password = dict(type = 'str', required = True, no_log = True),
    challenge = dict(type = 'str', required = True),
  )

  module = AnsibleModule(
    argument_spec = module_args,
    #support_check_mode = True
  )

  passwd = module.params['password']
  challenge = module.params['challenge']
  
  result = dict(changed = False, failed = False, response = '')

  parts = challenge.split("$")
  hash1 = hashlib.pbkdf2_hmac("sha256", passwd.encode(), bytes.fromhex(parts[2]), int(parts[1]))
  hash2 = hashlib.pbkdf2_hmac("sha256", hash1, bytes.fromhex(parts[4]), int(parts[3]))

  result['response'] = f"{parts[4]}${hash2.hex()}"
  module.exit_json(**result)


def main():
  run_module()
  
  
if __name__ == '__main__':
  main()
