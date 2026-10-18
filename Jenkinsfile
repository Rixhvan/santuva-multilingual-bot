pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code retrieved from GitHub.'
            }
        }

        stage('Build') {
            steps {
                sh 'docker --version'
                sh 'docker compose version'
                sh 'docker compose -f compose.yaml config --quiet'
            }
        }

        stage('Test/Validate') {
            steps {
                sh 'docker build -f Dockerfile.test -t santuva-test .'
                sh 'docker run --rm santuva-test'
                sh 'docker build -f Dockerfile.frontend -t santuva-frontend-ci .'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker compose -f compose.yaml build'
            }
        }

        stage('Result') {
            steps {
                echo 'RESULT: All CI stages passed successfully.'
            }
        }
    }

    post {
        failure {
            echo 'RESULT: CI pipeline failed. Check the stage logs.'
        }
        always {
            echo 'Santuva CI pipeline execution finished.'
        }
    }
}
