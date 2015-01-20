#!/usr/bin/env python
"""
Usage: 
     jiver build-and-run [--skip-tests] <maven-module>...
     jiver create (project | plugin)
     jiver database (connect | backup | restore-latest)
     jiver run-tabs
     jiver upgrade-analyzer
     jiver vpn (all | split | my-current-gateway)


Options:
    -h --help     Show this screen.
    -v --version  Show version.
"""

from docopt import docopt
from jiver import __version__

from termcolor import colored
import subprocess
import sys

import tabs
import build_and_run
import database
import vpn



def start():
    version = ".".join(str(x) for x in __version__)
    arguments = docopt(__doc__, version=version)
    
    if arguments.get('core-checkout', None):
        print colored("NEED TO IMPLEMENT", 'red')

    elif arguments.get('build-and-run', None):
        maven_modules = arguments['<maven-module>']
        skip_tests = arguments['--skip-tests']
        build_and_run.for_modules(maven_modules, skip_tests)

    elif arguments.get('create', None):
        if arguments['project']:
            try:
                cmd = "mvn -U jive:create-project"
                print colored("Running '" + cmd + "'", 'yellow')
                return_code = subprocess.call(cmd.split())
            except KeyboardInterrupt:
                print colored("Maven processed killed", 'red')
                sys.exit(0)
        elif arguments['plugin']:
            try:
                cmd = "mvn -U jive:create-plugin"
                print colored("Running '" + cmd + "'", 'yellow')
                return_code = subprocess.call(cmd.split())
            except KeyboardInterrupt:
                print colored("Maven processed killed", 'red')
                sys.exit(0)

    elif arguments.get('upgrade-analyzer', None):
        try:
            cmd = "java -jar /usr/local/jiver/upgrade-analyzer.jar port=9000"
            print colored("Running '" + cmd + "'", 'yellow')
            return_code = subprocess.call(cmd.split())
        except KeyboardInterrupt:
            print colored("Processed killed", 'red')
            sys.exit(0)

    elif arguments.get('database', None):
        if arguments['connect']:
            database.connect()
        elif arguments['backup']:
            database.backup()
        elif arguments['restore-latest']:
            database.restore_latest()

    elif arguments.get('vpn', None):
        if arguments['all']:
            vpn.all()
        elif arguments['split']:
            vpn.split()
        elif arguments['my-current-gateway']:
            vpn.my_current_gateway()

    elif arguments.get('run-tabs', None):
        tabs.run()



