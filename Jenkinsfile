pipeline {

    agent any

    stages {

        stage('Install') {
            steps {

                echo 'Creating Python virtual environment...'

                bat '''
                    if exist "C:\\Users\\ACER\\AppData\\Local\\Python\\bin\\python.exe" (
                        echo Python executable found
                    ) else (
                        echo Python executable NOT FOUND
                        exit /b 1
                    )
                '''

                bat '''
                    "C:\\Users\\ACER\\AppData\\Local\\Python\\bin\\python.exe" -m venv venv
                '''

                echo 'Installing Python dependencies...'

                bat '''
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                '''

                bat '''
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''

                echo 'Installing Playwright...'

                bat '''
                    venv\\Scripts\\python.exe -m playwright install
                '''
            }
        }

        stage('Test') {
            steps {

                echo 'Running API automation tests...'

                bat '''
                    if not exist "reports\\html-report" mkdir "reports\\html-report"
                    if not exist "reports\\allure-report" mkdir "reports\\allure-report"
                '''

                bat '''
                    venv\\Scripts\\python.exe -m pytest tests ^
                    --alluredir=reports\\allure-report ^
                    --html=reports\\html-report\\report.html ^
                    --self-contained-html
                '''
            }
        }

        stage('Publish Report') {
            steps {

                echo 'Publishing Pytest HTML report...'

                publishHTML(target: [
                    reportName: 'Pytest HTML Report',
                    reportDir: 'reports/html-report',
                    reportFiles: 'report.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])

                echo 'Publishing Allure report...'

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

            echo 'Archiving reports...'

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