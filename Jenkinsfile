pipeline {

    agent any

    environment {
        CMD_EXE = 'C:\\Windows\\System32\\cmd.exe'
    }

    stages {

        stage('Verify Windows') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "VERIFYING WINDOWS"
                    Write-Host "=========================================="

                    $cmd = "C:\\Windows\\System32\\cmd.exe"

                    if (-not (Test-Path -LiteralPath $cmd)) {
                        Write-Error "cmd.exe was not found at $cmd"
                        exit 1
                    }

                    Write-Host "CMD found at: $cmd"

                    & $cmd /c "echo CMD_OK"

                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "cmd.exe could not be executed"
                        exit 1
                    }

                    Write-Host "Windows CMD is working correctly."
                '''
            }
        }

        stage('Find Python') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "SEARCHING FOR REAL PYTHON"
                    Write-Host "=========================================="

                    $pythonCandidates = @(
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python314\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
                        "C:\\Users\\PC\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
                        "C:\\Program Files\\Python314\\python.exe",
                        "C:\\Program Files\\Python313\\python.exe",
                        "C:\\Program Files\\Python312\\python.exe",
                        "C:\\Program Files\\Python311\\python.exe",
                        "C:\\Program Files (x86)\\Python314\\python.exe",
                        "C:\\Program Files (x86)\\Python313\\python.exe",
                        "C:\\Program Files (x86)\\Python312\\python.exe",
                        "C:\\Program Files (x86)\\Python311\\python.exe"
                    )

                    $python = $null

                    foreach ($candidate in $pythonCandidates) {

                        if (Test-Path -LiteralPath $candidate) {

                            Write-Host "Checking: $candidate"

                            try {
                                $version = & $candidate --version 2>&1

                                if ($LASTEXITCODE -eq 0) {
                                    $python = $candidate
                                    Write-Host "REAL PYTHON FOUND:"
                                    Write-Host $python
                                    Write-Host $version
                                    break
                                }
                            }
                            catch {
                                Write-Host "Cannot execute $candidate"
                            }
                        }
                    }

                    if ($null -eq $python) {

                        Write-Host ""
                        Write-Host "Searching all common Python locations..."

                        $locations = @(
                            "C:\\Users\\PC\\AppData\\Local\\Programs\\Python",
                            "C:\\Program Files\\Python",
                            "C:\\Program Files (x86)\\Python"
                        )

                        foreach ($location in $locations) {

                            if (Test-Path -LiteralPath $location) {

                                $found = Get-ChildItem `
                                    -Path $location `
                                    -Filter python.exe `
                                    -Recurse `
                                    -ErrorAction SilentlyContinue

                                foreach ($file in $found) {

                                    try {
                                        $version = & $file.FullName --version 2>&1

                                        if ($LASTEXITCODE -eq 0) {
                                            $python = $file.FullName
                                            Write-Host "REAL PYTHON FOUND:"
                                            Write-Host $python
                                            Write-Host $version
                                            break
                                        }
                                    }
                                    catch {
                                    }
                                }
                            }

                            if ($null -ne $python) {
                                break
                            }
                        }
                    }

                    if ($null -eq $python) {

                        Write-Host ""
                        Write-Host "=========================================="
                        Write-Host "PYTHON NOT FOUND"
                        Write-Host "=========================================="
                        Write-Host ""
                        Write-Host "The following file is NOT real Python:"
                        Write-Host "C:\\Users\\PC\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"
                        Write-Host ""
                        Write-Host "Jenkins needs a real Python installation."
                        Write-Host "Install Python from python.org and install it for all users."
                        Write-Host ""

                        exit 1
                    }

                    # Save the Python path for the next Jenkins stages
                    Set-Content -Path "python_path.txt" -Value $python

                    Write-Host ""
                    Write-Host "Python path saved successfully."
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "CREATING VIRTUAL ENVIRONMENT"
                    Write-Host "=========================================="

                    if (-not (Test-Path "python_path.txt")) {
                        Write-Error "python_path.txt was not found."
                        exit 1
                    }

                    $python = Get-Content "python_path.txt" -Raw
                    $python = $python.Trim()

                    Write-Host "Using Python:"
                    Write-Host $python

                    if (Test-Path "venv") {
                        Remove-Item "venv" -Recurse -Force
                    }

                    & $python -m venv venv

                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "Failed to create virtual environment."
                        exit 1
                    }

                    $venvPython = Join-Path $PWD "venv\\Scripts\\python.exe"

                    if (-not (Test-Path -LiteralPath $venvPython)) {
                        Write-Error "Virtual environment Python was not created."
                        exit 1
                    }

                    & $venvPython --version

                    Write-Host "Virtual environment created successfully."
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "INSTALLING DEPENDENCIES"
                    Write-Host "=========================================="

                    $python = Join-Path $PWD "venv\\Scripts\\python.exe"

                    if (-not (Test-Path -LiteralPath $python)) {
                        Write-Error "Virtual environment Python not found."
                        exit 1
                    }

                    & $python -m pip install --upgrade pip

                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "pip upgrade failed."
                        exit 1
                    }

                    if (-not (Test-Path "requirements.txt")) {
                        Write-Error "requirements.txt was not found."
                        exit 1
                    }

                    & $python -m pip install -r requirements.txt

                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "requirements.txt installation failed."
                        exit 1
                    }

                    Write-Host "Dependencies installed successfully."
                '''
            }
        }

        stage('Install Playwright') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "INSTALLING PLAYWRIGHT BROWSERS"
                    Write-Host "=========================================="

                    $python = Join-Path $PWD "venv\\Scripts\\python.exe"

                    & $python -m playwright install

                    if ($LASTEXITCODE -ne 0) {
                        Write-Error "Playwright browser installation failed."
                        exit 1
                    }

                    Write-Host "Playwright installation completed."
                '''
            }
        }

        stage('Create Reports') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "CREATING REPORT DIRECTORIES"
                    Write-Host "=========================================="

                    New-Item -ItemType Directory `
                        -Path "reports\\html-report" `
                        -Force | Out-Null

                    New-Item -ItemType Directory `
                        -Path "reports\\allure-report" `
                        -Force | Out-Null

                    Write-Host "Report directories created."
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                powershell '''
                    Write-Host "=========================================="
                    Write-Host "RUNNING API TESTS"
                    Write-Host "=========================================="

                    $python = Join-Path $PWD "venv\\Scripts\\python.exe"

                    if (-not (Test-Path "tests")) {
                        Write-Error "tests folder was not found."
                        exit 1
                    }

                    & $python -m pytest tests `
                        --html="reports\\html-report\\report.html" `
                        --self-contained-html `
                        --alluredir="reports\\allure-report"

                    $testResult = $LASTEXITCODE

                    Write-Host ""
                    Write-Host "Pytest exit code: $testResult"

                    if ($testResult -ne 0) {
                        Write-Error "API tests failed."
                        exit $testResult
                    }

                    Write-Host "API tests completed successfully."
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
            echo '=========================================='
            echo 'ARCHIVING REPORTS'
            echo '=========================================='

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