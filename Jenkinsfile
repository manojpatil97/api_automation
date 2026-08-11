pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out project from Git...'
                checkout scm
            }
        }

        stage('Find Python') {
            steps {
                echo 'Searching for real Python installation...'

                bat '''
                    echo ==========================================
                    echo SEARCHING FOR PYTHON
                    echo ==========================================

                    set "PYTHON_EXE="

                    if exist "C:\\Program Files\\Python314\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python314\\python.exe"
                    if exist "C:\\Program Files\\Python313\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python313\\python.exe"
                    if exist "C:\\Program Files\\Python312\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python312\\python.exe"
                    if exist "C:\\Program Files\\Python311\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python311\\python.exe"

                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"

                    if not defined PYTHON_EXE (
                        echo ERROR: Real Python installation was not found.
                        echo.
                        echo Jenkins cannot use:
                        echo C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe
                        echo.
                        echo Please install Python for all users.
                        exit /b 1
                    )

                    echo Python found:
                    echo %PYTHON_EXE%

                    "%PYTHON_EXE%" --version

                    echo %PYTHON_EXE% > python_path.txt
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo 'Creating virtual environment...'

                bat '''
                    set /p PYTHON_EXE=<python_path.txt

                    if exist "venv" rmdir /s /q "venv"

                    "%PYTHON_EXE%" -m venv venv

                    if not exist "venv\\Scripts\\python.exe" exit /b 1

                    venv\\Scripts\\python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'

                bat '''
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Create Reports') {
            steps {
                echo 'Creating report folders...'

                bat '''
                    if not exist "reports" mkdir "reports"
                    if not exist "reports\\html-report" mkdir "reports\\html-report"
                    if not exist "reports\\allure-report" mkdir "reports\\allure-report"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running API automation tests...'

                bat '''
                    venv\\Scripts\\python.exe -m pytest tests --html=reports\\html-report\\report.html --self-contained-html
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                echo 'Publishing HTML report...'

                publishHTML(target: [
                    reportName: 'Pytest HTML Report',
                    reportDir: 'reports/html-report',
                    reportFiles: 'report.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])
            }
        }
    }

    post {
        always {
            echo 'Archiving reports...'

            archiveArtifacts(
                artifacts: 'reports/**',
                allowEmptyArchive: true
            )
        }

        success {
            echo '=========================================='
            echo 'API AUTOMATION PIPELINE PASSED'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'API AUTOMATION PIPELINE FAILED'
            echo '=========================================='
        }
    }
}