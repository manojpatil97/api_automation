pipeline {

    agent any

    environment {
        BASE_URL = 'https://app.reqres.in'
        PYTHON_EXE = 'C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
        VENV_PYTHON = "${WORKSPACE}\\venv\\Scripts\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '=========================================='
                echo 'CHECKING OUT PROJECT'
                echo '=========================================='

                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================

                    if not exist "%PYTHON_EXE%" (
                        echo ERROR: Python not found
                        echo %PYTHON_EXE%
                        exit /b 1
                    )

                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python cannot be executed
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

                    if exist "%WORKSPACE%\\venv" (
                        echo Removing old virtual environment...
                        rmdir /s /q "%WORKSPACE%\\venv"
                    )

                    "%PYTHON_EXE%" -m venv "%WORKSPACE%\\venv"

                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment
                        exit /b 1
                    )

                    if not exist "%VENV_PYTHON%" (
                        echo ERROR: Virtual environment Python not found
                        exit /b 1
                    )

                    "%VENV_PYTHON%" --version

                    echo VENV_OK
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALLING DEPENDENCIES
                    echo ==========================================

                    cd /d "%WORKSPACE%"

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt not found
                        exit /b 1
                    )

                    echo Upgrading pip...
                    "%VENV_PYTHON%" -m pip install --upgrade pip

                    if errorlevel 1 (
                        echo ERROR: pip upgrade failed
                        exit /b 1
                    )

                    echo.
                    echo Installing requirements.txt...

                    "%VENV_PYTHON%" -m pip install -r "%WORKSPACE%\\requirements.txt"

                    if errorlevel 1 (
                        echo ERROR: Dependency installation failed
                        exit /b 1
                    )

                    echo.
                    echo Checking pytest-playwright...

                    "%VENV_PYTHON%" -m pip show pytest-playwright

                    if errorlevel 1 (
                        echo ERROR: pytest-playwright is not installed
                        exit /b 1
                    )

                    echo.
                    echo Checking pytest...

                    "%VENV_PYTHON%" -m pytest --version

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

        stage('Install Playwright Browsers') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALLING PLAYWRIGHT BROWSERS
                    echo ==========================================

                    "%VENV_PYTHON%" -m playwright install chromium

                    if errorlevel 1 (
                        echo ERROR: Playwright browser installation failed
                        exit /b 1
                    )

                    echo PLAYWRIGHT_BROWSER_OK
                '''
            }
        }

        stage('Verify Pytest Playwright Plugin') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTEST-PLAYWRIGHT
                    echo ==========================================

                    "%VENV_PYTHON%" -m pytest --fixtures | findstr /I "playwright"

                    if errorlevel 1 (
                        echo ERROR: playwright fixture was not found
                        echo pytest-playwright plugin may not be loaded
                        exit /b 1
                    )

                    echo PYTEST_PLAYWRIGHT_OK
                '''
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
                    "%VENV_PYTHON%" --version

                    echo.
                    echo Pytest version:
                    "%VENV_PYTHON%" -m pytest --version

                    echo.
                    echo BASE_URL:
                    echo %BASE_URL%

                    echo.
                    echo Starting tests...

                    "%VENV_PYTHON%" -m pytest tests -v -o addopts="" --html="%WORKSPACE%\\reports\\report.html" --self-contained-html --junitxml="%WORKSPACE%\\results.xml"

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
            echo '=========================================='
            echo 'PUBLISHING TEST RESULTS'
            echo '=========================================='

            junit allowEmptyResults: true,
                  testResults: 'results.xml'

            publishHTML(
                target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ]
            )
        }

        success {
            echo '=========================================='
            echo 'BUILD SUCCESSFUL'
            echo 'ALL PYTEST TESTS PASSED'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'BUILD FAILED'
            echo 'CHECK PYTEST ERROR ABOVE'
            echo '=========================================='
        }
    }
}