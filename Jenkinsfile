pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/mueedmak/ssd-lab'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Flask App') {
            steps {
                bat """
                taskkill /IM python.exe /F || echo "No previous server running"

                call venv\\Scripts\\activate
                set FLASK_APP=app.py
                start /B python -m flask run --host=0.0.0.0 --port=5000
                """
            }
        }
    }
}
