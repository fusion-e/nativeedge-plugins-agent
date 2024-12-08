#!/bin/bash

# Copy home template folder if is not initialized
#if [ ! -f /home/docker/.initialized ]; then
#	(
#		rm -rf /home/docker
#		mv /opt/home_docker_tmpl /home/docker
#		chown docker:docker /home/docker
#
#	)
#	touch /home/docker/.initialized
#fi

ls -l /home
ls -l /home/docker
ls -l /home/docker/app

/usr/sbin/sshd -D & python /home/docker/app/app.py

