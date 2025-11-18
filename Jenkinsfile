pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                echo '=== Pulling latest code ==='
                git branch: 'main', url: 'https://github.com/mueedmak/ssd-lab'
            }
        }

        stage('Simple Build') {
            steps {
                echo '=== Running simple build ==='
                bat """
                echo Hello from Jenkins!
                """
            }
        }

        stage('Success Stage') {
            steps {
                echo '=== Pipeline will finish successfully ==='
            }
        }

    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
