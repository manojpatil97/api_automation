pipeline {
    agent any

    stages {

        stage('Verify Windows') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING WINDOWS
                    echo ==========================================
                    where cmd
                    echo CMD_OK
                '''
            }
        }

        stage('Find Python') {
            steps {
                script {
                    def pythonCheck = bat(
                        returnStatus: true,
                        script: '''
                            @echo off
                            py -3 --version >nul 2>&1
                            exit /b %ERRORLEVEL%
                        '''
                    )

                    if (pythonCheck == 0) {
                        env.PYTHON_CMD = 'py -3'
                    } else {
                        def pythonCheck2 = bat(
                            returnStatus: true,
                            script: '''
                                @echo off
                                python --version >nul 2>&1
                                exit /b %ERRORLEVEL%
                            '''
                        )

                        if (pythonCheck2 == 0) {
                            env.PYTHON_CMD = 'python'
                        } else {
                            error('Python is not available to the Jenkins service account. Install Python for all users or configure the Jenkins service to run under your Windows user account.')
                        }
                    }

                    echo "Python command: ${env.PYTHON_CMD}"
                }
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    if exist venv rmdir /s /q venv
                    %PYTHON_CMD% -m venv venv
                    if not exist venv/Scripts/python.exe exit /b 1
                    venv/Scripts/python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    venv/Scripts/python.exe -m pip install --upgrade pip
                    venv/Scripts/python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
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
            echo 'API AUTOMATION PIPELINE PASSED'
        }

        failure {
            echo 'API AUTOMATION PIPELINE FAILED'
        }
    }
}
