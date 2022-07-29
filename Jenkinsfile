pipeline {
  agent {
    label 'devops' // Jenkins agent label
  }
  environment {
    AWS_ACCESS_KEY_ID = credentials('aws_key_access')
    AWS_SECRET_ACCESS_KEY = credentials('aws_secret_key')
  }
  stages {
    stage('Create Project Folder') {
      steps {
        sh 'mkdir -p -m a=rwx cdk_apache'
      }
    }
    stage('Initialize CDK Project') {
      steps {
        dir('cdk_apache') {
          sh 'cdk init app --language python'
          sh 'export PYTHONPATH=$PWD/.venv/bin/python3.9'
          // Copy customized scripts and app code for the project
          sh 'cp ../app.py ../user_data.sh .'
          sh 'cp ../cdk_apache_stack.py cdk_apache/'
        }
      }
      post {
        failure {
          cleanWs()
          echo 'Project initialization failed'
        }
        success {
          echo 'CDK project has been initialized successfully'
        }
      }
    }
    stage('Build AWS Resources Through a Virtual Environment') {
      steps {
        dir('cdk_apache') {
          sh '. .venv/bin/activate && pip3 install -r requirements.txt'
          sh 'cdk deploy --require-approval never'
        }
      }
      post {
        failure {
          sh 'cdk destroy --force'
          cleanWs()
        }
        success {
          echo 'Apache Virtual Machine Deployed'
          echo '5 minutes until proceed with the Clean Infrastructure & Workspace stage'
          sleep(time: 5, unit: "MINUTES")
        }
      }
    }
    stage('Clean Infrastructure & Workspace') {
      steps {
        dir('cdk_apache') {
          sh 'cdk destroy --force'
          echo 'AWS resources destroyed!'
        }  
      }
      post {
        failure {
          echo 'The AWS resources were not destroyed! Please delete them manually through AWS console'
        }
        success {
          cleanWs()
          echo 'Jenkins Workspace has been wipe out'
        }
      }
    }
  }
}