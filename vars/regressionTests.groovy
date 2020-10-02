def executeRegressionTests(heal_enabled, levels, browser) {    
    String healValue = ''
    node {
        stage('Checkout Tests') {
            sh 'ls -ltR'
            if (fileExists('project')) {
                sh 'rm -rf project'
            }
            dir('project') {
                git branch: 'master', credentialsId: 'bitbucket', url: 'https://bitbucket.org/haisrig/sfd_app_rtcs.git'                
                print('Cloing the Regression tests from Bitbucket')
            }            
        }
        stage('Prepare Environment') {
            print('Preparing Environment for tests')
            healValue = String.valueOf(heal_enabled)
            healValue = healValue[0].toUpperCase() + healValue.substring(1)
            print(healValue)
        }
        stage('Execute Tests') {
            print('Executing Regression tests')            
            sh "docker run -v `pwd`/reports:/opt/robotframework/reports:Z -v `pwd`/project:/opt/robotframework/tests:Z -e BROWSER=$browser -e AWS_ACCESS_KEY_ID=AKIA2EMYZUE52BZL7B6A -e AWS_SECRET_ACCESS_KEY=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 -e levels=$levels -e healEnabled=$healValue -e ROBOT_THREADS=2 healer"
        }
        stage('Prepare Reports') {
            robot outputPath: '/var/lib/jenkins/workspace/test-pipeline/reports', logFileName: 'log.html', outputFileName: 'output.xml', reportFileName: 'report.hml', passThreshold: 100, unstableThreshold: 75.0
        }
        stage('Notification') {
            print('Notifying via team')
        }
    }
}