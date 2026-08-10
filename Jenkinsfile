pipeline {
    agent any

    /*
     * Jenkins is running as Local System and its service PATH cannot find cmd.exe.
     * These variables force Jenkins to use the real Windows CMD.
     */
    environment {
        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps;${env.PATH}"
        COMSPEC = "C:\\Windows\\System32\\cmd.exe"

        /*
         * Python path supplied for this machine.
         */
        PYTHON = "C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"
    }

    stages {

        stage('Verify CMD') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING WINDOWS CMD
                    echo ==========================================
                    echo COMSPEC=%COMSPEC%
                    where cmd
                    "%COMSPEC%" /c "echo CMD_TEST_OK"
                '''
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================
                    if not exist "%PYTHON%" (
                        echo ERROR: Python executable was not found:
                        echo %PYTHON%
                        exit /b 1
                    )

                    "%PYTHON%" --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATING VIRTUAL ENVIRONMENT
                    echo ==========================================

                    if exist "venv" (
                        rmdir /s /q "venv"
                    )

                    "%PYTHON%" -m venv venv

                    if not exist "venv\Scripts\python.exe" (
                        echo ERROR: Virtual environment was not created.
                        exit /b 1
                    )

                    venv\Scripts\python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALLING DEPENDENCIES
                    echo ==========================================

                    venv\Scripts\python.exe -m pip install --upgrade pip
                    venv\Scripts\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                    echo ==========================================
                    echo RUNNING API TESTS
                    echo ==========================================

                    if not exist "reports\allure-report" mkdir "reports\allure-report"
                    if not exist "reports\html-report" mkdir "reports\html-report"

                    venv\Scripts\python.exe -m pytest tests ^
                        --html=reports\html-report\report.html ^
                        --self-contained-html ^
                        --alluredir=reports\allure-report
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
                    results: [
                        [path: 'reports/allure-report']
                    ]
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
