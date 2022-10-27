# Demo of creating request in servicenow
Testing python script and servicenow api with ansible

## Installation of requirements

```bash
ansible-galaxy collection install servicenow.itsm
pip3 install python-networkdays
```

## Usage

```bash
ansible-playbook snow-playbook.yml --ask-vault-pass
```