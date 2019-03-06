#!/usr/bin/groovy

def start() {
    node() {
        print "Cloning the code"
        checkout scm
    }
}