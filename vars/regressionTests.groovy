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
            sh 'pwd && ls -ltR'
            sh "docker run -v `pwd`/reports:/opt/robotframework/reports:Z -v `pwd`/project:/opt/robotframework/tests:Z -e BROWSER=$browser -e AWS_ACCESS_KEY_ID=AKIA2EMYZUE52BZL7B6A -e AWS_SECRET_ACCESS_KEY=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 -e levels=$levels -e healEnabled=$heal_enabled -e ROBOT_THREADS=2 healer"
        }
        stage('Notification') {
            print('Notifying via team')
        }
    }
}