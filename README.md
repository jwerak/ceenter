# Technical

Technical repo for Ceenter infrastructure

## Local setup

Steps to prepare local environment.

### Prerequisites

ansible 2.9+

### Install Ansible collections

Configure ansible.cfg:
Download ansible-hub token from https://cloud.redhat.com/ansible/automation-hub/token

update ansible.cfg to include:
``` ini
[defaults]
collections_paths = ./collections

[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://cloud.redhat.com/api/automation-hub/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Install dependent collections
```shell
ansible-galaxy collection install -r ./collections/requirements.yml
```

Detailed [blog about setting up env](https://www.ansible.com/blog/hands-on-with-ansible-collections) for automation-hub collections.

Install google.cloud requirements:

``` shell
yum install python-requests
pip install requests google-auth
```

Download [GCP credentials](https://docs.ansible.com/ansible/latest/scenario_guides/guide_gce.html#credentials).

### Create VM on GCP

``` shell
ansible-playbook GCP_VM_Create.yml
```

## Ansible Tower Setup

Create Credential:
- GCP connection
- Github
- RHV

Create Project:
- technical

Create Job Templates:
- GCP Create VM
- RHV Create VM

Authenticate Ansible Tower to Automation-hub:
- Retrieve token at https://cloud.redhat.com/ansible/automation-hub/token
- Update token in Ansible Tower: https://www.ansible.com/blog/installing-and-using-collections-on-ansible-tower
