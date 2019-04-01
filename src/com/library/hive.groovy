#!/usr/bin/groovy
package com.library

def run(args) {
    try{
        String lang = 'hive'
        libraryUtils.generateSonarPropertiesFile(args,lang)
        libraryUtils.runSonarAnalysis(lang)

    }catch(e){
        print(e.getMessage())
        return false
    }
    return true
}