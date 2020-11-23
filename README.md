Ceenter is Awesome!

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

The API Caller is an example GUI which help generating the propoer API syntax. Ultimately it may also execute the API call, but not at this stage yet.
The metdata for API Caller is under the api-caller folder. The first file is the menu-map.json where the interactive menu options are defined.


