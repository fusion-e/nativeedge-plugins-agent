FROM korenlev/base:latest

ENV USER=docker
ENV HOME=/home/$USER
USER root
RUN adduser $USER || true
RUN apt-get update && apt-get install fuse sudo sed apt-utils vim openssh-server gzip git -y
RUN ssh-keygen -A && mkdir -p /run/sshd
RUN usermod -aG sudo $USER && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && touch /home/$USER/.sudo_as_admin_successful
RUN echo "$USER:$USER" |chpasswd
RUN rm $HOME/.ssh && mkdir $HOME/.ssh ; chmod 700 $HOME/.ssh
COPY known_hosts $HOME/.ssh/
RUN chown -R $USER:$USER $HOME/.ssh
COPY run.sh /
RUN chmod 755 /run.sh

USER $USER
RUN mkdir -p $HOME/app
WORKDIR $HOME/app
COPY app.py $HOME/app/
COPY requirements.txt $HOME/app/
RUN echo building as $(whoami)
RUN echo $(which python)
ENV PATH=$HOME/.local/bin:$PATH

RUN /usr/local/bin/python -m pip install --disable-pip-version-check --upgrade pip
RUN pip install -r requirements.txt --disable-pip-version-check

USER root

# Move home folder as template, real home folder will be mounted as PV during deployment process
# RUN mv /home/$USER /opt/home_${USER}_tmpl

# ports to access the service
EXPOSE 5000 22

# running the application service inside the container with sshd
ENTRYPOINT ["/run.sh"]


