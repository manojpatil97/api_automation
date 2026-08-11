pipeline {
    agent any

    environment {
        VENV_DIR = "venv"

        // Python installed on this Jenkins machine
        PYTHON_EXE = "C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"

        // Fix Windows PATH for Jenkins
        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0;C:\\Program Files\\Git\\cmd;${env.PATH}"
    }

    stages {

        stage('Verify Windows') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING WINDOWS
                    echo ==========================================

                    echo COMSPEC=%COMSPEC%
                    echo PATH=%PATH%

                    if not exist "C:\\Windows\\System32\\cmd.exe" (
                        echo ERROR: cmd.exe not found
                        exit /b 1
                    )

                    ver

                    echo WINDOWS_OK
                '''
            }
        }


        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================

                    echo Python path:
                    echo %PYTHON_EXE%

                    if not exist "%PYTHON_EXE%" (
                        echo ERROR: Python executable not found
                        echo Expected:
                        echo %PYTHON_EXE%
                        exit /b 1
                    )

                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python could not be executed
                        exit /b 1
                    )

                    echo PYTHON_OK
                '''
            }
        }


        stage('Create Virtual Environment') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATING VIRTUAL ENVIRONMENT
                    echo ==========================================

                    if exist "%WORKSPACE%\\%VENV_DIR%" (
                        echo Removing old virtual environment...
                        rmdir /s /q "%WORKSPACE%\\%VENV_DIR%"
                    )

                    echo Creating new virtual environment...

                    "%PYTHON_EXE%" -m venv "%WORKSPACE%\\%VENV_DIR%"

                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment Python not found
                        exit /b 1
                    )

                    echo Virtual environment created successfully.

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" --version

                    echo VENV_OK
                '''
            }
        }


        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALLING PYTHON DEPENDENCIES
                    echo ==========================================

                    cd /d "%WORKSPACE%"

                    echo Current directory:
                    cd

                    echo.
                    echo Checking requirements.txt...

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt was not found.
                        echo Expected location:
                        echo %WORKSPACE%\\requirements.txt
                        exit /b 1
                    )

                    echo requirements.txt found.

                    echo.
                    echo Upgrading pip...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip

                    if errorlevel 1 (
                        echo ERROR: pip upgrade failed
                        exit /b 1
                    )

                    echo.
                    echo Installing requirements.txt...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\requirements.txt"

                    if errorlevel 1 (
                        echo ERROR: requirements.txt installation failed
                        exit /b 1
                    )

                    echo.
                    echo Installing pytest...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pip install pytest

                    if errorlevel 1 (
                        echo ERROR: pytest installation failed
                        exit /b 1
                    )

                    echo.
                    echo Installing pytest-html...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pip install pytest-html

                    if errorlevel 1 (
                        echo ERROR: pytest-html installation failed
                        exit /b 1
                    )

                    echo.
                    echo Checking installed pytest...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pytest --version

                    if errorlevel 1 (
                        echo ERROR: pytest is not available
                        exit /b 1
                    )

                    echo.
                    echo ==========================================
                    echo DEPENDENCIES INSTALLED SUCCESSFULLY
                    echo ==========================================
                '''
            }
        }


        stage('Set Environment') {
            steps {
                script {
                    env.BASE_URL = 'https://jsonplaceholder.typicode.com'

                    echo "BASE_URL = ${env.BASE_URL}"
                }
            }
        }


        stage('Create Reports Directory') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATING REPORT DIRECTORY
                    echo ==========================================

                    if not exist "%WORKSPACE%\\reports" (
                        mkdir "%WORKSPACE%\\reports"
                    )

                    echo Reports directory:
                    echo %WORKSPACE%\\reports

                    echo REPORT_DIRECTORY_OK
                '''
            }
        }


        stage('Run Pytest Tests') {
            steps {
                bat '''
                    echo ==========================================
                    echo RUNNING PYTEST TESTS
                    echo ==========================================

                    cd /d "%WORKSPACE%"

                    echo Current directory:
                    cd

                    echo.
                    echo Python version:
                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" --version

                    echo.
                    echo Pytest version:
                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pytest --version

                    echo.
                    echo Starting tests...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pytest ^
                        -v ^
                        -o addopts="" ^
                        --html="%WORKSPACE%\\reports\\report.html" ^
                        --self-contained-html ^
                        --junitxml="%WORKSPACE%\\results.xml"

                    if errorlevel 1 (
                        echo.
                        echo ==========================================
                        echo PYTEST TESTS FAILED
                        echo ==========================================
                        exit /b 1
                    )

                    echo.
                    echo ==========================================
                    echo PYTEST TESTS PASSED
                    echo ==========================================
                '''
            }
        }
    }


    post {

        always {
            echo "Publishing test reports..."

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'API Automation HTML Report'
            ])

            junit(
                allowEmptyResults: true,
                testResults: 'results.xml'
            )
        }


        success {
            echo "=========================================="
            echo "JENKINS BUILD SUCCESSFUL"
            echo "=========================================="
        }


        failure {
            echo "=========================================="
            echo "JENKINS BUILD FAILED"
            echo "Check the console output and HTML report."
            echo "=========================================="
        }


        cleanup {
            echo "Cleaning Jenkins workspace..."
            deleteDir()
        }
    }
}