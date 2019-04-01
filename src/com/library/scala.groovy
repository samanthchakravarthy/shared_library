#!/usr/bin/groovy
package  com.library

def run(args) {
    try{
        String lang = 'scala'
        println("Executing scala build....")
        sh """
           cd scala
           sbt clean assembly
        """
        libraryUtils.generateSonarPropertiesFile(args,lang)
        libraryUtils.runSonarAnalysis(lang)

    }catch(e){
        print(e.getMessage())
        return false
    }
    return true
}