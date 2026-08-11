pipeline {
 
    agent any
 
    stages {
 
        stage('Create Venv') {

            steps {

                bat 'C:\\Users\\PC\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe -m venv venv'

            }

        }
 
        stage('Install Dependencies') {

            steps {

                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'

            }

        }
 
        stage('Run Tests') {

            steps {

                bat '''

                venv\\Scripts\\python -m pytest -v

                '''

            }

        }

    }

}
 