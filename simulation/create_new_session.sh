#!/bin/bash

VERBOSITY=false

function log(){
  if  $VERBOSITY ; then
    echo "$*"
  fi
}

: ${PYPP11_HOME:?"Env. var. PYPP11_HOME not set. Please source env.bashrc at root of seeps source directory."}
log $PYPP11_HOME

SCHEDULER_ROOT=$(cd `dirname $0` && pwd)

# Setup
BIN_DIR=$PYPP11_HOME/'bin'
SIMULATION_DIR=$PYPP11_HOME/'simulation'
DATA_SOURCE_DIR=$PYPP11_HOME/'simulation/data'
WORKSPACE_DIR=$PYPP11_HOME/'simulation/workspace'

# Debug
log $BIN_DIR
log $DATA_SOURCE_DIR
log $WORKSPACE_DIR


# Create session folder in workspace_dir. Name is based on date and hour of creation
datetime=$(date +'%Y-%m-%d-%H-%M')
foldername='Session-'$datetime
session_folder=$WORKSPACE_DIR/$foldername
mkdir -p $session_folder


# Copy scheduler into session folder
cp $SIMULATION_DIR/'scheduler_template.sh' $WORKSPACE_DIR/$foldername/'scheduler.sh'


#
# Copy conf files to session folder, configuring template filepaths
#

# In PYPP11_HOME, replace slash by antislash slash. Need to escape the slash in the path for next sed commands to work
seeps_home_for_sed=$(echo $PYPP11_HOME | sed 's_/_\\/_g')
sed "s/%%seeps_dir%%/$seeps_home_for_sed/g" $DATA_SOURCE_DIR/conf/GlobalConfiguration_template.xml > $session_folder/GlobalConfiguration.xml
sed "s/%%seeps_dir%%/$seeps_home_for_sed/g" $DATA_SOURCE_DIR/conf/L0_ProcessingConf_template.xml > $session_folder/L0_ProcessingConf.xml
sed "s/%%seeps_dir%%/$seeps_home_for_sed/g" $DATA_SOURCE_DIR/conf/L1_ProcessingConf_template.xml > $session_folder/L1_ProcessingConf.xml


