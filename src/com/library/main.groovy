#!/usr/bin/groovy
package com.library

def start(Map jobArgs = null) {
    print "success"
    node () {
        stage("checkout") {
            checkout scm
        }
        stage("build") {
            def tech = libraryUtils.scanRepoTechnology()
            executeBuild(tech)
        }
    }
}

def executeBuild(String lang) {
    switch (technology) {
        case "java":
            print "Gotcha!!! Its Java. Performing the Java build"
            new java().run(args)
            break
        case "scala":
            print "Gotcha!!! Its scala. Performing the scala build"
            new scala().run(args)
            break
        case "python":
            print "Gotcha!!! Its python. Performing the python build"
            new python().run(args)
            break
        case "hive":
            print "Gotcha!!! Its hive. Performing the hive build"
            new hive().run(args)
            break
        case "impala":
            print "Gotcha!!! Its impala. Performing the impala build"
            new impala().run(args)
            break
        case "oozie":
            print "Gotcha!!! Its oozie. Performing the oozie build"
            new oozie().run(args)
            break
        default:
            print "No tech found"
            break
    }
}




