pipeline {
    agent {
        label 'ops-pilot'
    }

    environment {
        NOTIFICATION_URL = credentials('NOTIFICATION_URL')
    }

    stages {
        stage('下载代码') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/WeOps-Lab/OpsPilot.git'
            }
        }

        stage('构建基础服务镜像') {
            steps {
                dir('support-files/docker') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pilot-base -f ./Dockerfile.base .'
                }

                dir('depend/elasticsearch') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pilot-elasticsearch .'
                }

                dir('depend/saltstack_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/saltstack-server .'
                }

                dir('depend/bionics') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/bionics .'
                }
            }
        }

        stage('构建Model Servers') {
            steps {
                dir('model_server/bce_embed_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/bce-embed-server .'
                }

                dir('model_server/bce_rerank_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/bce-rerank-server .'
                }

                dir('model_server/chat_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/chat-server .'
                }

                dir('model_server/chunk_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/chunk-server .'
                }

                dir('model_server/classicfy_aiops_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/classicfy-aiops-server .'
                }

                dir('model_server/fast_embed_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/fast-embed-server .'
                }

                dir('model_server/ocr_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/ocr-server .'
                }

                dir('model_server/pandoc_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pandoc-server .'
                }

                dir('model_server/rag_server') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/rag-server .'
                }
            }
        }

        stage('构建Pilot') {
            steps {
                dir('pilot') {
                    sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pilot .'
                }
            }
        }

        stage('构建Munchkin') {
            steps {
                dir('munchkin') {
                    sh '''
                        mkdir -p templates
                        sudo docker build -t ccr.ccs.tencentyun.com/megalab/munchkin .
                    '''
                }
            }
        }
    }

    post {
        success {
            sh '''
                curl -X POST $NOTIFICATION_URL \
                -H 'Content-Type: application/json' \
                -d '{
                    "content": "OpsPilot 构建成功"
                }'
            '''
        }
        failure {
            sh '''
                curl -X POST $NOTIFICATION_URL \
                -H 'Content-Type: application/json' \
                -d '{
                    "content": "OpsPilot 构建失败"
                }'
            '''
        }
    }
}