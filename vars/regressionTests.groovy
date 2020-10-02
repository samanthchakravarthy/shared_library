def executeRegressionTests(heal_enabled, levels, browser) {
    print('Executing Regression tests')
    print(heal_enabled)
    print(levels)
    print(browser)
    node {
        stage('Checkout Tests') {
            if (fileExists('project')) {
                sh 'rm -rf project'
            }
            dir('project') {
                git branch: 'master', credentialsId: 'bitbucket', url: 'https://bitbucket.org/haisrig/sfd_app_rtcs.git'
                sh 'ls -ltR'
                print('Cloing the Regression tests from Bitbucket')
            }            
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