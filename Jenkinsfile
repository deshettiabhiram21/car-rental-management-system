pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Car Rental Management System...'
                checkout scm
            }
        }

        stage('Python Setup') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r "car-rent/backend/requirements.txt"
                '''
            }
        }

        stage('Application Check') {
            steps {
                sh '''
                    ./venv/bin/python -c "import flask; import flask_sqlalchemy; import flask_login; import pymysql; print('All Python dependencies imported successfully')"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building Docker containers..."
                    docker compose build
                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                sh '''
                    echo "Starting MySQL and Car Rental application..."
                    docker compose up -d
                '''
            }
        }

        stage('Container Check') {
            steps {
                sh '''
                    echo "Checking running containers..."
                    docker compose ps
                '''
            }
        }
    }

    post {
        success {
            echo 'Car Rental CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'Car Rental CI/CD Pipeline failed.'
        }
    }
}