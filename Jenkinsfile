pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ecommerce-app .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop ecommerce-container || true
                docker rm ecommerce-container || true
                docker run -d \
                    --name ecommerce-container \
                    -p 5000:5000 \
                    ecommerce-app
                '''
            }
        }
    }
}