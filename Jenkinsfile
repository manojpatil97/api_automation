pipeline {

    agent any

    environment {
        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;${env.PATH}"
    }

    stages {

        stage('Verify Windows') {
            steps {
                echo 'Verifying Windows environment...'

                bat '''
                    echo ==========================================
                    echo WINDOWS CHECK
                    echo ==========================================

                    echo COMSPEC=%COMSPEC%
                    echo PATH=%PATH%

                    "%COMSPEC%" /c "echo CMD_OK"

                    if not exist "C:\\Windows\\System32\\cmd.exe" (
                        echo ERROR: cmd.exe not found
                        exit /b 1
                    )

                    echo Windows CMD is available.
                '''
            }
        }


        stage('Find Python') {
            steps {
                echo 'Finding Python installation...'

                bat '''
                    echo ==========================================
                    echo FINDING PYTHON
                    echo ==========================================

                    set "PYTHON_EXE="

                    if exist "C:\\Program Files\\Python314\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python314\\python.exe"
                    if exist "C:\\Program Files\\Python313\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python313\\python.exe"
                    if exist "C:\\Program Files\\Python312\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python312\\python.exe"
                    if exist "C:\\Program Files\\Python311\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python311\\python.exe"
                    if exist "C:\\Program Files\\Python310\\python.exe" set "PYTHON_EXE=C:\\Program Files\\Python310\\python.exe"

                    if exist "C:\\Python314\\python.exe" set "PYTHON_EXE=C:\\Python314\\python.exe"
                    if exist "C:\\Python313\\python.exe" set "PYTHON_EXE=C:\\Python313\\python.exe"
                    if exist "C:\\Python312\\python.exe" set "PYTHON_EXE=C:\\Python312\\python.exe"
                    if exist "C:\\Python311\\python.exe" set "PYTHON_EXE=C:\\Python311\\python.exe"
                    if exist "C:\\Python310\\python.exe" set "PYTHON_EXE=C:\\Python310\\python.exe"

                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python311\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
                    if exist "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" set "PYTHON_EXE=C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"

                    if "%PYTHON_EXE%"=="" (
                        echo ERROR: Real Python installation was not found.
                        echo.
                        echo IMPORTANT:
                        echo C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe
                        echo is only a Microsoft Store alias and cannot be used.
                        echo.
                        echo Install Python from python.org and restart Jenkins.
                        exit /b 1
                    )

                    echo Python found at:
                    echo %PYTHON_EXE%

                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python cannot be executed.
                        exit /b 1
                    )

                    echo PYTHON_EXE=%PYTHON_EXE%>python_path.txt
                '''
            }
        }


        stage('Create Virtual Environment') {
            steps {
                echo 'Creating virtual environment...'

                bat '''
                    echo ==========================================
                    echo CREATING VIRTUAL ENVIRONMENT
                    echo ==========================================

                    set "PYTHON_EXE="

                    for /f "tokens=1,* delims==" %%A in (python_path.txt) do (
                        if "%%A"=="PYTHON_EXE" set "PYTHON_EXE=%%B"
                    )

                    echo Using Python:
                    echo %PYTHON_EXE%

                    if exist "venv" (
                        rmdir /s /q "venv"
                    )

                    "%PYTHON_EXE%" -m venv venv

                    if errorlevel 1 (
                        echo ERROR: Virtual environment creation failed.
                        exit /b 1
                    )

                    venv\\Scripts\\python.exe --version
                '''
            }
        }


        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                bat '''
                    echo ==========================================
                    echo INSTALLING DEPENDENCIES
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
                echo 'Installing Playwright browsers...'

                bat '''
                    echo ==========================================
                    echo INSTALLING PLAYWRIGHT
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
                echo 'Creating HTML report directory...'

                bat '''
                    echo ==========================================
                    echo CREATING REPORT DIRECTORY
                    echo ==========================================

                    if not exist "reports" mkdir "reports"

                    if not exist "reports\\html-report" mkdir "reports\\html-report"
                '''
            }
        }


        stage('Run Tests') {
            steps {
                echo 'Running API automation tests...'

                bat '''
                    echo ==========================================
                    echo RUNNING PYTEST
                    echo ==========================================

                    venv\\Scripts\\python.exe -m pytest tests ^
                    --html=reports\\html-report\\report.html ^
                    --self-contained-html

                    if errorlevel 1 (
                        echo ==========================================
                        echo PYTEST TESTS FAILED
                        echo ==========================================
                        exit /b 1
                    )

                    echo ==========================================
                    echo PYTEST TESTS PASSED
                    echo ==========================================
                '''
            }
        }


        stage('Publish HTML Report') {
            steps {
                echo 'Publishing Pytest HTML report...'

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
            echo 'Archiving test reports...'

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