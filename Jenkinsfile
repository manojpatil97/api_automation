pipeline {
    agent any

    environment {
        VENV_DIR = "venv"

        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0;${env.PATH}"
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
                    echo CMD_OK
                '''
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================

                    set "FOUND_PYTHON="

                    REM ==========================================
                    REM Python 3.14 new installation location
                    REM ==========================================

                    if exist "C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" (
                        set "FOUND_PYTHON=C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"
                    )

                    if defined FOUND_PYTHON (
                        echo Python found at:
                        echo %FOUND_PYTHON%
                        goto :python_found
                    )


                    REM ==========================================
                    REM Search new Python installation folders
                    REM ==========================================

                    for /f "delims=" %%D in ('dir /b /ad "C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-*" 2^>nul') do (
                        if exist "C:\\Users\\PC\\AppData\\Local\\Python\\%%D\\python.exe" (
                            set "FOUND_PYTHON=C:\\Users\\PC\\AppData\\Local\\Python\\%%D\\python.exe"
                            goto :python_found
                        )
                    )


                    REM ==========================================
                    REM Search normal Python installation
                    REM ==========================================

                    for /f "delims=" %%D in ('dir /b /ad "C:\\Program Files\\Python*" 2^>nul') do (
                        if exist "C:\\Program Files\\%%D\\python.exe" (
                            set "FOUND_PYTHON=C:\\Program Files\\%%D\\python.exe"
                            goto :python_found
                        )
                    )


                    REM ==========================================
                    REM Search Python in Program Files x86
                    REM ==========================================

                    for /f "delims=" %%D in ('dir /b /ad "C:\\Program Files (x86)\\Python*" 2^>nul') do (
                        if exist "C:\\Program Files (x86)\\%%D\\python.exe" (
                            set "FOUND_PYTHON=C:\\Program Files (x86)\\%%D\\python.exe"
                            goto :python_found
                        )
                    )


                    REM ==========================================
                    REM Search C:\\PythonXXX
                    REM ==========================================

                    for /f "delims=" %%D in ('dir /b /ad "C:\\Python*" 2^>nul') do (
                        if exist "C:\\%%D\\python.exe" (
                            set "FOUND_PYTHON=C:\\%%D\\python.exe"
                            goto :python_found
                        )
                    )


                    REM ==========================================
                    REM Try Python Launcher
                    REM ==========================================

                    py -3 --version >nul 2>&1

                    if not errorlevel 1 (
                        for /f "delims=" %%P in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do (
                            set "FOUND_PYTHON=%%P"
                        )
                    )

                    if defined FOUND_PYTHON (
                        goto :python_found
                    )


                    REM ==========================================
                    REM Python not found
                    REM ==========================================

                    echo.
                    echo ==========================================
                    echo ERROR: PYTHON NOT FOUND
                    echo ==========================================
                    echo.
                    echo Jenkins could not find a real Python installation.
                    echo.
                    echo Expected Python path:
                    echo C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe
                    echo.
                    echo Please verify that this file exists on the Jenkins machine.
                    echo.
                    exit /b 1


                    :python_found

                    echo.
                    echo ==========================================
                    echo PYTHON FOUND
                    echo ==========================================

                    echo Using Python:
                    echo %FOUND_PYTHON%

                    "%FOUND_PYTHON%" --version

                    if errorlevel 1 (
                        echo ERROR: Python executable cannot be started.
                        exit /b 1
                    )

                    echo %FOUND_PYTHON% > "%WORKSPACE%\\python_path.txt"

                    echo PYTHON_OK
                '''
            }
        }


        stage('Create Venv') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATING VIRTUAL ENVIRONMENT
                    echo ==========================================

                    if not exist "%WORKSPACE%\\python_path.txt" (
                        echo ERROR: python_path.txt not found
                        exit /b 1
                    )

                    set /p FOUND_PYTHON=<"%WORKSPACE%\\python_path.txt"

                    echo Using Python:
                    echo %FOUND_PYTHON%

                    if not exist "%FOUND_PYTHON%" (
                        echo ERROR: Python executable does not exist
                        echo %FOUND_PYTHON%
                        exit /b 1
                    )

                    if exist "%WORKSPACE%\\%VENV_DIR%" (
                        echo Removing old virtual environment...
                        rmdir /s /q "%WORKSPACE%\\%VENV_DIR%"
                    )

                    "%FOUND_PYTHON%" -m venv "%WORKSPACE%\\%VENV_DIR%"

                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment Python not found
                        exit /b 1
                    )

                    echo ==========================================
                    echo VIRTUAL ENVIRONMENT CREATED
                    echo ==========================================

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" --version

                    echo VENV_OK
                '''
            }
        }


        stage('Locate Project Files') {
            steps {
                bat '''
                    echo ==========================================
                    echo LOCATING PROJECT FILES
                    echo ==========================================

                    set "PROJECT_DIR="

                    for /f "delims=" %%F in ('dir /s /b "%WORKSPACE%\\requirements.txt" 2^>nul') do (
                        set "PROJECT_DIR=%%~dpF"
                        goto :project_found
                    )

                    :project_found

                    if not defined PROJECT_DIR (
                        echo requirements.txt not found.
                        echo Using Jenkins workspace as project directory.

                        set "PROJECT_DIR=%WORKSPACE%\\"
                    )

                    echo Project directory:
                    echo %PROJECT_DIR%

                    echo %PROJECT_DIR% > "%WORKSPACE%\\project_dir.txt"

                    echo PROJECT_OK
                '''
            }
        }


        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALLING DEPENDENCIES
                    echo ==========================================

                    set /p PROJECT_DIR=<"%WORKSPACE%\\project_dir.txt"

                    echo Project directory:
                    echo %PROJECT_DIR%

                    if not exist "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment Python not found
                        exit /b 1
                    )

                    echo Upgrading pip...

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip

                    if errorlevel 1 (
                        echo ERROR: pip upgrade failed
                        exit /b 1
                    )

                    if exist "%PROJECT_DIR%requirements.txt" (

                        echo Installing requirements.txt...

                        "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%PROJECT_DIR%requirements.txt"

                        if errorlevel 1 (
                            echo ERROR: Dependency installation failed
                            exit /b 1
                        )

                    ) else (

                        echo WARNING: requirements.txt not found.
                        echo Skipping dependency installation.

                    )

                    echo DEPENDENCIES_OK
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

                    echo Reports directory ready.
                '''
            }
        }


        stage('Run Tests') {
            steps {
                bat '''
                    echo ==========================================
                    echo RUNNING PYTEST TESTS
                    echo ==========================================

                    set /p PROJECT_DIR=<"%WORKSPACE%\\project_dir.txt"

                    echo Project directory:
                    echo %PROJECT_DIR%

                    cd /d "%PROJECT_DIR%"

                    if not exist "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment Python not found
                        exit /b 1
                    )

                    "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" -m pytest -v -o addopts="" --html="%WORKSPACE%\\reports\\report.html" --self-contained-html --junitxml="%WORKSPACE%\\results.xml"

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


        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'API Automation HTML Report'
                ])
            }
        }
    }


    post {

        always {

            echo '=========================================='
            echo 'BUILD COMPLETED'
            echo '=========================================='

            archiveArtifacts(
                artifacts: 'reports/**,results.xml',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }


        success {

            echo '=========================================='
            echo 'API AUTOMATION PIPELINE SUCCESS'
            echo '=========================================='
        }


        failure {

            echo '=========================================='
            echo 'API AUTOMATION PIPELINE FAILED'
            echo '=========================================='
        }


        cleanup {

            echo 'Cleaning Jenkins workspace...'

            deleteDir()
        }
    }
}