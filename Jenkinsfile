
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        DEPLOY_DIR = '/var/www/studysphere'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out StudySphere source code'

                checkout scm

                sh '''
                    echo "Repository revision:"
                    git rev-parse --short HEAD
                    git log -1 --oneline
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Preparing StudySphere build'

                sh '''
                    set -eu

                    test -f website/index.html
                    test -f website/style.css
                    test -f website/script.js

                    rm -rf build/site
                    mkdir -p build/site

                    cp -a website/. build/site/

                    echo "StudySphere build completed"
                    ls -la build/site
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running StudySphere application tests'

                sh '''
                    python3 scripts/validate_site.py build/site
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying StudySphere to Nginx'

                sh '''
                    set -eu

                    test -d "$DEPLOY_DIR"

                    rsync -rltv --delete \
                        --no-perms \
                        --no-owner \
                        --no-group \
                        build/site/ "$DEPLOY_DIR/"

                    HTTP_CODE=$(curl -s -o /tmp/studysphere-response.html \
                        -w "%{http_code}" http://127.0.0.1/)

                    echo "HTTP response: $HTTP_CODE"

                    test "$HTTP_CODE" = "200"

                    grep -qi "StudySphere" \
                        /tmp/studysphere-response.html

                    echo "Deployment verified successfully"
                '''
            }
        }
    }

    post {
        success {
            echo 'StudySphere CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'StudySphere CI/CD Pipeline failed. Check the console output.'
        }

        always {
            archiveArtifacts(
                artifacts: 'build/site/**',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }
    }
}
