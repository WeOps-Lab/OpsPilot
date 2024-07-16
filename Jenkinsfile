node('ops-pilot'){
    stage('下载代码'){
        git branch: 'main',
            url: 'https://github.com/WeOps-Lab/OpsPilot.git'
    }

    stage('构建elasticsearch镜像'){
        dir('depend/elasticsearch'){
            sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pilot-elasticsearch .'
        }
    }

    stage('构建SaltStack Server镜像'){
        dir('depend/saltstack_server'){
            sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/saltstack-server .'
        }
    }
}
