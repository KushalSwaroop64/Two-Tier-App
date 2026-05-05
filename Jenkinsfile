pipeline {
    agent any

    environment {
        IMAGE_NAME = "two-tier-flask"
        DB_PASSWORD = credentials('db-password')
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/KushalSwaroop64/Two-Tier-App.git'
            }
        }

        stage('Install & Test') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r app/requirements.txt
                    python3 -m pytest app/tests/ --tb=short -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    export PATH=/usr/local/bin:$PATH
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    export PATH=/usr/local/bin:$PATH
                    export DB_PASSWORD=${DB_PASSWORD}
                    docker compose down --remove-orphans
                    docker compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful — build #${BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline failed — check logs above"
        }
    }
}