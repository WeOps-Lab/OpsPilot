docker build -t ccr.ccs.tencentyun.com/megalab/pilot-base -f ./support-files/docker/Dockerfile.base .

cd ./model_server/fast_embed_server
docker build -t ccr.ccs.tencentyun.com/megalab/fast-embed-server .
