def executeSnowflakesPipeline() {
node { 
   stage('Checkout') { 
      checkout scm:[
        $class: 'GitSCM', 
        branches: [[name: 'master']], 
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
   stage('Deploy') {
       sh 'ls -ltR'
       withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId:'Snowflakes', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
        sh 'flyway -url=jdbc:snowflake://https://xg81978.southeast-asia.azure.snowflakecomputing.com/?db=DEMO_DB -user=$USERNAME -password=$PASSWORD -locations=filesystem:sql info'
        }
   }
     
}
}