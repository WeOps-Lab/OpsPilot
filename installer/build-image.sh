docker build -t ccr.ccs.tencentyun.com/megalab/pilot-base -f ./support-files/docker/Dockerfile.base .

cd ./model_server/fast_embed_server
docker build -t ccr.ccs.tencentyun.com/megalab/fast-embed-server .

cd ../bce_rerank_server
docker build -t ccr.ccs.tencentyun.com/megalab/bce-rerank-server .

cd ../classicfy_aiops_server
docker build -t ccr.ccs.tencentyun.com/megalab/classicfy-aiops-server .

cd ../bce_embed_server
docker build -t ccr.ccs.tencentyun.com/megalab/bce-embed-server .

cd ../chunk_server
docker build -t ccr.ccs.tencentyun.com/megalab/chunk-server .
docker push ccr.ccs.tencentyun.com/megalab/chunk-server

cd ../rag_server
docker build -t ccr.ccs.tencentyun.com/megalab/rag-server .

cd ../pandoc_server
docker build -t ccr.ccs.tencentyun.com/megalab/pandoc-server .

cd ../chat_server
docker build -t ccr.ccs.tencentyun.com/megalab/chat-server .
docker push ccr.ccs.tencentyun.com/megalab/chat-server



cd ../../pilot
docker build -t ccr.ccs.tencentyun.com/megalab/pilot .

cd ../munchkin
docker build -t ccr.ccs.tencentyun.com/megalab/munchkin .

cd ../depend/elasticsearch
docker build -t ccr.ccs.tencentyun.com/megalab/pilot-elasticsearch .

cd ./saltstack_server
docker build -t ccr.ccs.tencentyun.com/megalab/saltstack-server .