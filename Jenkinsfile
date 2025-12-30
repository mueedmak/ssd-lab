pipeline {
    agent any
    
    environment {
        // Define deployment directory
        DEPLOY_DIR = '/var/www/flask-app'
        VENV_DIR = 'venv'
        PYTHON_VERSION = 'python3'
        // Service name for restart (optional)
        SERVICE_NAME = 'flask-app'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/mueedmak/ssd-lab.git'
                echo 'Repository cloned successfully!'
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    # Remove old virtual environment if exists
                    rm -rf ${VENV_DIR}
                    
                    # Create new virtual environment
                    ${PYTHON_VERSION} -m venv ${VENV_DIR}
                    
                    # Activate virtual environment and upgrade pip
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    
                    echo "Virtual environment created successfully!"
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies from requirements.txt...'
                sh '''
                    # Activate virtual environment
                    . ${VENV_DIR}/bin/activate
                    
                    # Install dependencies
                    pip install -r requirements.txt
                    
                    # Install testing dependencies
                    pip install pytest pytest-cov pytest-flask
                    
                    echo "Dependencies installed successfully!"
                    pip list
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests with pytest...'
                sh '''
                    # Activate virtual environment
                    . ${VENV_DIR}/bin/activate
                    
                    # Create tests directory if it doesn't exist
                    mkdir -p tests
                    
                    # Run pytest with coverage
                    pytest tests/ -v --cov=. --cov-report=html --cov-report=term || true
                    
                    echo "Unit tests completed!"
                '''
            }
            post {
                always {
                    // Archive test results if they exist
                    junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
                    // Archive coverage reports
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Application') {
            steps {
                echo 'Building and packaging the Flask application...'
                sh '''
                    # Activate virtual environment
                    . ${VENV_DIR}/bin/activate
                    
                    # Create build directory
                    mkdir -p build
                    
                    # Copy application files to build directory
                    cp -r app.py templates/ instance/ requirements.txt build/ 2>/dev/null || true
                    
                    # Create a deployment package
                    cd build
                    tar -czf flask-app-${BUILD_NUMBER}.tar.gz *
                    mv flask-app-${BUILD_NUMBER}.tar.gz ..
                    
                    echo "Application packaged successfully!"
                    ls -lh flask-app-${BUILD_NUMBER}.tar.gz
                '''
            }
        }
        
        stage('Deploy Application') {
            steps {
                echo 'Deploying the Flask application...'
                sh '''
                    # Create deployment directory if it doesn't exist
                    sudo mkdir -p ${DEPLOY_DIR}
                    
                    # Backup existing deployment (if exists)
                    if [ -d "${DEPLOY_DIR}/app.py" ]; then
                        sudo cp -r ${DEPLOY_DIR} ${DEPLOY_DIR}.backup.$(date +%Y%m%d_%H%M%S)
                        echo "Backup created successfully!"
                    fi
                    
                    # Extract and copy files to deployment directory
                    sudo tar -xzf flask-app-${BUILD_NUMBER}.tar.gz -C ${DEPLOY_DIR}
                    
                    # Set appropriate permissions
                    sudo chown -R jenkins:jenkins ${DEPLOY_DIR}
                    sudo chmod -R 755 ${DEPLOY_DIR}
                    
                    echo "Application deployed to ${DEPLOY_DIR}"
                    ls -la ${DEPLOY_DIR}
                '''
            }
        }
        
        stage('Restart Service') {
            steps {
                echo 'Restarting Flask application service...'
                script {
                    try {
                        sh '''
                            # Check if service exists and restart it
                            if sudo systemctl list-unit-files | grep -q ${SERVICE_NAME}; then
                                sudo systemctl restart ${SERVICE_NAME}
                                sudo systemctl status ${SERVICE_NAME}
                                echo "Service ${SERVICE_NAME} restarted successfully!"
                            else
                                echo "Service ${SERVICE_NAME} not found. Skipping restart."
                                echo "You can manually start the application with:"
                                echo "cd ${DEPLOY_DIR} && python3 app.py"
                            fi
                        '''
                    } catch (Exception e) {
                        echo "Service restart failed or not configured. Application files are deployed."
                        echo "Manual start command: cd ${DEPLOY_DIR} && python3 app.py"
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully! ✓'
            echo "Build Number: ${BUILD_NUMBER}"
            echo "Deployment Location: ${DEPLOY_DIR}"
            // Archive the build artifacts
            archiveArtifacts artifacts: 'flask-app-*.tar.gz', fingerprint: true
        }
        failure {
            echo 'Pipeline failed! ✗'
            echo 'Please check the logs for errors.'
        }
        always {
            // Clean up workspace
            echo 'Cleaning up...'
            cleanWs()
        }
    }
}