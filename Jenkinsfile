pipeline {
    agent any

    environment {
        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;${env.PATH}"
        COMSPEC = "C:\\Windows\\System32\\cmd.exe"
    }

    stages {

        stage('Verify Windows CMD') {
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

        stage('Find Real Python') {
            steps {
                script {
                    def pythonPath = bat(
                        returnStdout: true,
                        script: '''
                            @echo off
                            set "FOUND="

                            if exist "C:\Program Files\Python313\python.exe" set "FOUND=C:\Program Files\Python313\python.exe"
                            if exist "C:\Program Files\Python312\python.exe" set "FOUND=C:\Program Files\Python312\python.exe"
                            if exist "C:\Program Files\Python311\python.exe" set "FOUND=C:\Program Files\Python311\python.exe"
                            if exist "C:\Program Files\Python310\python.exe" set "FOUND=C:\Program Files\Python310\python.exe"

                            if exist "C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe" set "FOUND=C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe"
                            if exist "C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe" set "FOUND=C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe"
                            if exist "C:\Users\PC\AppData\Local\Programs\Python\Python311\python.exe" set "FOUND=C:\Users\PC\AppData\Local\Programs\Python\Python311\python.exe"
                            if exist "C:\Users\PC\AppData\Local\Programs\Python\Python310\python.exe" set "FOUND=C:\Users\PC\AppData\Local\Programs\Python\Python310\python.exe"

                            if defined FOUND (
                                echo %FOUND%
                                exit /b 0
                            )

                            for /f "delims=" %%P in ('where py.exe 2^>nul') do (
                                echo %%P
                                exit /b 0
                            )

                            for /f "delims=" %%P in ('where python.exe 2^>nul') do (
                                echo %%P
                                exit /b 0
                            )

                            echo NO_REAL_PYTHON_FOUND
                            exit /b 1
                        '''
                    ).trim()

                    if (!pythonPath || pythonPath == 'NO_REAL_PYTHON_FOUND') {
                        error('No real Python installation was found for the Jenkins Local System account. The WindowsApps python.exe path is only a Microsoft Store alias and is not a usable Python installation for this Jenkins service.')
                    }

                    env.PYTHON = pythonPath
                    echo "Using Python: ${env.PYTHON}"
                }
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                    echo ==========================================
                    echo VERIFYING PYTHON
                    echo ==========================================
                    echo Python: %PYTHON%
                    "%PYTHON%" --version
                    if errorlevel 1 exit /b 1
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

                    "%PYTHON%" -m venv venv

                    if not exist "venv\Scripts\python.exe" (
                        echo ERROR: Virtual environment creation failed.
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

                    venv\Scripts\python.exe -m pytest tests --html=reports\html-report\report.html --self-contained-html --alluredir=reports\allure-report
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
