#!/usr/bin/env bash

# Hard-coded for specific desktops
python_interp="python"
if [[ $HOSTNAME == turtleland2* ]]; then
  ld_library_path="/media/ssd/sim/projects/erdc/build/cmb-superbuild/install/lib"
  pythonpath="/media/ssd/sim/projects/erdc/build/cmb-superbuild/superbuild/smtk/build"
elif [[ $HOSTNAME == tortuga* ]]; then
  python_interp="/usr/bin/python"
  ld_library_path="/Users/john/kitware/cmb/build/smtk-superbuild/install/lib"
  pythonpath="/Users/john/kitware/cmb/build/smtk"
else
  echo "Unsupported machine"
  exit -1
fi

# Get directory, per http://stackoverflow.com/questions/59895
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  TARGET="$(readlink "$SOURCE")"
  if [[ $TARGET == /* ]]; then
    #echo "SOURCE '$SOURCE' is an absolute symlink to '$TARGET'"
    SOURCE="$TARGET"
  else
    DIR="$( dirname "$SOURCE" )"
    #echo "SOURCE '$SOURCE' is a relative symlink to '$TARGET' (relative to '$DIR')"
    SOURCE="$DIR/$TARGET" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  fi
done
#echo "SOURCE is '$SOURCE'"
RDIR="$( dirname "$SOURCE" )"
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
# if [ "$DIR" != "$RDIR" ]; then
#   echo "DIR '$RDIR' resolves to '$DIR'"
# fi
echo "DIR is '$DIR'"


test_num=1
if [ $# -gt 0 ] ; then
  test_num=$1
fi

LD_LIBRARY_PATH=${ld_library_path} \
PYTHONPATH=${pythonpath} \
${python_interp} ${DIR}/testwriter.py ${DIR}/test${test_num}.crf ${DIR}/test${test_num}.ibamr \
  $*


# To generate baseline files, use
#${python_interp} ${DIR}/testwriter.py ${DIR}/test${test_num}.crf ${DIR}/test${test_num}-baseline.ibamr \
