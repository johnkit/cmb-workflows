#!/usr/bin/env bash

# Hard-coded for jat desktop (turtleland2)

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


LD_LIBRARY_PATH=/media/ssd/sim/cmb_core/build-gitlab/superbuild-11/install/lib \
PYTHONPATH=/media/ssd/sim/cmb_core/build-gitlab/superbuild-11/superbuild/smtk/src/smtk-build \
python ${DIR}/testwriter.py $*
