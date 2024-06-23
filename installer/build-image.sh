docker build -t ccr.ccs.tencentyun.com/megalab/pilot-base -f ./support-files/docker/Dockerfile.base .

cd ./model_server/fast_embed_server
docker build -t ccr.ccs.tencentyun.com/megalab/fast-embed-server .

cd ../bce_rerank_server
docker build -t ccr.ccs.tencentyun.com/megalab/bce-rerank-server .

cd ../chunk_server
docker build -t ccr.ccs.tencentyun.com/megalab/chunk-server .

cd ../pandoc_server
docker build -t ccr.ccs.tencentyun.com/megalab/pandoc-server .

cd ../bce_embed_server
docker build -t ccr.ccs.tencentyun.com/megalab/bce-embed-server .

cd ../../../pilot
docker build -t ccr.ccs.tencentyun.com/megalab/pilot .

cd ../munchkin
docker build -t ccr.ccs.tencentyun.com/megalab/munchkin-base -f ./Dockerfile.base .
docker build -t ccr.ccs.tencentyun.com/megalab/munchkin .