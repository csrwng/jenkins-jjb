FROM openshift/origin:latest

USER root

RUN yum -y install python-pip

RUN git clone -b bearer_token https://github.com/csrwng/jenkins-job-builder.git && \
    cd jenkins-job-builder && \
    pip install .

RUN mkdir /home/user && \
    chmod g+rwx /home/user

WORKDIR /home/user

ENV JENKINS_SERVICE_URL="http://jenkins" \
    HOME=/home/user

ENTRYPOINT ["/bin/bash", "-c", "while(true); do date; sleep 30; done"]
