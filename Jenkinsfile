pipeline {
    agent any

    environment {
        IMAGE_NAME = "two-tier-flask"
        DB_PASSWORD = credentials('db-password')   // stored in Jenkins credentials
    }

    triggers {
        githubPush()     // auto-trigger on every push
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/KushalSwaroop64/Two-Tier-App'
            }
        }

        stage('Install & Test') {
            steps {
                sh '''
                    pip install -r app/requirements.txt
                    pytest app/tests/ --tb=short -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy') {
            steps {
                sh '''
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
            echo "Pipeline failed — check test output above"
        }
    }
}