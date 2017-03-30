#!/usr/bin/python

from __future__ import print_function
import sys
import kubernetes.client
import base64
import tempfile
import os
from subprocess import call

from kubernetes.client.rest import ApiException
import oc_common
import jobs_common

def main(argv):
    if len(argv)==0:
        print('No arguments passed. Please specify a namespace, name, and value of ci.openshift.io/jenkins-job annotation')
    elif len(argv)==3:
        process_config(argv[0], argv[1], argv[2])

def process_config(namespace, name, annotation_value=None):
    if (not annotation_value) or (annotation_value != "true"):
        print("configmap %s/%s is not applicable to Jenkins" % (namespace, name))
        return

    core_instance = oc_common.connect_to_kube_core()    

    try:
        config_map = core_instance.read_namespaced_config_map(name, namespace)
    except ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_configmap: %s\n" % e)
        exit(1)

    if len(config_map.data) != 1:
        print("Invalid config map %s/%s: more than one data key present\n" % (namespace, name))

    tempdir = tempfile.mkdtemp()
    filename = config_map.data.keys()[0]
    localname = os.path.join(tempdir, filename)
    jobfile = open(localname, "w")
    jobfile.write(config_map.data[filename])
    jobfile.close()

    call("jenkins-jobs", "update", localname)
    jobs_common.add_to_known_names(namespace, name)

if __name__ == "__main__":
    main(sys.argv[1:])
