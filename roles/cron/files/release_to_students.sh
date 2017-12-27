#!/bin/bash

if [[ $# -eq 0 ]]
then
  echo 'Usage: ./release_to_students.sh [Week Number]'
  exit 0
fi

N=$1

USERS=($(cat /export/users.txt | awk '{print $1}'))

SOURCE_DIR="/export/shared/info490-fa17/Week$N"

for i in ${USERS[@]}
do

  # if a new user, create home directory
  HOME_DIR="/export/home/$i"
  if [ ! -d "$HOME_DIR" ]
  then
    echo "Released: $HOME_DIR"
    mkdir "$HOME_DIR"
    chown 1000:100 "$HOME_DIR"
  fi

  # if there is no lessons dir, create one
  LESSONS_DIR="/export/home/$i/info490-fa17-lessons"
  if [ ! -d "$LESSONS_DIR" ]
  then
    echo "Released: $LESSONS_DIR"
    mkdir "$LESSONS_DIR"
    chown 1000:100 "$LESSONS_DIR"
  fi

  TARGET_DIR="$LESSONS_DIR/Week$N"
  if [ ! -d "$TARGET_DIR" ]
  then
    echo "Released: $TARGET_DIR"
    /bin/cp -r "$SOURCE_DIR" "$TARGET_DIR"
    chown -R 1000:100 "$TARGET_DIR"
  fi

done
