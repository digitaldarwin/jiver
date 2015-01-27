#!/usr/bin/env python
"""
Usage:
     jiver build-and-run [--skip-tests] <maven-module>...
     jiver core-checkout [--depth-1] <version>
     jiver core-checkout-url [--depth-1] <url>
     jiver create (project | plugin)
     jiver database (connect | backup | restore-latest)
     jiver diffmerge <directory-1> <directory-2> <file>
     jiver diffmerge <directory-1> <directory-2> <directory-3> <file>
     jiver move-theme-to-top-level
     jiver overlay <file>
     jiver run-tabs
     jiver upgrade-analyzer
     jiver vpn (all | split | my-current-gateway)


Options:
    -h --help     Show this screen.
    -v --version  Show version.

Documentation:
     jiver build-and-run
            Command gives you the ability to run maven builds for multiple plugins/modules for a Jive project in sequence and then run the
            cargo-start script. This command can run in any subdirectory of a Jive project.

            Example:
                jiver build-and-run --skip-tests retention user-sync web

                This will run 'mvn clean package -DskipTest=true' for retention, then user-syc, and finally web. Once successfully built,
                the cargo-start script will run.

     jiver core-checkout
            Command will checkout a version of core code. This command works with tab completion for the Jive version numbers. The version
            numbers can be found in /usr/local/jiver/git-checkout.txt. This config file was generated from
            https://brewspace.jiveland.com/docs/DOC-61409.

            Example:
                jiver core-checkout --depth-1 7.0.0.2

                This will clone the code for 7.0.0.2 in ~/code. It will only obtain one log message. This helps to minimize the size of the
                checkout.

     jiver core-checkout-url
            Similar to 'jiver core-checkout', but for a URL. You can use the urls from https://brewspace.jiveland.com/docs/DOC-61409.

            Example:
                jiver core-checkout-url --depth-1 'http://git.jiveland.com/?p=core/application.git;a=shortlog;h=refs/heads/release_7.0.2.x'

     jiver create
            Used to create a project or a plugin
        project
            Runs 'mvn -U jive:create-project'
        plugin
            Runs 'mvn -U jive:create-plugin'

     jiver database
            All of these commands must run while in a Jive project directory or subdirectory.

        connect
            Will automatically connect via psql to the configured jdbc value in JIVE_PROJECT/target/jiveHome/jive_startup.xml
        backup
            Will back up the databases (main, eae, analytics) for the current Jive project with a timestamp to ~/code/DB-BACKUPS. This
            requires the user to conform to database names like the following:
                mcgrawhill
                mcgrawhill-eae
                mcgrawhill-analytics
        restore-latest
            Restores the most recent backup in ~/code/DB-BACKUPS for the current Jive project.

     jiver diffmerge
            Given two or three directories, this will look for the given filename. This searches all the directories for the filename and
            opens them in diffmerge.sh.

            Exmaple:
                jiver diffmerge ~/code/7.0.0.1 ~/code/7_0_3_1_core_ga login.ftl

                This generates the following command:
                diffmerge.sh \\
                ~/code/7.0.0.1/application/war/src/main/webapp/WEB-INF/classes/template/global/login.ftl \\
                ~/code/7_0_3_1_core_ga/war/src/main/webapp/WEB-INF/classes/template/global/login.ftl

            If multiple files are found, you can pass in a more specific string for the filename

            Example:
                jiver diffmerge ~/code/7.0.0.1 ~/code/7_0_3_1_core_ga global/login.ftl

                Notice the filename has 'global/' added to it.


     jiver move-theme-to-top-level

     jiver overlay
            Give ths user the ability to overlay a file per the rules defined on https://brewspace.jiveland.com/docs/DOC-74315. You must be
            in a Jive project to run this command.

            Example:
                jiver overlay '/Users/mike.masters/.m2/repository/com/jivesoftware/jive-core/7.0.3.1_5dfcca9/jive-core-7.0.3.1_5dfcca9-sources.jar!/com/jivesoftware/community/aaa/sso/saml/filter/JiveLocalMessageStorageSAMLEntryPoint.java'

                This will overlay JiveLocalMessageStorageSAMLEntryPoint.java by extracting the file from the source jar and placing the file
                accordingly in the 'web' directory of the Jive project. You can obtain the file argument by using the following steps:

                1. Open the Jive project for the customer in Intellij.
                2. Press <command>-<shift>-<n> to search for the file you want to overlay. Make sure 'Include non-project files' has a
                    checkmark next to it.
                3. Right click on the tab the source file is open in.
                4. Click 'Copy Path'.
                5. Paste value in the console with the command. Make sure to have the path value enclosed in single quotes. There should be
                    an exclamation in the string. This will be interpreted by bash/zsh.


     jiver run-tabs
            Please see https://brewspace.jiveland.com/people/mike.masters/blog/2013/11/21/automated-tabs-and-services

     jiver upgrade-analyzer
            Please see https://brewspace.jiveland.com/community/ps/ps_engineering/blog/2014/10/17/upgrade-analyzer for additional info. This
            command will start up the upgrade analyzer installed with the 'jiver' command. The upgrade analyzer is available in
            /usr/local/jiver.

     jiver vpn
            Please see https://brewspace.jiveland.com/docs/DOC-167753 for more info. This command automates the steps from that doc.
        all
            Saves the current gateway value and sends all traffic through the VPN.
        split
            Uses the previously saved gateway value and splits the VPN traffic.
        my-current-gateway
            Displays the current gateway value.

"""

from docopt import docopt
from jiver import __version__

from termcolor import colored
import subprocess
import sys
import os
import signal

import tabs
import build_and_run
import database
import vpn
import diffmerge
import overlay
import move_theme_to_top_level
import core_checkout



def start():
    version = ".".join(str(x) for x in __version__)
    arguments = docopt(__doc__, version=version)

    if arguments.get('core-checkout', None):
        version = arguments['<version>']
        depth_1 = arguments['--depth-1']
        core_checkout.run(version, depth_1)

    elif arguments.get('core-checkout-url', None):
        url = arguments['<url>']
        depth_1 = arguments['--depth-1']
        core_checkout.url(url, depth_1)

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
        os.setpgrp()
        try:
            cmd = "java -jar /usr/local/jiver/upgrade-analyzer.jar port=9000"
            print colored("Running '" + cmd + "'", 'yellow')
            return_code = subprocess.call(cmd.split())
        except KeyboardInterrupt:
            print colored("Processed killed", 'red')
            os.killpg(0, signal.SIGKILL)
            sys.exit(0)

    elif arguments.get('database', None):
        if arguments['connect']:
            database.connect()
        elif arguments['backup']:
            database.backup()
        elif arguments['restore-latest']:
            database.restore_latest()

    elif arguments.get('move-theme-to-top-level', None):
        move_theme_to_top_level.run()

    elif arguments.get('diffmerge', None):
        d1 = arguments['<directory-1>']
        d2 = arguments['<directory-2>']
        d3 = arguments['<directory-3>']
        filename = arguments['<file>']
        diffmerge.run(filter(None, [d1, d2, d3]), filename)

    elif arguments.get('vpn', None):
        if arguments['all']:
            vpn.all()
        elif arguments['split']:
            vpn.split()
        elif arguments['my-current-gateway']:
            vpn.my_current_gateway()

    elif arguments.get('overlay', None):
        filename = arguments['<file>']
        overlay.overlay_file(filename)

    elif arguments.get('run-tabs', None):
        tabs.run()



