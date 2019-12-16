#!/usr/bin/env bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROJECT="pypp11"

# ----------------------------------------------------
# --- SETUPTOOLS/CMAKE CONFIGURATION------------------
# ----------------------------------------------------
export PYPP11_HOME=$CURRENT_DIR

export PYPP11_EXTERNAL_LIBS_DIR=$CURRENT_DIR/external_libraries


export OSFI_HOME=$CURRENT_DIR/external_libraries/OSFI/OSFI-3.5.0-Source

export PYTHONPATH=$CURRENT_DIR/external_libraries/OSFI/OSFI-3.5.0-Source/include/Python:$PYTHONPATH


VENV_DIRECTORY=~/virtualenvs/$PROJECT

# ----------------------------------------------------
# --- MODULES SELECTION --------------------------------
# ----------------------------------------------------

source modules.bashrc


# ----------------------------------------------------
# --- HELPER FUNCTIONS -------------------------------
# ----------------------------------------------------
# Some are hardcoded, be careful

# Create a virtualenv for $PROJECT and activate it. Any previous venv will be
# overwritten
#
# Returns nothing.
function pypp11_venv_create() {
  cd $PYPP11_HOME
  if [ -d "$VENV_DIRECTORY" ]; then
    rm -Rf "$VENV_DIRECTORY"
  fi
  virtualenv "$VENV_DIRECTORY"
  source "$VENV_DIRECTORY"/bin/activate
}
alias pypp11_venv=pypp11_venv_create


# Actiavte the current virtualenv for $PROJECT
#
# Returns nothing.
function pypp11_venv_activate() {
  cd $PYPP11_HOME
  if [ -d "$VENV_DIRECTORY" ]; then
    source "$VENV_DIRECTORY"/bin/activate
  fi
}
alias pypp11_activate=pypp11_venv_activate

# Install the python's dependencies.
# Warning: The list may be incomplete
#
# Returns nothing.
function pypp11_build_dependencies() {
  cd $PYPP11_HOME
  python3 -m pip install -r requirements.txt
  cd -
}
alias pypp11_dep=pypp11_build_dependencies



# Install the python's package in editable mode.
#
# Returns nothing.
function pypp11_develop() {
  cd $PYPP11_HOME
  python3 -m pip install -e . --user
  cd -
}
alias pypp11_develop=pypp11_develop


# Install the package locally ( = in user folders) - no sudo rights needed
#
# Returns nothing.
function pypp11_local_install() {
  cd $PYPP11_HOME
  python3 -m pip install --user .
  cd -
}
alias pypp11_linstall=pypp11_local_install


# Install the package for all users - sudo rights needed
#
# Returns nothing.
function pypp11_install() {
  cd $PYPP11_HOME
  python3 -m pip install .
  cd -
}
alias pypp11_install=pypp11_install


# Uninstall the python package ( from develop, local or global install )
#
# Returns nothing.
function pypp11_uninstall() {
  python3 -m pip uninstall $PROJECT
}
alias pypp11_uninstall=pypp11_uninstall


# Run the Python test suite
#
# Returns nothing.
function pypp11_test() {
  cd $PYPP11_HOME
  python3 setup.py test
  cd -
}
alias pypp11_test=pypp11_test

# Run the Python coverage suite
#
# Returns nothing.
function pypp11_coverage_run() {
  cd $PYPP11_HOME
  coverage run setup.py test
  cd -
}

# Generate the coverage report
#
# Returns nothing.
function pypp11_coverage_report_html() {
  cd $PYPP11_HOME
  coverage html -i
  cd -
}

# Create distribution package with sources as an archive in dist/ folder
# Returns nothing.
function pypp11_source_distribution() {
  cd $PYPP11_HOME
  python3 setup.py sdist
  cd -
}
alias pypp11_sdist=pypp11_source_distribution


# Create a distribution as an egg file in dist/ folder. No sources included
#
# Returns nothing.
function pypp11_dist_no_sources() {
  cd $PYPP11_HOME
  # python3 setup.py egg-info -Db "" sdist bdist_egg --exclude-source-files
  python3 setup.py sdist bdist_egg --exclude-source-files  # or this one
  cd -
}
alias pypp11_bdist_nosrc=pypp11_dist_no_sources


function pypp11_clean_pyc() {
  find $PYPP11_HOME -name '*.pyc' -delete
  find $PYPP11_HOME -type d -name "__pycache__" -delete
  # find . -name "*.pyc" -exec rm -f {} \;  # or this one if -delete not supported by find. depends on version. Use carefully
}

# Execute a script and display output both in terminal and log file
#
# $1 - Name of scheduler script to run
# $2 - Name of log file (optional)
#
# Returns nothing.
#
# Warning: Currently not working through bash function. Only when running the
# full command in terminal directly,
# https://unix.stackexchange.com/questions/25372/turn-off-buffering-in-pipe
function pypp11_run() {
  if [[ $# -eq 1 ]]; then
    stdbuf -oL -eL ./$1 2>&1 | tee log.txt
  elif [[ $# -eq 2 ]]; then
    stdbuf -oL -eL ./$1 2>&1 | tee $2
  else
    echo "Number of argument invalid - expecting 1 or 2"
    exit 1
  fi
}
