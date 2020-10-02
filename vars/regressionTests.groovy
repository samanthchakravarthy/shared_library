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
            try {
                //sh "docker run -v `pwd`/reports:/opt/robotframework/reports:Z -v `pwd`/project:/opt/robotframework/tests:Z -e BROWSER=$browser -e AWS_ACCESS_KEY_ID=AKIA2EMYZUE52BZL7B6A -e AWS_SECRET_ACCESS_KEY=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 -e levels=$levels -e healEnabled=$healValue -e ROBOT_THREADS=2 healer"
                sh 'ls'               
            } catch (Exception e) {
                print ("Inside Catch block")
                //currentBuild.result = 'FAILURE'
            }            
        }
        stage('Prepare Reports') {
            robot outputPath: '/var/lib/jenkins/workspace/test-pipeline/reports', logFileName: 'log.html', outputFileName: 'output.xml', reportFileName: 'report.hml', otherFiles:'*.png', passThreshold: 100, unstableThreshold: 75.0
        }
        stage('Notification') {
            print('Notifying via teams')
            def color = getColor(currentBuild.result)
            print (color)
            office365ConnectorSend message: getNotifyMessage(), status:currentBuild.result, webhookUrl:'https://outlook.office.com/webhook/2ac6b5ed-eec5-4252-a1ea-2d200d4906ca@76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/IncomingWebhook/c1457550db5f4b1c9d2b64116445a7fb/e738f645-7d63-468d-b25b-fcd9315c6c59', color: color
        }
    }
}

def getNotifyMessage() {    
    def xmlContent = readFile(file: '/var/lib/jenkins/workspace/test-pipeline/reports/output.xml')    
    def result = new XmlSlurper().parseText(xmlContent)
    def cTests = result.statistics.total.stat[0]
    def cPass = result.statistics.total.stat[0].@pass
    def cFail = result.statistics.total.stat[0].@fail
    def aTests = result.statistics.total.stat[1]
    def aPass = result.statistics.total.stat[1].@pass
    def aFail = result.statistics.total.stat[1].@fail
    return """
    $cTests: 
        Pass: $cPass; Fail: $cFail
    $aTests: 
        Pass: $aPass; Fail: $aFail
    """
}

def getColor(String buildStatus) {
    print (buildStatus)
    switch(buildStatus) {
        case 'SUCCESS': return '#BDFFC2'
        case ['FAILURE', 'FAILED']: return '#FF9FA2'
        default: return '#BDFFC2'
    }
}