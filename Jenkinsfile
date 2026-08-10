pipeline {

    agent any

    environment {

        PYTHON = 'C:\\Program Files\\Python314\\python.exe'

        PYTHON_SCRIPTS = 'C:\\Program Files\\Python314\\Scripts'

        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Program Files\\Python314;C:\\Program Files\\Python314\\Scripts;${env.PATH}"

        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('Verify Environment') {
            steps {
                echo '=========================================='
                echo 'VERIFYING JENKINS ENVIRONMENT'
                echo '=========================================='

                bat 'where cmd'

                bat '''
                    if exist "%PYTHON%" (
                        echo Python found at:
                        echo %PYTHON%
                    ) else (
                        echo ERROR: Python was not found at %PYTHON%
                        exit /b 1
                    )
                '''

                bat '"%PYTHON%" --version'

                bat '"%PYTHON%" -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '=========================================='
                echo 'INSTALLING PYTHON DEPENDENCIES'
                echo '=========================================='

                bat '"%PYTHON%" -m pip install --upgrade pip'

                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Create Report Directory') {
            steps {
                echo '=========================================='
                echo 'CREATING REPORT DIRECTORIES'
                echo '=========================================='

                bat '''
                    if not exist "reports" mkdir "reports"
                    if not exist "reports\\html" mkdir "reports\\html"
                    if not exist "allure-results" mkdir "allure-results"
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                echo '=========================================='
                echo 'RUNNING API AUTOMATION TESTS'
                echo '=========================================='

                bat '''
                    "%PYTHON%" -m pytest tests ^
                    --html=reports\\html\\report.html ^
                    --self-contained-html ^
                    --alluredir=allure-results ^
                    --clean-alluredir
                '''
            }
        }
    }

    post {

        always {

            echo '=========================================='
            echo 'PUBLISHING HTML REPORT'
            echo '=========================================='

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/html',
                reportFiles: 'report.html',
                reportName: 'Playwright API HTML Report',
                reportTitles: 'API Automation Test Report'
            ])

            archiveArtifacts(
                artifacts: 'reports/html/report.html',
                allowEmptyArchive: true
            )

            archiveArtifacts(
                artifacts: 'allure-results/**',
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
            echo 'Please check the test execution logs above.'
        }
    }
}