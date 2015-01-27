

import maven_utils

import os
import sys
from termcolor import colored
import string
import xml.etree.ElementTree as ET

pom_xml = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <name>themes</name>
    <modelVersion>4.0.0</modelVersion>
    <artifactId>themes</artifactId>
    <packaging>pom</packaging>

    <parent>
        <groupId>$GROUP_ID</groupId>
        <artifactId>$ARTIFACT_ID</artifactId>
        <version>$VERSION</version>
        <relativePath>../pom.xml</relativePath>
    </parent>

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>2.4</version>
                <executions>
                    <execution>
                        <id>plugin-assembly</id>
                        <goals><goal>single</goal></goals>
                        <configuration>
                            <skipAssembly>true</skipAssembly>
                        </configuration>
                    </execution>
                    <execution>
                        <id>theme-assembly</id>
                        <goals><goal>single</goal></goals>
                        <configuration>
                            <skipAssembly>false</skipAssembly>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-antrun-plugin</artifactId>
                <executions>
                    <!-- DO NOT execute the explode-jive-plugin ant tasks -->
                    <execution>
                        <id>explode-jive-plugin</id>
                        <goals><goal>run</goal></goals>
                        <configuration>
                            <skip>true</skip>
                        </configuration>
                    </execution>
                </executions>
            </plugin>

        </plugins>
    </build>
</project>

"""


def __verify_source_directory_and_create_destination_directory(old_theme_dir, new_theme_dir):
    if not os.path.isdir(old_theme_dir):
        print colored('Themes directory not found in web project', 'red')
        sys.exit(1)
    
    if os.path.isdir(new_theme_dir):
        print colored('New theme directory already exists', 'red')
        sys.exit(1)

    print colored("Found theme directory " + old_theme_dir, 'yellow')
    print colored("Creating " + new_theme_dir, 'yellow')
    os.makedirs(new_theme_dir)

def __print_out_node_information(root):
    for child in root:
        print child.tag, child.attrib
        if child.tag == "groupId":
            group_id = child.attrib
        elif child.tag == "artifactId":
            artifact_id = child.attrib
        elif child.tag == "version":
            version = child.attrib

def __obtain_project_specific_data_from_main_pom_and_create_theme_pom(mvn_dir, new_theme_dir):

    pom_file = mvn_dir + '/pom.xml'
    #print pom_file
    
    group_id = None
    artifact_id = None
    version = None

    root = ET.parse(pom_file).getroot()

    #__print_out_node_information(root)
    nodes = root.find('{http://maven.apache.org/POM/4.0.0}groupId')
    group_id = nodes.text
   
    nodes = root.find('{http://maven.apache.org/POM/4.0.0}artifactId')
    artifact_id = nodes.text
    
    nodes = root.find('{http://maven.apache.org/POM/4.0.0}version')
    version = nodes.text

    print "groupId: " + group_id
    print "artifactId: " + artifact_id
    print "version: " + version

    f = open(new_theme_dir + "/pom.xml", 'w')
    tmpl = string.Template(pom_xml)
   
    f.write(tmpl.substitute(GROUP_ID = group_id, ARTIFACT_ID = artifact_id, VERSION = version))


def run():
    
    mvn_dir = maven_utils.find_root_maven_dir_from_current_dir()

    old_theme_dir = mvn_dir + "/web/src/main/themes"
    new_theme_dir = mvn_dir + "/themes"
    
    __verify_source_directory_and_create_destination_directory(old_theme_dir, new_theme_dir)

    __obtain_project_specific_data_from_main_pom_and_create_theme_pom(mvn_dir, new_theme_dir)




