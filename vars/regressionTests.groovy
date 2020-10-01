def executeRegressionTests() {
    print('Executing Regression tests')
    node {
        stage('Checkout Tests') {
            print('Cloing the Regression tests from Bitbucket')
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