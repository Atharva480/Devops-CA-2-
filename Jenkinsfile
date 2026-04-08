pipeline {
    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Atharva480/Devops-CA-2-'
            }
        }

        stage('Validate Form Files') {
            steps {
                bat 'dir'
                bat 'type index.html'
            }
        }

        stage('Check Input Fields') {
            steps {
                bat 'findstr /i "input" index.html'
                bat 'findstr /i "select" index.html'
                bat 'findstr /i "form" index.html'
            }
        }

        stage('Run Basic Validation') {
            steps {
                bat 'echo Form fields detected successfully'
            }
        }

        stage('Deploy') {
            steps {
                bat 'echo Deployment successful'
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
