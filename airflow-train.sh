echo "设置Minio连接......"
mc config host add minio $MINIO_HOST $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

echo "下载数据......"
mc download $MINIO_BUCKET_NAME ./data
cd ./data
unzip -o *.zip
rm *.zip

echo "训练模型......"
cd ..
rasa train -d data --fixed-model-name $RASA_MODEL_NAME

echo "上传模型......"
mc cp ./models/$RASA_MODEL_NAME minio/$MINIO_MODEL_BUCKET_NAME