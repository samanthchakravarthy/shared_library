#!/usr/bin/groovy

String scanRepoTechnology() {
    String pDir = pwd()
    if (isFileExists(pDir + "/pom.xml")) {
        return "java"
    }
    if (isFileExists(pDir + "/build.sbt")){
        return "scala"
    }
    if(isFileExists(pDir + "/environment.yml")){
        return "python"
    }
}


boolean isFileExists(String fileName) {
    def file = new File(fileName)
    return file.exists()
}

/*
def isGivenDirExists(String dir){
    println(dir)
    sh """
      pwd
      if [ -d $dir];
      then
        echo "$dir exists"
        echo "true" >> commandResult
      else
        echo "$dir doesn't exists"
        echo "false" >> commandResult
      fi
    """
    String strDir = readFile('commandResult').trim()
    return strDir.toBoolean()
}

def isGivenFileExists(String file){
    println(file)
    sh """
      pwd
      if [ -e $file];
      then
        echo "$file exists"
        echo "true" >> commandResult
      else
        echo "$file doesn't exists"
        echo "false" >> commandResult
      fi
    """
    String strFile = readFile('commandResult').trim()
    return strFile.toBoolean()
}
*/

void generateSonarPropertiesFile(args, String lang){
    try{
        println("Generating sonar properties file for sonar" +lang)
        def langMap = [python:  'py', scala: 'scala', java: 'java', impala: 'plsql', hive: 'plsql', oozie: 'xml']
        def langCode = langMap[lang]
        sh"""
           touch $lang/sonar-project.properties
           cd $lang
           echo "sonar.sources=." >> sonar-project.properties
           echo "sonar.sourceEncoding=UTF-8" >> sonar-project.properties
            echo "sonar.language=$langCode" >> sonar-project.properties
            echo "sonar.projectKey=${args.projectKey}-$lang" >> sonar-project.properties
            echo "sonar.projectName=${args.projectName}-$lang" >> sonar-project.properties
        """
        println("Generating sonar properties for " +lang+ "is completed")
    }catch(e){
        println("Error generating sonar properties file")
    }
}

void runSonarAnalysis(String lang){
    def scanner = tool 'SonarQube-Scanner'
    withSonarQubeEnv('sonar-server'){
        println(scanner)
        println("Running sonar analysis for" +lang)
        sh"""
         cd $lang
         $scanner/bin/sonar-scanner
        """
    }
    println("Running sonar analysis for "+lang+ "is completed")
}

def init(loadLibVars = null){
    if(loadLibVars != null){
        loadLibraryVars(loadLibVars)
    }
    return this
}

Map loadProperties(loadLibVars){
    def readFile = "{$pwd()}/${loadLibVars}"
    try{
        return readYml(file: "${readFile}")
    }catch(e){
        println("Error loading properties file")
    }
}

def loadLibraryVars(loadLibVars = 'props.yml'){
    props = [:]
    println ("loading props $loadLibVars")
    propsFileName = loadLibVars
    vars('props.yml', loadLibVars)
    loadProperties(loadLibVars)
}
def vars(String name, value){
    addToVars(name,value)
}

def addToVars(String name, value){
    props[name] = value
}