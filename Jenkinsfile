pipeline {
    agent any

    environment {
        APP_NAME = "Devops-CA-2"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Atharva480/Devops-CA-2-'
            }
        }

        stage('Build') {
            steps {
                echo "Building ${APP_NAME}..."
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying ${APP_NAME}..."
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully ✅'
        }

        failure {
            echo 'Pipeline failed ❌'
        }
    }
}
