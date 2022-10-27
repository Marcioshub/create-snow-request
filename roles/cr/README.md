Create Request Role
=========

Calls a python script which reads in and filters a CSV file of inactive users and returns a list of results. From the resulting list a servicenow request will be created for each user.

Requirements
------------

- python
- python-networkdays module installed
- csv file of inactive users
- holidays json file
- the csv file (inactive users) must be in the following order and have the same header names:

| S.No | Display Name | SAM Account Name | When Created | Last Logon Time | Account Status | Account Expiry Time | Manager | OU Name |
| ---- |:------------:| ----------------:| ------------:| ---------------:| --------------:| -------------------:| -------:| -------:|

- the json file (holidays) must be in the following format:

```
[
  {
    "month": "1",
    "day": "1"
  },
  {
    "month": "1",
    "day": "17"
  },
  {
    "month": "2",
    "day": "12"
  },
  ...
]
```

Role Variables
--------------

- SN_HOST
- SN_USERNAME
- SN_PASSWORD
- INACTIVE_USERS_PATH
- CSV_SCRIPT
- HOLIDAYS

Dependencies
------------

- ansible-galaxy collection install servicenow.itsm

Example Playbook
----------------

ansible-playbook snow-playbook.yml

License
-------

MIT

