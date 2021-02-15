#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: my_test

short_description: This is my test module

version_added: "2.4"

description:
    - "This is my longer description explaining my test module"

options:
    name:
        description:
            - This is the message to send to the test module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

import requests
from lxml import html

def getAPIkey(serverIP, serverPort, username, password):

    url = 'https://' + str(serverIP) + ':' + str(serverPort)
    loginUrl = url + '/login'

    apiUrl = url + '/settings'

    credentials = {
        'username': username,
        'password': password
    }

    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    referer = 'https://' + serverIP
    header = {
        'User-Agent': userAgent,
        'referer': referer
    }

    with requests.Session() as session:

        result = session.get(loginUrl, verify=False)

        tree = html.fromstring(result.text)
        csrfToken = list(set(tree.xpath("//input[@name='csrf_token']/@value")))[0]

        payload = {
            'username': username,
            'password': password,
            'csrf_token': csrfToken
        }

        post = session.post(loginUrl, data=payload, verify=False, headers=header)
        response = session.get(apiUrl, verify=False, headers=header)



        result = {}
        if response.status_code == 200:
            tree = html.fromstring(response.text)
            apiKey = list(set(tree.xpath("//input[@id='api_key']/@value")))[0]
            apiKey = str(apiKey)


            result['apiKey'] = apiKey
        else:
            result['Error'] = str(response.status_code) + str(response)
#    result['apiKey'] = '123'
    return result

def run_module():

    module_args = dict(srvIP=dict(type='str', required=True),
        srvPort=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True))
    result = dict(changed=False, apiKey='')
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

#        res = dict('apiKey'='123')
    res = {}

    res = getAPIkey(module.params['srvIP'], module.params['srvPort'], module.params['username'], module.params['password'])

    if(res['apiKey']):
        result['apiKey'] = res['apiKey']
    else:
        module.fail_json(msg='Unable get API key', **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
