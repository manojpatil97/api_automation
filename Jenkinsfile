pipeline {

    agent any

    environment {
        PYTHONUNBUFFERED = '1'

        // Windows system paths
        PATH = "C:\\Windows\\System32;C:\\Windows;${env.PATH}"

        // Change this if your Python is installed somewhere else
        PYTHON_HOME = "C:\\Program Files\\Python314"
    }

    stages {

        stage('Verify Environment') {
            steps {
                echo 'Checking Windows environment...'

                bat 'where cmd'
                bat 'where python'
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

                bat 'python -m playwright install chromium'
            }
        }

        stage('Create Report Directory') {
            steps {
                echo 'Creating report directories...'

                bat 'if not exist reports\\html mkdir reports\\html'
                bat 'if not exist allure-results mkdir allure-results'
            }
        }

        stage('Run API Tests') {
            steps {
                echo 'Running API automation tests...'

                bat '''
                    python -m pytest tests ^
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

            archiveArtifacts(
                artifacts: 'allure-results/**',
                allowEmptyArchive: true
            )
        }

        success {
            echo '=========================================='
            echo 'API AUTOMATION TESTS PASSED'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'API AUTOMATION TESTS FAILED'
            echo 'Please check the Jenkins console and HTML report.'
            echo '=========================================='
        }
    }
}