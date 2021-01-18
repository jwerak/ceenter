# Ceenter

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Ceenter](#ceenter)
    - [Ansible naming convention](#ansible-naming-convention)
        - [Ansible Tower Job Template naming](#ansible-tower-job-template-naming)
        - [Ansible Playbook naming](#ansible-playbook-naming)
        - [Ansible Playbook Variable names](#ansible-playbook-variable-names)
        - [Ansible role variable names](#ansible-role-variable-names)
    - [Local setup](#local-setup)
        - [Prerequisites](#prerequisites)
        - [Install Ansible collections](#install-ansible-collections)
        - [Create VM on GCP](#create-vm-on-gcp)
        - [Manual Tower setup](#manual-tower-setup)
            - [Use awx cli tool](#use-awx-cli-tool)
            - [Setup Job Templates](#setup-job-templates)
                - [Create GCP VM](#create-gcp-vm)
    - [OpenShift setup](#openshift-setup)
    - [Api Caller](#api-caller)
        - [Example API Call to Ansible Tower](#example-api-call-to-ansible-tower)

<!-- markdown-toc end -->

## Ansible naming convention ##

### Ansible Tower Job Template naming ###

**Job Template names** are in form of:

*<requesttype>-<servicetype>-<platform>-<operation>*

Example: Create VM on GCP platform

*Service-VM-GCP-Create*

Job Template must accept extra variables defined as part of API Caller.

### Ansible Playbook naming ###

**Playbook names** are in form of:

*<requesttype>-<servicetype>-<platform>-<operation>.yml*

Example: Create VM on GCP platform

*Service-VM-GCP-Create.yml*

### Ansible Playbook Variable names ###

Ceenter metadata variables for VM Creation:

| variable            | description                                         | default value | options                        | purpose                     | status      |
|---------------------|-----------------------------------------------------|---------------|--------------------------------|-----------------------------|-------------|
| *vm_flavor*         | VM Flavor                                           | Small         | Small, Medium, Large           | Prefix for VM related roles | implemented |
| *vm_cpu*            | Number of virtual CPUs (exclusive with *vm_flavor*) | 1             | INT                            | Prefix for VM related roles | implemented |
| *vm_memory*         | memory in GB (exclusive with *vm_flavor*)           | 1             | INT                            | Prefix for VM related roles | implemented |
| *vm_disk_size*      | disk size                                           | 30            | INT                            | Prefix for VM related roles | implemented |
| *vm_OS*             | OS type                                             | centos8       | rhel7, rhel8, centos7, centos8 | Prefix for VM related roles | TBD         |
| *vm_storage_flavor* | performance of vm storage                           | standard      | standard, performance          | Prefix for VM related roles | TBD         |
| *ceenter_vm_region* | geographical region                                 | standard      | standard, performance          | Prefix for VM related roles | TBD         |

### Ansible role variable names ###

Role variable names should be in form: `<role_name>_*`, so for example disk size in *gcp_vm* role will be defined as `gcp_vm_disk_size_gb`.

## Local setup

Steps to prepare local environment.

### Prerequisites

ansible 2.9+

### Install Ansible collections

Configure ansible.cfg:
Download ansible-hub token from https://cloud.redhat.com/ansible/automation-hub/token

Save token locally to *~/.ansible/galaxy_token*.

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


### Manual Tower setup ###

Create Credential:
- GCP connection
- Github
- RHV

Create Project:
- Ceenter Repo (https://github.com/ceenter/ceenter.git)

Create Job Templates:
- GCP Create VM
- RHV Create VM

Authenticate Ansible Tower to Automation-hub:
- Retrieve token at https://cloud.redhat.com/ansible/automation-hub/token
- Update token in Ansible Tower: https://www.ansible.com/blog/installing-and-using-collections-on-ansible-tower

#### Use awx cli tool ####

Install awx https://docs.ansible.com/ansible-tower/latest/html/towercli/usage.html#installation.

Tool awx doesn't have any local config file to store credentials, but you can export your credentials in local file.

You can use simple script to auth to Tower and use save auth key:
```bash
./utils/awx_login.py <TOWER_HOST> <TOWER_USER> <TOWER_PASSWORD> > ~/.awx_conf.env
source ~/.awx_conf.env
# Test config
awx activity_stream list
```

or create file manually:
```bash
cat > ~/.awx_conf.env <<EOF
export TOWER_HOST=${TOWER_HOST}
export TOWER_VERIFY_SSL=False
export TOWER_USERNAME=${TOWER_USERNAME}
export TOWER_OAUTH_TOKEN=${TOWER_OAUTH_TOKEN}
EOF
```

#### Setup Job Templates ####

##### Create GCP VM #####

Create Job Template:

```yaml
name: GCP VM Create
description: Create VM on GCP
job_type: Run
inventory: localhost
project: Ceenter Repo
Playbook: Service-VM-GCP-Create.yml
credentials: ['gcp-jveverka']
instance_group: Container with google auth
```

Create Survey for Job Template:

```yaml
Parameters: {"vm_name":"mytest","vm_flavor":"Small","vm_memory":2,"vm_cpu":1,"vm_disk_size":20}
```


## OpenShift setup ##

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

## Api Caller ##

The API Caller is an example GUI which helps generating the propoer API syntax. Ultimately it may also execute the API call, but not at this stage yet.
The metdata for API Caller is under the api-caller folder. The first file is the menu-map.json where the interactive menu options are defined.

### Example API Call to Ansible Tower ###

Launch Job *Service-VM-GCP-Create* with Curl:

```bash
curl -k -X POST --user admin:<PASSWORD> https://<TOWER_URL>/api/v2/job_templates/Service-VM-GCP-Create/launch/
```
