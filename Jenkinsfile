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
                    where cmd
                    if errorlevel 1 exit /b 1
                    echo CMD_OK
                '''
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    @echo off
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python313/python.exe" (
                        echo Found Python 3.13
                        "C:/Users/PC/AppData/Local/Programs/Python/Python313/python.exe" --version
                        exit /b 0
                    )

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe" (
                        echo Found Python 3.12
                        "C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe" --version
                        exit /b 0
                    )

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe" (
                        echo Found Python 3.11
                        "C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe" --version
                        exit /b 0
                    )

                    if exist "C:/Program Files/Python313/python.exe" (
                        echo Found system Python 3.13
                        "C:/Program Files/Python313/python.exe" --version
                        exit /b 0
                    )

                    if exist "C:/Program Files/Python312/python.exe" (
                        echo Found system Python 3.12
                        "C:/Program Files/Python312/python.exe" --version
                        exit /b 0
                    )

                    if exist "C:/Program Files/Python311/python.exe" (
                        echo Found system Python 3.11
                        "C:/Program Files/Python311/python.exe" --version
                        exit /b 0
                    )

                    if exist "C:/Users/PC/AppData/Local/Microsoft/WindowsApps/python.exe" (
                        echo WindowsApps python.exe exists, but it may be only a Microsoft Store alias.
                        "C:/Users/PC/AppData/Local/Microsoft/WindowsApps/python.exe" --version
                        if not errorlevel 1 exit /b 0
                    )

                    echo ERROR: A real Python installation was not found.
                    echo Jenkins cannot create a virtual environment from the WindowsApps alias.
                    exit /b 1
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    @echo off

                    if exist venv rmdir /s /q venv

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python313/python.exe" (
                        "C:/Users/PC/AppData/Local/Programs/Python/Python313/python.exe" -m venv venv
                        goto :venv_done
                    )

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe" (
                        "C:/Users/PC/AppData/Local/Programs/Python/Python312/python.exe" -m venv venv
                        goto :venv_done
                    )

                    if exist "C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe" (
                        "C:/Users/PC/AppData/Local/Programs/Python/Python311/python.exe" -m venv venv
                        goto :venv_done
                    )

                    if exist "C:/Program Files/Python313/python.exe" (
                        "C:/Program Files/Python313/python.exe" -m venv venv
                        goto :venv_done
                    )

                    if exist "C:/Program Files/Python312/python.exe" (
                        "C:/Program Files/Python312/python.exe" -m venv venv
                        goto :venv_done
                    )

                    if exist "C:/Program Files/Python311/python.exe" (
                        "C:/Program Files/Python311/python.exe" -m venv venv
                        goto :venv_done
                    )

                    echo ERROR: No real Python installation was found.
                    exit /b 1

                    :venv_done
                    if not exist "venv/Scripts/python.exe" (
                        echo ERROR: Virtual environment was not created.
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
