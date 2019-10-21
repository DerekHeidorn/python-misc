import re
import os
import sys
from shutil import copyfile

def copyEarFile(src, dst):
    print ("LRA CUSTOM SETUP: Coping: " + str(src) + ", " + str(dst))
    copyfile(src, dst)

def backupFile(src, dst):
    print ("LRA CUSTOM SETUP: Coping: " + str(src) + ", " + str(dst))
    copyfile(src, dst)

def replaceVariableInTemplateString(templateContent, envName, envValue):
    patternString = '\$\{' + envName + '\}'
    pattern = re.compile(patternString)
    return re.sub(pattern, envValue, templateContent)

# set WILDFLY_HOME=/wildfly
# set LRA_DATASOURCE_CONNECTION_URL=jdbc:sqlserver://localhost:1433;DatabaseName=BCLRS_DBA
# set LRA_DATASOURCE_MIN_POOL_SIZE=1
# set LRA_DATASOURCE_MAX_POOL_SIZE=3
# set LRA_DATASOURCE_USERNAME=BCLRS_USER
# set LRA_DATASOURCE_PASSWORD=BCLRS_PASSWORD
def getEnvironmentVariable(envName):
    envVariable = os.environ.get(envName)
    if envVariable:
        print ("LRA CUSTOM SETUP: Reading environent variable: " + envName)
        return envVariable
    else:
        print ("LRA CUSTOM SETUP: Environent variable doesn't exist: " + envName)
        exit()

if len(sys.argv) < 4:
    print ("LRA CUSTOM SETUP: Error reading arguments, should be 3 but found:" + str(sys.argv))
    exit()


jbossHome = getEnvironmentVariable('WILDFLY_HOME')
#connectionUrl = getEnvironmentVariable('LRA_DATASOURCE_CONNECTION_URL')
#minPoolSize = getEnvironmentVariable('LRA_DATASOURCE_MIN_POOL_SIZE')
#maxPoolSize = getEnvironmentVariable('LRA_DATASOURCE_MAX_POOL_SIZE')
#username = getEnvironmentVariable('LRA_DATASOURCE_USERNAME')
#password = getEnvironmentVariable('LRA_DATASOURCE_PASSWORD')

standaloneDatasourceTemplatePath = sys.argv[1]
standaloneDriverTemplatePath = sys.argv[2]
standaloneEarFilePath = sys.argv[3]
standaloneConfigFilePath = jbossHome + "/standalone/configuration/standalone.xml"
standaloneDeploymentsPath = jbossHome + "/standalone/deployments/lra.ear"

print ("standaloneDatasourceTemplatePath: " + standaloneDatasourceTemplatePath)
print ("standaloneDriverTemplatePath: " + standaloneDriverTemplatePath)
print ("standaloneConfigFilePath: " + standaloneConfigFilePath)

datasourcePatternString = '<datasource\\s[^>]*>.*</datasource>'
driverPatternString = '<driver\\s[^>]*>.*</driver>'

# Backup the file

backupFile(standaloneConfigFilePath, standaloneConfigFilePath + ".backup")

standaloneConfigFile = open(standaloneConfigFilePath, "r")
datasourceFile = open(standaloneDatasourceTemplatePath, "r") 
driverFile = open(standaloneDriverTemplatePath, "r") 

# read in the content
standaloneConfigContents = standaloneConfigFile.read()
datasourceContents = datasourceFile.read()
driverContents = driverFile.read()

standaloneConfigFile.close()
datasourceFile.close()
driverFile.close()

# replace variables within the template with the environment variables
#datasourceContentsReplaced = replaceVariableInTemplateString(datasourceContents, 'LRA_DATASOURCE_CONNECTION_URL', connectionUrl)
#datasourceContentsReplaced = replaceVariableInTemplateString(datasourceContentsReplaced, 'LRA_DATASOURCE_MIN_POOL_SIZE', minPoolSize)
#datasourceContentsReplaced = replaceVariableInTemplateString(datasourceContentsReplaced, 'LRA_DATASOURCE_MAX_POOL_SIZE', maxPoolSize)
#datasourceContentsReplaced = replaceVariableInTemplateString(datasourceContentsReplaced, 'LRA_DATASOURCE_USERNAME', username)
#datasourceContentsReplaced = replaceVariableInTemplateString(datasourceContentsReplaced, 'LRA_DATASOURCE_PASSWORD', password)

# compile the RegEx patterns for the main config file
datasourcePattern = re.compile(datasourcePatternString, re.MULTILINE|re.DOTALL) # Need to deal with RegEx over multilines
driverPattern = re.compile(driverPatternString, re.MULTILINE|re.DOTALL)

# replacement on the standalone.xml
standaloneConfigContentsReplaced = re.sub(datasourcePattern, datasourceContents, standaloneConfigContents)
standaloneConfigContentsReplaced = re.sub(driverPattern, driverContents, standaloneConfigContentsReplaced)



# save the replaced contents
standaloneConfigFile = open(standaloneConfigFilePath, "w")
standaloneConfigFile.write(standaloneConfigContentsReplaced)
standaloneConfigFile.close()

print ("LRA CUSTOM SETUP: writing replaced file: " + str(standaloneConfigFilePath))

# Copy Ear file:
copyEarFile(standaloneEarFilePath, standaloneDeploymentsPath)

print ("LRA CUSTOM SETUP: Finished")

