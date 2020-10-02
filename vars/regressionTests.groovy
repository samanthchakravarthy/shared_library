def executeRegressionTests(browser) {
    print('Executing Regression tests')
    print(browser)
    node {
        stage('Checkout Tests') {
            dir('project') {
                git branch: 'master', credentialsId: 'bitbucket', url: 'https://bitbucket.org/haisrig/sfd_app_rtcs.git'
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