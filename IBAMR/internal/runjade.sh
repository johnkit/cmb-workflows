#!/usr/bin/env bash

# List of templates in subfolder
declare -a names=( \
  "grid-2d" \
  "velocity-2d" \
  "solver" \
  )
subfolder="templates"

for name in ${names[@]}; do
  #echo ${name}
  rm -f ${subfolder}/${name}.sbt
  jade ${subfolder}/${name}.jade --pretty --extension sbt
done
