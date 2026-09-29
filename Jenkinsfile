pipeline {
    agent any

    environment {
        MYSQL_DATABASE = 'car_rental'
        MYSQL_USER = 'caruser'

        MYSQL_ROOT_PASSWORD = credentials('mysql-root-password')
        MYSQL_PASSWORD = credentials('mysql-password')
        FLASK_SECRET_KEY = credentials('flask-secret-key')
    }

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
                    echo "Building Docker image..."
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

        stage('Prepare Kubernetes Image') {
            steps {
                sh '''
                    echo "Saving Docker image..."
                    docker save car-rental-management-system-app:latest \
                        -o /tmp/car-rental-app.tar

                    echo "Loading image into Minikube..."
                    sudo -n /usr/local/bin/jenkins-minikube-load-image

                    echo "Kubernetes image loaded successfully."
                '''
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                sh '''
                    export KUBECONFIG=/var/lib/jenkins/kubeconfig

                    echo "Applying MySQL Kubernetes resources..."
                    kubectl apply -f k8s/mysql.yaml

                    echo "Applying Car Rental application..."
                    kubectl apply -f k8s/app.yaml

                    echo "Restarting application deployment..."
                    kubectl rollout restart deployment/car-rental-app

                    echo "Waiting for application rollout..."
                    kubectl rollout status deployment/car-rental-app --timeout=120s

                    echo "Kubernetes deployment completed."
                '''
            }
        }

        stage('Kubernetes Check') {
            steps {
                sh '''
                    export KUBECONFIG=/var/lib/jenkins/kubeconfig

                    echo "===== PODS ====="
                    kubectl get pods

                    echo "===== SERVICES ====="
                    kubectl get services
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