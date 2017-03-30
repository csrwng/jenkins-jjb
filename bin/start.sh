#!/bin/bash

if [[ ! -f ~/.config/jenkins_jobs/jenkins_jobs.ini ]]; then
	export TOKEN="$(oc whoami -t)"
	mkdir -p ~/.config/jenkins_jobs
	cat ~/jenkins_jobs.ini.template | envsubst > ~/.config/jenkins_jobs/jenkins_jobs.ini
fi

oc observe configmaps \
	--names=job-list.py  \
    --delete=job-delete.py -a "{ .metadata.annotations['ci\\.openshift\\.io/jenkins-job'] }" \
	-- job-update.py
