#!/bin/bash

declare -A MODULES_CONF_FILES
declare -A MODULES_INPUT_DIRS
declare -A MODULES_OUTPUT_DIR

VERBOSITY=false

function log(){
  if  $VERBOSITY ; then
    echo "$*"
  fi
}

: ${PYPP11_HOME:?"Env. var. PYPP11_HOME not set. Please source env.bashrc at root of seeps source directory."}

log $PYPP11_HOME

SCHEDULER_ROOT=$(cd `dirname $0` && pwd)

BIN_DIR=$PYPP11_HOME/'bin'
DATA_SOURCE_DIR=$PYPP11_HOME/'simulation/data'
CURRENT_WORKSPACE_DIR=$SCHEDULER_ROOT

log $BIN_DIR
log $DATA_SOURCE_DIR
log $CURRENT_WORKSPACE_DIR


########################
#     MODIFY HERE      #
########################
SIMULATION_GLOBAL_CONF='GlobalConfiguration.xml'
MODULES_SIMULATION=( L0_Processing L1_Processing)

MODULES_CONF_FILES=( [L0_Processing]='L0_ProcessingConf.xml' \
                      [L1_Processing]='L1_ProcessingConf.xml SIM_ProcessingConf.xml' \
                      )

MODULES_INPUT_DIRS=( [L0_Processing]='outputSIM outputOBM' \
                        [L1_Processing]='outputGMD outputL0M' \
                        )

MODULES_OUTPUT_DIR=( [L0_Processing]='outputL0M' \
                          [L1_Processing]='outputL1M' \
                          )


########################
# END OF MODIFY HERE   #
########################


########################
# DO NOT MODIFY HERE   #
########################
#
# Build argument list and run modules
#
for mods in "${MODULES_SIMULATION[@]}"; do
  conf_files_cmd=$CURRENT_WORKSPACE_DIR/$SIMULATION_GLOBAL_CONF','
  input_dirs_cmd=''
  output_files_cmd=''

  log "Simulation scheduler -- "
  log "Simulation scheduler -- Preparing to run $mods"

  #
  # Building first argument of module executable = global + local conf files
  #
  for i in ${MODULES_CONF_FILES[$mods]}; do
    if [[ ${MODULES_CONF_FILES[$mods]+_} ]]; then
      conf_files_cmd+=$CURRENT_WORKSPACE_DIR/$i
      conf_files_cmd+=","
    fi
  done
  #  Remove trailing comma
  conf_files_cmd=${conf_files_cmd%,};
  log "Simulation scheduler -- Printing conf files of $mods"
  log $conf_files_cmd

  #
  # Building second argument of module executable = input dirs
  #
  for i in ${MODULES_INPUT_DIRS[$mods]}; do
    if [[ ${MODULES_INPUT_DIRS[$mods]+_} ]]; then
      input_dirs_cmd+=$CURRENT_WORKSPACE_DIR/$i
      input_dirs_cmd+=","
    fi
  done
  #  Remove trailing comma
  input_dirs_cmd=${input_dirs_cmd%,};
  log "Simulation scheduler -- Printing input dirs of $mods"
  log $input_dirs_cmd

  #
  # Building third argument of module executable = output dir
  #
  for i in ${MODULES_OUTPUT_DIR[$mods]}; do
    if [[ ${MODULES_OUTPUT_DIR[$mods]+_} ]]; then
      output_files_cmd+=$CURRENT_WORKSPACE_DIR/$i
      output_files_cmd+=","
    fi
  done
  #  Remove trailing comma
  output_files_cmd=${output_files_cmd%,};
  log "Simulation scheduler -- Printing output dir of $mods"
  log $output_files_cmd

  #
  # Build full command to start executable
  #

  # Determine if file is python or c++ executable
  if [ -f "$BIN_DIR/$mods.py" ] ; then
    MOD_CMD=$BIN_DIR/$mods.py' '$conf_files_cmd' '$input_dirs_cmd' '$output_files_cmd
    log "Simulation scheduler -- Starting python $mods"
    python3 $MOD_CMD
    log "Simulation scheduler -- End of python $mods"
  else
    MOD_CMD=$BIN_DIR/$mods' '$conf_files_cmd' '$input_dirs_cmd' '$output_files_cmd
    log "Simulation scheduler -- Starting C++ $mods"
    $MOD_CMD
    log "Simulation scheduler -- End of C++ $mods"
  fi


done
