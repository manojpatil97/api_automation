pipeline {
    agent any

    environment {
        PATH = "C:/Windows/System32;C:/Windows;C:/Windows/System32/Wbem;${env.PATH}"
        COMSPEC = "C:/Windows/System32/cmd.exe"
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

        stage('Find Python') {
            steps {
                script {
                    def result = bat(
                        returnStatus: true,
                        script: '''
                            @echo off
                            echo Checking Python launcher...
                            where py
                            if errorlevel 1 exit /b 1
                            py -3 --version
                            if errorlevel 1 exit /b 1
                            exit /b 0
                        '''
                    )

                    if (result == 0) {
                        env.PYTHON_COMMAND = 'py -3'
                    } else {
                        def pythonResult = bat(
                            returnStatus: true,
                            script: '''
                                @echo off
                                echo Checking Python executable...
                                where python
                                if errorlevel 1 exit /b 1
                                python --version
                                if errorlevel 1 exit /b 1
                                exit /b 0
                            '''
                        )

                        if (pythonResult == 0) {
                            env.PYTHON_COMMAND = 'python'
                        } else {
                            error('Python 3 was not found for the Jenkins service account. Install Python from python.org and enable the Python launcher, then restart Jenkins.')
                        }
                    }

                    echo "Python command selected: ${env.PYTHON_COMMAND}"
                }
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================
                    %PYTHON_COMMAND% --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    echo ==========================================
                    echo CREATING VIRTUAL ENVIRONMENT
                    echo ==========================================

                    if exist "venv" rmdir /s /q "venv"

                    %PYTHON_COMMAND% -m venv venv

                    if not exist "venv/Scripts/python.exe" (
                        echo ERROR: Virtual environment creation failed.
                        exit /b 1
                    )

                    venv/Scripts/python.exe --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo ==========================================
                    echo INSTALLING DEPENDENCIES
                    echo ==========================================

                    venv/Scripts/python.exe -m pip install --upgrade pip
                    venv/Scripts/python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                    echo ==========================================
                    echo RUNNING API TESTS
                    echo ==========================================

                    if not exist "reports/allure-report" mkdir "reports/allure-report"
                    if not exist "reports/html-report" mkdir "reports/html-report"

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
