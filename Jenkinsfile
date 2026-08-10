pipeline {
    agent any

    environment {
        // Adjust this to match a real Python install on your Jenkins agent.
        // Common locations - uncomment/edit the one that matches your machine:
        // PYTHON_HOME = "C:\\Python312"
        // PYTHON_HOME = "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312"
        VENV_DIR = "venv"

        // The Jenkins agent's PATH is missing C:\Windows\System32 (exit code 9009
        // on 'where cmd.exe' proves this - where.exe itself couldn't be resolved).
        // Force the standard Windows system directories back onto PATH for every
        // stage in this pipeline, in addition to whatever the agent already has.
        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0;${env.PATH}"
    }

    stages {

        stage('Verify Windows') {
            steps {
                bat '''
                echo ==========================================
                echo VERIFYING WINDOWS CMD
                echo ==========================================
                echo PATH=%PATH%
                REM Use cmd's built-in 'ver' instead of the external where.exe -
                REM builtins work even if PATH is broken, since cmd.exe itself is
                REM already running and doesn't need to resolve them externally.
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

                REM 1. Try the official py launcher first (most reliable on Windows)
                py -3 --version >nul 2>&1
                if %ERRORLEVEL% EQU 0 (
                    set "FOUND_PYTHON=py -3"
                    echo Found Python via py launcher
                    goto :python_found
                )

                REM 2. Try common hardcoded install paths
                if exist "C:\\Python312\\python.exe" (
                    set "FOUND_PYTHON=C:\\Python312\\python.exe"
                    echo Found Python at C:\\Python312\\python.exe
                    goto :python_found
                )
                if exist "C:\\Python311\\python.exe" (
                    set "FOUND_PYTHON=C:\\Python311\\python.exe"
                    echo Found Python at C:\\Python311\\python.exe
                    goto :python_found
                )
                if exist "%LOCALAPPDATA%\\Programs\\Python\\Python312\\python.exe" (
                    set "FOUND_PYTHON=%LOCALAPPDATA%\\Programs\\Python\\Python312\\python.exe"
                    echo Found Python in LOCALAPPDATA
                    goto :python_found
                )

                echo ERROR: A real Python installation was not found.
                echo The WindowsApps python.exe alias is not a valid interpreter.
                echo Install Python from python.org and ensure "Add python.exe to PATH" is checked,
                echo or set PYTHON_HOME in this Jenkinsfile to the correct install path.
                exit /b 1

                :python_found
                echo Using: %FOUND_PYTHON%
                %FOUND_PYTHON% --version
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

                py -3 --version >nul 2>&1
                if %ERRORLEVEL% EQU 0 (
                    py -3 -m venv %VENV_DIR%
                ) else if exist "C:\\Python312\\python.exe" (
                    C:\\Python312\\python.exe -m venv %VENV_DIR%
                ) else if exist "C:\\Python311\\python.exe" (
                    C:\\Python311\\python.exe -m venv %VENV_DIR%
                ) else (
                    echo ERROR: No valid Python interpreter found for venv creation.
                    exit /b 1
                )

                if not exist "%VENV_DIR%\\Scripts\\python.exe" (
                    echo ERROR: Virtual environment was not created successfully.
                    exit /b 1
                )
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
                call %VENV_DIR%\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                if exist requirements.txt (
                    pip install -r requirements.txt
                ) else (
                    echo WARNING: No requirements.txt found - skipping dependency install.
                )
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                echo ==========================================
                echo RUNNING API TESTS
                echo ==========================================
                call %VENV_DIR%\\Scripts\\activate.bat
                REM Adjust this command to match your actual test runner/framework
                pytest --junitxml=results.xml
                '''
            }
        }

        stage('Publish Reports') {
            steps {
                junit allowEmptyResults: true, testResults: 'results.xml'
                archiveArtifacts artifacts: 'results.xml', allowEmptyArchive: true
            }
        }
    }

    post {
        failure {
            echo 'API AUTOMATION PIPELINE FAILED'
        }
        success {
            echo 'API AUTOMATION PIPELINE SUCCEEDED'
        }
    }
}
