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