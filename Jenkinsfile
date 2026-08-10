pipeline {

    agent any

    environment {
        PYTHON = 'C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe'
    }

    stages {

        stage('Setup Python') {
            steps {
                echo 'Checking Python installation...'

                bat '''
                    if not exist "%PYTHON%" (
                        echo ERROR: Python executable was not found:
                        echo %PYTHON%
                        exit /b 1
                    )

                    echo Python executable found:
                    echo %PYTHON%

                    "%PYTHON%" --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo 'Creating Python virtual environment...'

                bat '''
                    if exist "venv" (
                        rmdir /s /q "venv"
                    )

                    "%PYTHON%" -m venv venv
                '''

                bat '''
                    venv\\Scripts\\python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'

                bat '''
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                '''

                bat '''
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Create Reports') {
            steps {
                echo 'Creating report directories...'

                bat '''
                    if not exist "reports" mkdir "reports"
                    if not exist "reports\\html-report" mkdir "reports\\html-report"
                    if not exist "reports\\allure-report" mkdir "reports\\allure-report"
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                echo 'Running API automation tests...'

                bat '''
                    venv\\Scripts\\python.exe -m pytest tests ^
                    --html=reports\\html-report\\report.html ^
                    --self-contained-html ^
                    --alluredir=reports\\allure-report
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
                    allowMissing: false
                ])
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo 'Publishing Allure report...'

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
            echo 'Archiving reports...'

            archiveArtifacts(
                artifacts: 'reports/**',
                allowEmptyArchive: true
            )
        }

        success {
            echo '============================================'
            echo 'API AUTOMATION PIPELINE PASSED'
            echo '============================================'
        }

        failure {
            echo '============================================'
            echo 'API AUTOMATION PIPELINE FAILED'
            echo '============================================'
        }
    }
}