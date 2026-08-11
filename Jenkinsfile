pipeline {
    agent any

    parameters {
        choice(
            name: 'ENV',
            choices: ['QA', 'UAT', 'PROD'],
            description: 'Select Environment'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression'],
            description: 'Select Test Suite'
        )
    }

    environment {
        VENV_DIR = "venv"

        // The Jenkins agent's PATH has been observed missing C:\Windows\System32
        // on this machine - force the standard Windows system directories back
        // onto PATH for every stage, in addition to whatever the agent already has.
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
                REM Python version bump doesn't require editing this file again.
                for /f "delims=" %%D in ('dir /b /ad "C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-*" 2^>nul') do if exist "C:\\Users\\PC\\AppData\\Local\\Python\\%%D\\python.exe" set "FOUND_PYTHON=C:\\Users\\PC\\AppData\\Local\\Python\\%%D\\python.exe"
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 1c. Older per-user layout used by other Windows accounts/machines
                REM (e.g. Admin\\AppData\\Local\\Programs\\Python\\PythonXXX) - covers
                REM this pipeline running on a different agent than the one we debugged.
                for /f "delims=" %%U in ('dir /b "C:\\Users" 2^>nul') do (
                    for /f "delims=" %%D in ('dir /b /ad "C:\\Users\\%%U\\AppData\\Local\\Programs\\Python\\Python*" 2^>nul') do if exist "C:\\Users\\%%U\\AppData\\Local\\Programs\\Python\\%%D\\python.exe" set "FOUND_PYTHON=C:\\Users\\%%U\\AppData\\Local\\Programs\\Python\\%%D\\python.exe"
                )
                if defined FOUND_PYTHON echo Found Python at %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 2. Try the official py launcher (most reliable on Windows when present)
                py -3 --version >nul 2>&1
                if not errorlevel 1 for /f "delims=" %%P in ('py -3 -c "import sys;print(sys.executable)" 2^>nul') do set "FOUND_PYTHON=%%P"
                if defined FOUND_PYTHON echo Found Python via py launcher: %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                REM 3. Search Program Files (this is where "Install for all users" puts it)
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

                REM 5. Last resort - check the registry (covers unusual custom install paths)
                for /f "tokens=2,*" %%A in ('reg query "HKLM\\SOFTWARE\\Python\\PythonCore" /s /v ExecutablePath 2^>nul ^| findstr /i "ExecutablePath"') do if exist "%%B" set "FOUND_PYTHON=%%B"
                if defined FOUND_PYTHON echo Found Python via registry: %FOUND_PYTHON%
                if defined FOUND_PYTHON goto :python_found

                echo ERROR: A real Python installation was not found anywhere checked.
                echo Diagnostic - anything Python-related under Program Files:
                dir /b "C:\\Program Files" 2>nul | findstr /i python
                dir /b "C:\\Program Files (x86)" 2>nul | findstr /i python
                exit /b 1

                :python_found
                echo Using: %FOUND_PYTHON%
                "%FOUND_PYTHON%" --version
                echo %FOUND_PYTHON%> "%WORKSPACE%\\python_path.txt"
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
                    echo ERROR: python_path.txt not found - Verify Python stage did not run or failed.
                    exit /b 1
                )
                set /p FOUND_PYTHON=<"%WORKSPACE%\\python_path.txt"

                if not exist "%FOUND_PYTHON%" (
                    echo ERROR: Recorded Python path no longer exists: %FOUND_PYTHON%
                    exit /b 1
                )

                "%FOUND_PYTHON%" -m venv "%WORKSPACE%\\%VENV_DIR%"

                if not exist "%WORKSPACE%\\%VENV_DIR%\\Scripts\\python.exe" (
                    echo ERROR: Virtual environment was not created successfully.
                    exit /b 1
                )
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

                REM requirements.txt may be at the workspace root, or nested inside a
                REM wrapper folder depending on how the repo is laid out - search
                REM recursively instead of assuming the root.
                for /f "delims=" %%F in ('dir /s /b "%WORKSPACE%\\requirements.txt" 2^>nul') do set "PROJECT_DIR=%%~dpF"

                if not defined PROJECT_DIR (
                    echo WARNING: requirements.txt not found anywhere in the workspace.
                    echo Falling back to workspace root.
                    dir /b "%WORKSPACE%"
                    set "PROJECT_DIR=%WORKSPACE%\\"
                )

                echo Project directory resolved to: %PROJECT_DIR%
                echo %PROJECT_DIR%> "%WORKSPACE%\\project_dir.txt"
                echo LOCATE_OK
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

                call "%WORKSPACE%\\%VENV_DIR%\\Scripts\\activate.bat"
                python -m pip install --upgrade pip

                if exist "%PROJECT_DIR%requirements.txt" (
                    pip install -r "%PROJECT_DIR%requirements.txt"
                ) else (
                    echo WARNING: No requirements.txt found at %PROJECT_DIR% - skipping dependency install.
                )

                REM NOTE: playwright's browser download ("playwright install") is
                REM intentionally NOT run here. This project's conftest.py only uses
                REM sync_playwright().request.new_context() for pure API testing - it
                REM never launches a browser, so no Chromium/Firefox/WebKit download is
                REM needed. Attempting it was failing with EPERM trying to write into
                REM SYSTEM's own profile folder (confirms Jenkins runs as SYSTEM), and
                REM skipping it removes that failure point entirely rather than fixing
                REM a permission problem for a 150MB download this project never uses.
                REM If browser-driven tests are added later, uncomment the line below
                REM (and grant SYSTEM write access to its ms-playwright cache folder,
                REM or set PLAYWRIGHT_BROWSERS_PATH to a location SYSTEM can write to):
                REM playwright install chromium
                '''
            }
        }

        stage('Set Environment') {
            steps {
                script {
                    if (params.ENV == 'QA') {
                        env.BASE_URL = 'https://jsonplaceholder.typicode.com'
                    } else if (params.ENV == 'UAT') {
                        env.BASE_URL = 'https://jsonplaceholder.typicode.com'
                    } else {
                        env.BASE_URL = 'https://jsonplaceholder.typicode.com'
                    }
                    echo "Running on ${env.BASE_URL}"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (params.TEST_SUITE == 'all') {
                        bat '''
                        set /p PROJECT_DIR=<"%WORKSPACE%\\project_dir.txt"
                        call "%WORKSPACE%\\%VENV_DIR%\\Scripts\\activate.bat"
                        cd /d "%PROJECT_DIR%"
                        REM -o addopts="" clears pytest.ini's own --html setting for this
                        REM run, since it would otherwise collide with the --html flag below.
                        python -m pytest -v -o addopts="" --html=reports/report.html --self-contained-html --alluredir=allure-results --junitxml=results.xml
                        '''
                    } else {
                        bat """
                        set /p PROJECT_DIR=<"%WORKSPACE%\\project_dir.txt"
                        call "%WORKSPACE%\\%VENV_DIR%\\Scripts\\activate.bat"
                        cd /d "%PROJECT_DIR%"
                        python -m pytest -v -o addopts="" -m ${params.TEST_SUITE} --html=reports/report.html --self-contained-html --alluredir=allure-results --junitxml=results.xml
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'API Automation Report'
            ])

            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }

        cleanup {
            echo 'Cleaning Jenkins workspace...'
            deleteDir()
        }
    }
}
