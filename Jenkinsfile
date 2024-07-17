node('ops-pilot'){
    stage('下载代码'){
        git branch: 'main',
            url: 'https://github.com/WeOps-Lab/OpsPilot.git'
    }

    stage('构建基础服务镜像'){

        dir('depend/elasticsearch'){
            sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pilot-elasticsearch .'
        }

        dir('depend/saltstack_server'){
            sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/saltstack-server .'
        }

        dir('depend/bionics'){
            sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/bionics .'
        }
    }

    stage('构建Pilot'){
        dir('pilot'){
            sh 'sudo docker build -t ccr.ccs.tencentyun.com/megalab/pilot .'
        }
    }
}