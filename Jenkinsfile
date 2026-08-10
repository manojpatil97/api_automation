pipeline {

    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out the project...'
                checkout scm
            }
        }

        stage('Python Setup') {
            steps {
                echo 'Checking Python version...'
                bat 'python --version'
                bat 'python -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Install Playwright') {
            steps {
                echo 'Installing Playwright browsers...'

                bat 'python -m playwright install'
            }
        }

        stage('Run API Tests') {
            steps {
                echo 'Running Playwright API tests...'

                bat '''
                    python -m pytest tests ^
                    --html=reports/html/report.html ^
                    --self-contained-html ^
                    --alluredir=allure-results ^
                    --clean-alluredir
                '''
            }
        }
    }

    post {

        always {

            echo 'Publishing HTML report...'

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/html',
                reportFiles: 'report.html',
                reportName: 'Playwright API HTML Report',
                reportTitles: 'API Automation Report'
            ])

            archiveArtifacts(
                artifacts: 'reports/html/report.html',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'API Automation Tests Passed Successfully!'
        }

        failure {
            echo 'API Automation Tests Failed. Please check the HTML report.'
        }
    }
}