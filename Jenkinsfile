pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'  // Python virtual environment
    }

    stages {
        stage('Checkout') {
            steps {
                // Only allow trusted branches
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/mueedmak/ssd-lab']]
                ])
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python -m venv $VENV_DIR'
                sh '$VENV_DIR/Scripts/pip install --upgrade pip'
                sh '$VENV_DIR/Scripts/pip install -r requirements.txt'
            }
        }

        stage('Lint & Test') {
            steps {
                sh '$VENV_DIR/Scripts/pip install flake8 pytest'
                sh '$VENV_DIR/Scripts/flake8 .'
                sh '$VENV_DIR/Scripts/pytest'
            }
        }

        stage('Dependency Scan') {
            steps {
                sh '$VENV_DIR/Scripts/pip install safety'
                sh '$VENV_DIR/Scripts/safety check'
            }
        }

        stage('Build & Deploy') {
            steps {
                // Optional: Pull secret from Jenkins credentials
                withCredentials([string(credentialsId: 'FLASK_SECRET_KEY', variable: 'SECRET_KEY')]) {
                    sh 'docker build --build-arg SECRET_KEY=$SECRET_KEY -t flask-app:latest .'
                    sh 'docker run -d -p 5000:5000 flask-app:latest'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            echo 'Pipeline failed. Check errors.'
        }
    }
}
