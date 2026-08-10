pipeline {
    agent any

    environment {
        PATH = "C:/Windows/System32;C:/Windows;C:/Windows/System32/Wbem;${env.PATH}"
        PATHEXT = ".COM;.EXE;.BAT;.CMD"
    }

    stages {

        stage('Verify Windows') {
            steps {
                bat '''
                    @echo off
                    echo ==========================================
                    echo VERIFYING WINDOWS CMD
                    echo ==========================================
                    echo PATH=%PATH%
                    echo PATHEXT=%PATHEXT%
                    where cmd
                    if errorlevel 1 exit /b 1
                    echo CMD_OK
                '''
            }
        }

        stage('Find Python') {
            steps {
                bat '''
                    @echo off
                    echo ==========================================
                    echo FINDING PYTHON
                    echo ==========================================

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python313/python.exe" (
                        echo C:/Users/PC/AppData/Local/Programs/Python/Python313/python.exe>python_path.txt
                        goto :python_found
                    )

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe" (
                        echo C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe>python_path.txt
                        goto :python_found
                    )

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe" (
                        echo C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe>python_path.txt
                        goto :python_found
                    )

                    if exist "C:/Program Files/Python313/python.exe" (
                        echo C:/Program Files/Python313/python.exe>python_path.txt
                        goto :python_found
                    )

                    if exist "C:/Program Files/Python312/python.exe" (
                        echo C:/Program Files/Python312/python.exe>python_path.txt
                        goto :python_found
                    )

                    if exist "C:/Program Files/Python311/python.exe" (
                        echo C:/Program Files/Python311/python.exe>python_path.txt
                        goto :python_found
                    )

                    py -3 --version >nul 2>&1
                    if not errorlevel 1 (
                        echo py -3>python_path.txt
                        goto :python_found
                    )

                    python --version >nul 2>&1
                    if not errorlevel 1 (
                        echo python>python_path.txt
                        goto :python_found
                    )

                    echo ERROR: Python was not found.
                    exit /b 1

                    :python_found
                    set /p PYTHON_CMD=<python_path.txt
                    echo Python selected: %PYTHON_CMD%
                    %PYTHON_CMD% --version
                    if errorlevel 1 exit /b 1
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    @echo off
                    set /p PYTHON_CMD=<python_path.txt

                    if exist venv rmdir /s /q venv

                    echo Creating virtual environment...
                    %PYTHON_CMD% -m venv venv

                    if not exist "venv/Scripts/python.exe" (
                        echo ERROR: venv creation failed.
                        exit /b 1
                    )

                    venv/Scripts/python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    @echo off
                    venv/Scripts/python.exe -m pip install --upgrade pip
                    venv/Scripts/python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                    @echo off
                    if not exist reports mkdir reports
                    if not exist reports/allure-report mkdir reports/allure-report
                    if not exist reports/html-report mkdir reports/html-report

                    venv/Scripts/python.exe -m pytest tests --html=reports/html-report/report.html --self-contained-html --alluredir=reports/allure-report
                '''
            }
        }

        stage('Publish Reports') {
            steps {
                publishHTML(target: [
                    reportName: 'Pytest HTML Report',
                    reportDir: 'reports/html-report',
                    reportFiles: 'report.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])

                allure(
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-report']]
                )
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
            echo 'API AUTOMATION PIPELINE PASSED'
        }

        failure {
            echo 'API AUTOMATION PIPELINE FAILED'
        }
    }
}
