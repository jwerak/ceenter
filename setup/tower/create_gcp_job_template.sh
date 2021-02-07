#!/usr/bin/bash

# This script is creating surveys in job templates
# To be rewritten to ansible later
# Using .netrc file for authentication

SURVEY_CREATE_SPEC_FILE="./data/gcp_vm_create_survey_spec.json"
SURVEY_DELETE_SPEC_FILE="./data/gcp_vm_delete_survey_spec.json"
TOWER_HOST=${TOWER_HOST-"https://localhost"}

curl -X POST -H "Content-Type: application/json" -k -n ${TOWER_HOST}/api/v2/job_templates/Service-VM-GCP-Create/survey_spec/ -d @${SURVEY_CREATE_SPEC_FILE}

curl -X POST -H "Content-Type: application/json" -k -n ${TOWER_HOST}/api/v2/job_templates/Service-VM-GCP-Delete/survey_spec/ -d @${SURVEY_DELETE_SPEC_FILE}
