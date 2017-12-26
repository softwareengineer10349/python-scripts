################################################################################
# Function: getLineMatchingFromFilename - takes 2 input paramaters - sets 1 paramater
#
# General or specific: Completely General
#
# Description: Reads the settings.ini file and grabs the line you want
#
# Usage: getLineMatchingFromFilename setting.ini TEST_LOCATION
#
# Expected pipeline: called in the main function set up at the start - then getValueFromSettingsIniLine should be called to
# get the actual value from the line e.g. ~/folder/for/testing NOT TEST_LOCATION=~/folder/for/testing
#
###################### Input paramaters ########################################
#
# Argument 1: filename of settings.ini (full or relative path)
#
# Argument 2: regex to match the field you want
#
##################### Output paramaters ########################################
#
# LINE: the entire line of the settings.ini file matching your criteria.
# E.g. TEST_LOCATION=~/folder/for/testing
#
################################################################################

function getLineMatchingFromFilename {
  FILENAME="${1}"
  START_TO_MATCH="${2}"
  while IFS= read LINE; do
    if [[ "${LINE}" =~ "${START_TO_MATCH}" ]]; then
      return 0
    fi
  done < "${FILENAME}"
  #if nothing was returned by this point there are no matches
  exit 101 #code 100s are indicative of system code failing rather than user input - in this case 101 is looking for settings.ini heading that isn't there
}

################################################################################
# Function: getValueFromSettingsIniLine - takes 3 input paramaters - sets 1 paramater
#
# General or specific: Completely General
#
# Description: Reads one line of a settings.ini file and grabs the value of the heading
#
# Usage: getValueFromSettingsIniLine TEST_LOCATION=~/folder/for/testing.ini = 2
#
# Expected pipeline: called in the main function set up at the start - after getLineMatchingFromFilename
# grabs the correct line of settings.ini
#
###################### Input paramaters ########################################
#
# Argument 1: Full line of file of settings.ini
#
# Argument 2: Character delimiting the heading from the value
#
# Argument 3: Field position of value (expecting it to mostly be 2 but could use multiple options and switch from position 2,3, etc. based on criteria)
#
##################### Output paramaters ########################################
#
# LINE: the value of the settings.ini heading
# E.g. ~/folder/for/testing
#
################################################################################

function getValueFromSettingsIniLine {
  LINE_OF_FILE="${1}"
  SPLIT_BY="${2}"
  FIELD_POSISTION="${3}"
  LINE=`echo $LINE | cut -d"${SPLIT_BY}" -f${FIELD_POSISTION}`
}

################################################################################
# Function: setEachSettingsVariable - takes no input paramaters - sets 1 paramater
#
# General or specific: Relatively general - more complex scripts could do more complex things here
#
# Description: Calls everything that needs to be called to get the values from one line of the settings.ini file
#
# Usage: setEachSettingsVariable settings.ini TEST_LOCATION
#
# Expected pipeline: called in the main function set up at the start
# Each settings.ini heading will call this function
#
###################### Input paramaters ########################################
#
# Argument 1: Filename of the settings.ini file (full or relative)
#
# Argument 2: Regex identifier of the start of the line for the settings.ini line you want to grab
#
##################### Output paramaters ########################################
#
# LINE: the value of the settings.ini line you chose
#
################################################################################

function setEachSettingsVariable {
  SETTINGS_FILENAME="${1}"
  VARIABLE_START_IDENTIFIER="${2}"
  getLineMatchingFromFilename "${SETTINGS_FILENAME}" "${VARIABLE_START_IDENTIFIER}"
  getValueFromSettingsIniLine "${LINE}" "=" "2"
  #echo "MY new line = ${LINE}"
}

################################################################################
# Function: getSettingsFileValues - takes no input paramaters - sets many paramaters
#
# General or specific: Relatively specific to each script - grabs everything from the settings.ini related to this script.
# Obviously a lot of things use settings.ini so the general structure is very resuable, but different things will have somewhat different setting names.
#
# Description: Sets every single variable that this script needs from the settings.ini
#
# Usage: getSettingsFileValues
#
# Expected pipeline: called in the main function set up at the start - after getValueFromSettingsIniLine
# grabs the correct value from the settings.ini file
#
###################### Input paramaters ########################################
#
# None
#
##################### Output paramaters ########################################
#
# TEST_LOCATION: this is the filename where things are being tested e.g. local web server
#
# DEV_LOCATION: this is the filename where things are being developed before testing
#
################################################################################

function getSettingsFileValues {
  SETTINGS_FILENAME="settings.ini"
  setEachSettingsVariable "${SETTINGS_FILENAME}" "TEST_LOCATION"
  TEST_LOCATION="${LINE}"
  setEachSettingsVariable "${SETTINGS_FILENAME}" "DEV_LOCATION"
  DEV_LOCATION="${LINE}"
}

####################### Code execution starts here #############################

#gets all values from settings.ini
getSettingsFileValues


#cd "${DEVELOPMENT_LOCATION}/"* "${TEST_LOCATION}/"
