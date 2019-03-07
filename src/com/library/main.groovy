#!/usr/bin/groovy
package com.library

def start(Map jobArgs = null) {
    print "success"
    node () {
        stage("checkout") {
            checkout scm
            print pwd()
        }
        stage("build") {
            def tech = scanRepoTechnology()
            executeBuild(tech)
        }
    }
}

def executeBuild(String technology) {
    switch (technology) {
        case "java":
            print "Gotcha!!! Its Java. Performing the Java build"
            break
        default:
            print "No tech found"
            break
    }
}

String scanRepoTechnology() {
    String pDir = pwd()
    if(isFileExists(pDir +"/pom.xml")) {
        return "java"
    }
}

boolean isFileExists(String fileName) {
    def file = new File(fileName)
    return file.exists()
}



