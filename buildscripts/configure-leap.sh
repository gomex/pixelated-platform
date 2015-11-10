#!/bin/bash

# exit on any error
set -e
set -x 

usage() { echo "Usage: $0 [-p to use try.pixelated-project.org defaults]" 1>&2; exit 1; }

USE_PIXELATED_DEFAULTS=
while getopts "hp" OPT; do
	case $OPT in
		p)
			USE_PIXELATED_DEFAULTS=1
			;;
		*)
			usage
			;;
	esac
done
shift $((OPTIND-1))

LEAP_OPTS=''
LEAP_CONFIG='/home/leap/configuration/'

echo "==============================================="
echo "configuring leap"
echo "==============================================="
sudo mkdir -p $LEAP_CONFIG
ME=$USER
sudo chown $ME $LEAP_CONFIG
cd $LEAP_CONFIG

if [ -n "$USE_PIXELATED_DEFAULTS" ] ; then
	leap $LEAP_OPTS new --contacts no-reply@try.pixelated-project.org --domain try.pixelated-project.org --name LEAP_Example --platform=/home/leap/leap_platform .
else
	leap $LEAP_OPTS new --platform=/home/leap/leap_platform .
fi
echo -e '\n@log = "/var/log/leap/deploy.log"' >> Leapfile
sudo mkdir -p /var/log/leap
ssh-keygen -f ~/.ssh/id_rsa -P ""
sudo mkdir -p /root/.ssh
sudo sh -e -c "cat $HOME/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys"
mkdir -p $LEAP_CONFIG/files/nodes/pixelated
sh -c 'cat /etc/ssh/ssh_host_rsa_key.pub | cut -d" " -f1,2 >> /home/leap/configuration/files/nodes/pixelated/pixelated_ssh.pub'
leap $LEAP_OPTS add-user --self
leap $LEAP_OPTS cert ca
leap $LEAP_OPTS cert csr
leap $LEAP_OPTS node add pixelated ip_address:"$(facter ipaddress)"  services:webapp,mx,couchdb,soledad,monitor couch.master:true couch.pwhash_alg:pbkdf2 tags:production

echo '{ "webapp": { "admins": ["testadmin"] } }' > services/webapp.json

leap $LEAP_OPTS compile

git config --global user.email "go-ci@pixelated-project.org"
git config --global user.name "Pixelated CI"
git init
git add .
git commit -m"configured provider"


mkdir -p file/puppet/modules/custom/manifests
cat << EOF > files/puppet/modules/custom/manifests/init.pp
class custom {
  include pixelated::dispatcher
}
EOF

git submodule add https://github.com/pixelated/puppet-pixelated.git files/puppet/modules
git add files/puppet/modules
git commit -m 'added pixelated submodule'

leap $LEAP_OPTS node init pixelated
if [ $? -eq 1 ]; then
  echo "node init failed"
  exit 1
fi

leap $LEAP_OPTS -v 2 deploy
if [ $? -eq 1 ]; then
  echo "deploy failed"
  exit 1
fi

set +e
git add .
git commit -m"initialized and deployed provider"
set -e

echo "==============================================="
echo "testing the platform"
echo "==============================================="

leap $LEAP_OPTS -v 2 test --continue

echo "==============================================="
echo "setting node to demo-mode"
echo "==============================================="
sudo postconf -e default_transport="error: in demo mode"

sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo /etc/init.d/ssh reload

# add users: testadmin and testuser with passwords "hallo123"
curl -s -k https://localhost/1/users.json -d "user%5Blogin%5D=testuser&user%5Bpassword_salt%5D=7d4880237a038e0e&user%5Bpassword_verifier%5D=b98dc393afcd16e5a40fb57ce9cddfa6a978b84be326196627c111d426cada898cdaf3a6427e98b27daf4b0ed61d278bc856515aeceb2312e50c8f816659fcaa4460d839a1e2d7ffb867d32ac869962061368141c7571a53443d58dc84ca1fca34776894414c1090a93e296db6cef12c2cc3f7a991b05d49728ed358fd868286"
curl -s -k https://localhost/1/users.json -d "user%5Blogin%5D=testadmin&user%5Bpassword_salt%5D=ece1c457014d8282&user%5Bpassword_verifier%5D=9654d93ab409edf4ff1543d07e08f321107c3fd00de05c646c637866a94f28b3eb263ea9129dacebb7291b3374cc6f0bf88eb3d231eb3a76eed330a0e8fd2a5c477ed2693694efc1cc23ae83c2ae351a21139701983dd595b6c3225a1bebd2a4e6122f83df87606f1a41152d9890e5a11ac3749b3bfcf4407fc83ef60b4ced68"

echo "==============================================="
echo "cleaning up"
echo "==============================================="
sync
sleep 10
