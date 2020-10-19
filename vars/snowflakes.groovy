def executeSnowflakesPipeline() {
node { 
   stage('Checkout') { 
      checkout scm:[
        $class: 'GitSCM', 
        branches: [[name: 'develop']], 
        doGenerateSubmoduleConfigurations: false, 
        extensions: [[$class: 'CleanCheckout']], 
        submoduleCfg: [], 
        userRemoteConfigs: [[credentialsId: 'bitbucket', url: 'https://haisrig@bitbucket.org/haisrig/sf_analytics.git']]
    ]
   }
   stage('MergeConflict') {
       echo "Executing Merge Conflict..."
       sleep 1
       echo "Merge Conflict check is completed"
   }
   stage('Static Code Analysis') {
        def scannerHome = tool 'SonarQube Scanner'
        withSonarQubeEnv('sonar') {
            sh """
                ${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=sf_analysis -Dsonar.organization=haisrig-bitbucket
            """
        }
   }
   stage('Package') {
       echo "Executing Package State..."
       sleep 1
       echo "Packaging Stage is completed"
   }
   stage('Publish') {
       echo "Executing Publish State..."
       sleep 1
       echo "Packaging Publish is completed"
   }
   stage('Deploy') {
       sh 'ls -ltR'
       withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId:'Snowflakes', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
        sh 'flyway -url=jdbc:snowflake://https://xg81978.southeast-asia.azure.snowflakecomputing.com/?db=DEMO_DB -user=$USERNAME -password=$PASSWORD -locations=filesystem:sql migrate'
        }
   }
   stage('Notification') {
            print('Notifying via teams')
            def color = getColor(currentBuild.result)            
            office365ConnectorSend status:currentBuild.result, webhookUrl:'https://outlook.office.com/webhook/2ac6b5ed-eec5-4252-a1ea-2d200d4906ca@76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/IncomingWebhook/c1457550db5f4b1c9d2b64116445a7fb/e738f645-7d63-468d-b25b-fcd9315c6c59'
    }
}
}