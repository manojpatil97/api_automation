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

                REM 1. Confirmed install location on this specific machine (Python 3.14's
                REM new per-user layout: AppData\\Local\\Python\\pythoncore-VER-ARCH,
                REM which replaced the old Programs\\Python\\PythonXXX layout).
                if exist "C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" set "FOUND_PYTHON=C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"
                if defined FOUND_PYTHON echo Found Python at confirmed location: %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 1b. Same new-style layout, generalized with a wildcard so a future
                REM Python version bump (3.15, etc.) doesn't require editing this file again.
                for /f "delims=" %%D in ('dir /b /ad "C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-*" 2^>nul') do if exist "C:\\Users\\PC\\AppData\\Local\\Python\\%%D\\python.exe" set "FOUND_PYTHON=C:\\Users\\PC\\AppData\\Local\\Python\\%%D\\python.exe"
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 2. Try the official py launcher (most reliable on Windows when present)
                py -3 --version >nul 2>&1
                if not errorlevel 1 for /f "delims=" %%P in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do set "FOUND_PYTHON=%%P"
                if defined FOUND_PYTHON echo Found Python via py launcher: %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 3. Search Program Files (this is where "Install for all users" puts it)
                REM Using dir/b + for/f instead of for /d with a block body, since nested
                REM parenthesized blocks break badly if any echoed text contains ( or ).
                for /f "delims=" %%D in ('dir /b /ad "C:\\Program Files\\Python*" 2^>nul') do if exist "C:\\Program Files\\%%D\\python.exe" set "FOUND_PYTHON=C:\\Program Files\\%%D\\python.exe"
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                for /f "delims=" %%D in ('dir /b /ad "C:\\Program Files (x86)\\Python*" 2^>nul') do if exist "C:\\Program Files (x86)\\%%D\\python.exe" set "FOUND_PYTHON=C:\\Program Files (x86)\\%%D\\python.exe"
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 4. Search C:\\PythonXX (older-style installs)
                for /f "delims=" %%D in ('dir /b /ad "C:\\Python*" 2^>nul') do if exist "C:\\%%D\\python.exe" set "FOUND_PYTHON=C:\\%%D\\python.exe"
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 5. Search old-style per-user install location (pre-3.14 layout)
                for /f "delims=" %%D in ('dir /b /ad "%LOCALAPPDATA%\\Programs\\Python\\Python*" 2^>nul') do if exist "%LOCALAPPDATA%\\Programs\\Python\\%%D\\python.exe" set "FOUND_PYTHON=%LOCALAPPDATA%\\Programs\\Python\\%%D\\python.exe"
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 6. Last resort - check the registry (covers unusual custom install paths)
                for /f "tokens=2,*" %%A in ('reg query "HKLM\\SOFTWARE\\Python\\PythonCore" /s /v ExecutablePath 2^>nul ^| findstr /i "ExecutablePath"') do if exist "%%B" set "FOUND_PYTHON=%%B"
                if defined FOUND_PYTHON echo Found Python via registry: %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                echo ERROR: A real Python installation was not found anywhere checked.
                echo Checked: confirmed path, py launcher, Program Files, Program Files x86, C colon Python folders, old-style LOCALAPPDATA, registry.
                echo Diagnostic - anything Python-related under Program Files:
                dir /b "C:\\Program Files" 2>nul | findstr /i python
                dir /b "C:\\Program Files (x86)" 2>nul | findstr /i python
                exit /b 1

                :python_found
                echo Using: %FOUND_PYTHON%
                "%FOUND_PYTHON%" --version
                REM Persist the discovered path to a file so later stages (separate
                REM cmd.exe processes) don't have to re-discover it from scratch.
                echo %FOUND_PYTHON%> python_path.txt
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

                if not exist python_path.txt (
                    echo ERROR: python_path.txt not found - Verify Python stage did not run or failed.
                    exit /b 1
                )
                set /p FOUND_PYTHON=<python_path.txt

                if not exist "%FOUND_PYTHON%" (
                    echo ERROR: Recorded Python path no longer exists: %FOUND_PYTHON%
                    exit /b 1
                )

                "%FOUND_PYTHON%" -m venv %VENV_DIR%

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

                REM This project uses playwright's API request context (see conftest.py),
                REM which still needs its driver installed even though no browser UI is
                REM being driven - this step commonly gets missed and causes cryptic
                REM "Executable doesn't exist" errors at test time.
                playwright install
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
                REM pytest.ini already adds --html=reports/html/report.html --self-contained-html
                REM --junitxml is added here on top so Jenkins' junit step can parse results too
                pytest --junitxml=results.xml
                '''
            }
        }

        stage('Publish Reports') {
            steps {
                junit allowEmptyResults: true, testResults: 'results.xml'
                archiveArtifacts artifacts: 'results.xml, reports/html/**', allowEmptyArchive: true
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
