pipeline {

    agent any

    stages {

        stage('Install') {
            steps {

                bat '"C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe" -m venv venv'

                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'

                bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {

                bat 'if not exist reports\\allure-report mkdir reports\\allure-report'

                bat 'if not exist reports\\html-report mkdir reports\\html-report'

                retry(2) {
                    bat 'venv\\Scripts\\python.exe -m pytest tests --alluredir=reports/allure-report --html=reports/html-report/report.html --self-contained-html'
                }
            }
        }

        stage('Publish Report') {
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
    }
}