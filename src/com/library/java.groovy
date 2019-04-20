#!/usr/bin/groovy
package com.library

def run(args) {
    try{
        String lang = 'java'
        println("Executing java build....")
        sh """
           mkdir -p java_artifact
           mvn clean install
           chmod +x target/*.jar
           cp target/*.jar ../java_artifact
        """
        stage('UnitTest'){
            print("Unit tests are executed in the build command")
        }
        stage('SonarAnalysis') {
            libraryUtils.generateSonarPropertiesFile(args, lang)
            libraryUtils.runSonarAnalysis(lang)
        }
    }catch(e){
        print(e.getMessage())
        return false
    }
    return true
}