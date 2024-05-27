// A very simple JenkinsFile to deploy the containers Locally (Windows Envs)
pipeline {
    agent any
    
    environment {
        GIT_REPO = 'https://github.com/KNrodrigo/LaneD-Models-App.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout  code from GitHub using my token credentials
                git url: "${GIT_REPO}", branch: 'main', credentialsId: 'jenkins'
            }
        }
        
        stage('Build and Run Docker Compose') {
            steps {
                script {

                    bat 'docker --version'
                    bat 'docker-compose --version'
                    bat 'docker-compose down'  
                    bat 'docker-compose up -d'  
                }
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
