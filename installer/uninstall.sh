/usr/local/bin/k3s-uninstall.sh
systemctl stop docker
systemctl disable --now docker
apt-get purge docker-ce docker-ce-cli containerd.io -y
rm -rf /var/lib/docker
rm -Rf /var/lib/containerd/