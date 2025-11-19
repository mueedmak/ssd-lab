pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SONAR_TOKEN')
        SONARQUBE_ENV = 'MySonarQube'   // Jenkins → Configure System → SonarQube server name
        VENV = 'venv'
    }

    options {
        skipDefaultCheckout(true)
        ansiColor('xterm')
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [
                        [$class: 'CloneOption', depth: 1, noTags: true, shallow: true]
                    ],
                    userRemoteConfigs: [[url: 'https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git']]
                ])
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    pytest --junitxml=reports/junit.xml || true
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('SonarQube Analysis (SAST)') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                        . ${VENV}/bin/activate

                        sonar-scanner \
                          -Dsonar.projectKey=flask_app \
                          -Dsonar.projectName=FlaskApp \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def qg = waitForQualityGate(timeout: 5)
                    if (qg.status != 'OK') {
                        error "❌ SonarQube Quality Gate FAILED: ${qg.status}"
                    }
                    echo "✅ Quality Gate Passed: ${qg.status}"
                }
            }
        }

        stage('Build Flask App Image (Optional)') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "Packaging Flask app (optional step)..."
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*.xml', allowEmptyArchive: true
            cleanWs()
        }
        success { echo "Pipeline completed successfully." }
        failure { echo "Pipeline failed." }
    }
}
