pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        FLASK_APP = 'app.py'
    }

    stages {

        stage('Clone Repo') {
            steps {
                echo '=== Pulling latest code ==='
                git 'https://github.com/mueedmak/ssd-lab'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '=== Creating virtual environment ==='
                bat """
                python -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo '=== Running tests (if folder exists) ==='
                bat """
                call %VENV_DIR%\\Scripts\\activate
                if exist tests (
                    pytest -q
                ) else (
                    echo No tests folder found.
                )
                """
            }
        }

        stage('Deploy Flask App') {
            steps {
                echo '=== Deploying Flask App ==='
                bat """
                REM Kill any running Flask server on port 5000
                for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do taskkill /F /PID %%a >nul 2>&1

                call %VENV_DIR%\\Scripts\\activate
                set FLASK_APP=%FLASK_APP%

                REM Start app in background
                start "" python -m flask run --host=0.0.0.0 --port=5000
                timeout /t 3 >nul
                echo Flask app deployed successfully!
                """
            }
        }
    }

    post {
        success {
            echo ' CI/CD pipeline succeeded.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
