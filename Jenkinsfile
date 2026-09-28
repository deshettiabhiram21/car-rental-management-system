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
                    ./venv/bin/pip install -r "car rent/backend/requirements.txt"
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

        stage('Build') {
            steps {
                echo 'Car Rental application build completed successfully.'
            }
        }
    }

    post {
        success {
            echo 'Car Rental CI Pipeline completed successfully!'
        }

        failure {
            echo 'Car Rental CI Pipeline failed.'
        }
    }
}
