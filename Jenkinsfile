pipeline {
    agent any

    environment {
        PATH = "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0;C:\\Program Files\\Git\\cmd"
    }

    stages {

        stage('Verify Windows') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "VERIFYING WINDOWS"
                    Write-Host "=========================================="

                    Write-Host "PowerShell:"
                    $PSVersionTable.PSVersion

                    Write-Host "Windows:"
                    [System.Environment]::OSVersion.Version

                    Write-Host "CMD:"
                    Test-Path "C:\\Windows\\System32\\cmd.exe"

                    Write-Host "=========================================="
                '''
            }
        }

        stage('Find Python') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "FINDING PYTHON"
                    Write-Host "=========================================="

                    $pythonPaths = @(
                        "C:\\Program Files\\Python314\\python.exe",
                        "C:\\Program Files\\Python313\\python.exe",
                        "C:\\Program Files\\Python312\\python.exe",
                        "C:\\Program Files\\Python311\\python.exe",
                        "C:\\Program Files\\Python310\\python.exe",

                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python314\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
                    )

                    $python = $null

                    foreach ($path in $pythonPaths) {
                        if (Test-Path $path) {
                            $python = $path
                            break
                        }
                    }

                    if ($null -eq $python) {
                        Write-Host ""
                        Write-Host "ERROR: REAL PYTHON WAS NOT FOUND."
                        Write-Host ""
                        Write-Host "The following WindowsApps alias is NOT valid:"
                        Write-Host "C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"
                        Write-Host ""
                        Write-Host "Please install Python for all users."
                        exit 1
                    }

                    Write-Host "REAL PYTHON FOUND:"
                    Write-Host $python

                    & $python --version

                    if ($LASTEXITCODE -ne 0) {
                        Write-Host "ERROR: Python exists but cannot be executed."
                        exit 1
                    }

                    Set-Content -Path "python_path.txt" -Value $python
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "CREATING VIRTUAL ENVIRONMENT"
                    Write-Host "=========================================="

                    $python = Get-Content "python_path.txt"

                    if (Test-Path "venv") {
                        Remove-Item "venv" -Recurse -Force
                    }

                    & $python -m venv venv

                    if ($LASTEXITCODE -ne 0) {
                        Write-Host "ERROR: Failed to create virtual environment."
                        exit 1
                    }

                    if (!(Test-Path "venv\\Scripts\\python.exe")) {
                        Write-Host "ERROR: venv Python was not created."
                        exit 1
                    }

                    & "venv\\Scripts\\python.exe" --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "INSTALLING DEPENDENCIES"
                    Write-Host "=========================================="

                    & "venv\\Scripts\\python.exe" -m pip install --upgrade pip

                    if ($LASTEXITCODE -ne 0) {
                        Write-Host "ERROR: pip upgrade failed."
                        exit 1
                    }

                    & "venv\\Scripts\\python.exe" -m pip install -r requirements.txt

                    if ($LASTEXITCODE -ne 0) {
                        Write-Host "ERROR: requirements installation failed."
                        exit 1
                    }
                '''
            }
        }

        stage('Install Playwright') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "INSTALLING PLAYWRIGHT"
                    Write-Host "=========================================="

                    & "venv\\Scripts\\python.exe" -m playwright install

                    if ($LASTEXITCODE -ne 0) {
                        Write-Host "ERROR: Playwright installation failed."
                        exit 1
                    }
                '''
            }
        }

        stage('Create Reports') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "CREATING REPORT DIRECTORIES"
                    Write-Host "=========================================="

                    New-Item -ItemType Directory -Force -Path "reports" | Out-Null
                    New-Item -ItemType Directory -Force -Path "reports\\html-report" | Out-Null
                    New-Item -ItemType Directory -Force -Path "reports\\allure-report" | Out-Null
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "RUNNING API TESTS"
                    Write-Host "=========================================="

                    & "venv\\Scripts\\python.exe" -m pytest tests `
                        --alluredir="reports\\allure-report" `
                        --html="reports\\html-report\\report.html" `
                        --self-contained-html

                    $testResult = $LASTEXITCODE

                    Write-Host "Pytest exit code: $testResult"

                    exit $testResult
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    reportName: 'Pytest HTML Report',
                    reportDir: 'reports/html-report',
                    reportFiles: 'report.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])
            }
        }

        stage('Publish Allure Report') {
            steps {
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