OCP_Project
===========

Ansible role to create or remove OpenShift Project (AKA kubernetes namespace).

Requirements
------------

Connection to OpenShift cluster with privileges for Project creation, e.g. [self-provisioner](https://docs.openshift.com/container-platform/4.7/authentication/using-rbac.html).

Role Variables
--------------

* **ocp_project_name**: Project's name.
* **ocp_project_display_name**: Name shown in OpenShift web console.
* **ocp_project_description**: Longer description shown in OpenShift web console.

Dependencies
------------

None

Example Playbook
----------------

``` yaml
- hosts: localhost
  connection: local
  roles:
    - ocp_project:
      vars:
        project_name: foobar
```

License
-------

GPLv3
