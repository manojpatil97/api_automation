pipeline {

    agent any

    environment {
        PYTHON_EXE = 'C:\\Program Files\\Python313\\python.exe'
    }

    stages {

        stage('Verify Windows') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFY WINDOWS
                    echo ==========================================

                    echo COMSPEC=%COMSPEC%

                    "%COMSPEC%" /c "echo CMD_OK"

                    if not exist "C:\\Windows\\System32\\cmd.exe" (
                        echo ERROR: cmd.exe not found
                        exit /b 1
                    )
                '''
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFY PYTHON
                    echo ==========================================

                    echo Python path:
                    echo %PYTHON_EXE%

                    if not exist "%PYTHON_EXE%" (
                        echo ERROR: Python was not found at:
                        echo %PYTHON_EXE%
                        echo.
                        echo Please change PYTHON_EXE in Jenkinsfile
                        echo to the actual python.exe location.
                        exit /b 1
                    )

                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python exists but cannot be executed by Jenkins.
                        exit /b 1
                    )

                    echo Python is working correctly.
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATE VIRTUAL ENVIRONMENT
                    echo ==========================================

                    if exist "venv" (
                        rmdir /s /q "venv"
                    )

                    "%PYTHON_EXE%" -m venv venv

                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment.
                        exit /b 1
                    )

                    venv\\Scripts\\python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALL DEPENDENCIES
                    echo ==========================================

                    venv\\Scripts\\python.exe -m pip install --upgrade pip

                    if errorlevel 1 (
                        echo ERROR: pip upgrade failed.
                        exit /b 1
                    )

                    venv\\Scripts\\python.exe -m pip install -r requirements.txt

                    if errorlevel 1 (
                        echo ERROR: requirements installation failed.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Install Playwright') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALL PLAYWRIGHT
                    echo ==========================================

                    venv\\Scripts\\python.exe -m playwright install

                    if errorlevel 1 (
                        echo ERROR: Playwright installation failed.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Create Reports') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATE REPORT DIRECTORY
                    echo ==========================================

                    if not exist "reports" mkdir "reports"

                    if not exist "reports\\html-report" mkdir "reports\\html-report"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    echo ==========================================
                    echo RUN PYTEST
                    echo ==========================================

                    venv\\Scripts\\python.exe -m pytest tests ^
                    --html=reports\\html-report\\report.html ^
                    --self-contained-html

                    if errorlevel 1 (
                        echo ==========================================
                        echo PYTEST FAILED
                        echo ==========================================
                        exit /b 1
                    )

                    echo ==========================================
                    echo PYTEST PASSED
                    echo ==========================================
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
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