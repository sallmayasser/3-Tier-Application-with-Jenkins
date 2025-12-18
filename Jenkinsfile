pipeline {
    agent any

    environment {
        POSTGRES_USER = credentials('pg_user')
        POSTGRES_PASSWORD = credentials('pg_password')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sallmayasser/3-Tier-Application-with-Jenkins.git'
            }
        }
        stage('Build Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Verify') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
