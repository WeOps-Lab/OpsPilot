read -p "Enter the Public IP address of the server: " PUBLIC_IP

echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
echo "source /etc/bash_completion" >> /etc/profile
echo "source <(kubectl completion bash)" >> /etc/profile
sysctl -p

export INSTALL_K3S_EXEC="--disable metrics-server --tls-san $PUBLIC_IP --node-ip $PUBLIC_IP --node-external-ip $PUBLIC_IP --flannel-backend wireguard-native --flannel-external-ip --service-node-port-range 1-65535 --docker"

curl https://releases.rancher.com/install-docker/20.10.sh | sh
curl -sfL https://get.k3s.io | sh -s - --docker

kubectl create ns ops-pilot
kubectl apply -f ./depend/postgres.yml
kubectl apply -f ./depend/rabbitmq.yml
kubectl apply -f ./depend/elasticsearch.yml
kubectl apply -f ./depend/minio.yml