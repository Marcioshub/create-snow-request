#!/usr/local/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import csv
import json 
import datetime
from networkdays import networkdays

DOCUMENTATION = r'''
---
module: filter_users

short_description: Testing python script and servicenow api with ansible

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module filters inactive users from a csv file then 
             returns the output.

options:
    csv:
        description: This is the csv path of the inactive users to send to the test module.
        required: true
        type: str
    holidays:
        description: This is the holidays path to send to the test module.
        required: true
        type: str

author:
    - Marcio Castillo
'''

EXAMPLES = r'''
# Pass in a message
- name: Test this module
  filter_users:
    holidays: holidays.json
    csv: Inactive_Users.csv
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
users:
    changed: True
    failed: False
    message: The following users are have been inactive for 40 days or more
    users: [...]
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        holidays=dict(type='str', required=True),
        csv=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message='',
        users=[]
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    try:
        # load holidays
        h = open(module.params["holidays"], "r")
        holidays = json.load(h)
        HOLIDAYS = set()
        h.close()

        # load holidays into set
        for i in holidays:
            HOLIDAYS.add(datetime.date(2022, int(i["month"]), int(i["day"])))

        c = open(module.params["csv"], "r")
        csvFile = csv.reader(c.readlines())
        c.close()

        # skip header
        next(csvFile)

        # displaying the contents of the CSV file
        for user in csvFile:
            if user[8] != "District Offices/NYC Executive/User Accounts/Commissioners":
                if user[4] != "0":
                    start = user[4].split(" ")[0].split("-") 
                    days = networkdays.Networkdays(
                        datetime.date(int(start[0]), int(start[1]), int(start[2])),
                        datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
                        HOLIDAYS
                    )
                    inactive_days = len(days.networkdays()) - 1
                    if int(inactive_days) >= 45:
                        user_with_days = user
                        user_with_days.append(inactive_days)
                        result["users"].append(user_with_days[1:])

        if len(result["users"]) > 0:
            result["changed"] = True
            result["message"] = "The following users are have been inactive for 45 days or more"
        else:
            result["changed"] = False
            result["message"] = "No inactive users currently in the list"

    except Exception as e:
        result["changed"] = False
        result["message"] = e
        module.fail_json(msg=e, **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()

