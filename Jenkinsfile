pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t foodonline-ci .'
            }
        }

        stage('Verify Image') {
            steps {
                sh 'docker images | grep foodonline-ci'
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'cp .env.example .env.dev'
            }
        }

        stage('Django Check') {
            steps {
                sh 'docker run --rm --env-file .env.dev foodonline-ci python manage.py check'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm --env-file .env.dev foodonline-ci python manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker compose down
                docker compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}