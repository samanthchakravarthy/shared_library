#!/usr/bin/groovy

package com.library

def start() {
    node() {
        print "Cloning the code"
        checkout scm
    }
}