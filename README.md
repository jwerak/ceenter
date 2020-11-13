# Ceenter

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Ceenter](#ceenter)
    - [Metadata for VM Creation](#metadata-for-vm-creation)
        - [Ansible naming convention](#ansible-naming-convention)
            - [Ansible Playbook names](#ansible-playbook-names)
            - [Ansible Playbook Variable names](#ansible-playbook-variable-names)
            - [Ansible role variable names](#ansible-role-variable-names)
    - [Local setup](#local-setup)
        - [Prerequisites](#prerequisites)
        - [Install Ansible collections](#install-ansible-collections)
        - [Create VM on GCP](#create-vm-on-gcp)
    - [Ansible Tower](#ansible-tower)
        - [Tower setup](#tower-setup)
        - [OpenShift setup](#openshift-setup)
    - [Api Caller](#api-caller)

<!-- markdown-toc end -->

## Metadata for VM Creation

### Ansible naming convention

#### Ansible Playbook names

**Playbook names** are in form of:

*<requesttype>-<servicetype>-<platform>-<operation>.yml*

Example: Create VM on GCP platform

*Service-VM-GCP-Create.yml*

#### Ansible Playbook Variable names

Convention for ceenter external Ansible variable prefixes:

| prefix        | purpose                     |
|---------------|-----------------------------|
| `ceenter_`    | Prefix all variables        |
| `ceenter_vm_` | Prefix for VM related roles |

Ceenter metadata variables for VM Creation:

| variable                    | default value | options                        | purpose                     |
|-----------------------------|---------------|--------------------------------|-----------------------------|
| `ceenter_vm_image`          | centos8       | rhel7, rhel8, centos7, centos8 | Prefix for VM related roles |
| `ceenter_vm_flavor`         | small         | small, medium, large           | Prefix for VM related roles |
| `ceenter_vm_disk_size_gb`   | 30            | number                         | Prefix for VM related roles |
| `ceenter_vm_storage_flavor` | standard      | standard, performance          | Prefix for VM related roles |
| `ceenter_vm_region`         | standard      | standard, performance          | Prefix for VM related roles |

#### Ansible role variable names

Role variable names should be in form: `<role_name>_*`, so for example disk size in *gcp_vm* role will be defined as `gcp_vm_disk_size_gb`.

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

## Ansible Tower

### Tower setup

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

### OpenShift setup

Additional Container Group on OpenShift
- `oc create -n tower -f ocp-setup/role-pod-manager.yml`
- `oc create -n tower -f ocp-setup/sa-tower-container-group.yml`
- `oc create -n tower -f ocp-setup/rb-tower-container-group.yml`

Download serviceaccount credentials, e.g. from ui download serviceaccount kubeconfig.

Customize Pod Spec on Instance Group
```yaml
---
apiVersion: v1
kind: Pod
metadata:
  namespace: tower
spec:
  containers:
    - image: quay.io/ceenter/ansible-runner-google:1.4.6
      tty: true
      stdin: true
      imagePullPolicy: Always
      args:
        - sleep
        - infinity
```

Container image is build in [ansible-runner-images repository](https://github.com/ceenter/ansible-runner-images).

## Api Caller

The API Caller is an example GUI which helps generating the propoer API syntax. Ultimately it may also execute the API call, but not at this stage yet.
The metdata for API Caller is under the api-caller folder. The first file is the menu-map.json where the interactive menu options are defined.
