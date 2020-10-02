def executeRegressionTests() {
    print('Executing Regression tests')
    node {
        stage('Checkout Tests') {
            dir('project') {
                git branch: 'master', credentialsId: 'bitbucket', url: 'https://haisrig@bitbucket.org/haisrig/queuereader.git'
                sh 'ls -ltR'
                print('Cloing the Regression tests from Bitbucket')
            }
            sh 'rm -rf project'
        }
        stage('Prepare Environment') {
            print('Preparing Environment for tests')
        }
        stage('Execute Tests') {
            print('Executing Regression tests')
        }
        stage('Notification') {
            print('Notifying via team')
        }
    }
}