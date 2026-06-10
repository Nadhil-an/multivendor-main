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

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag foodonline-ci nadilan/foodonline-ci:latest'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push nadilan/foodonline-ci:latest'
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