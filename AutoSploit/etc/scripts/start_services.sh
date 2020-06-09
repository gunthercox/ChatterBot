#!/bin/bash

function startApacheLinux () {
  # NOTE: if you are running on Arch uncomment this
  #sudo systemctl start apache > /dev/null 2>&1
  # and comment this one out
  sudo systemctl start apache2 > /dev/null 2>&1
}

function startPostgreSQLLinux () {
  sudo systemctl start postgresql > /dev/null 2>&1
}

function main () {
  if [ $1 == "linux" ]; then
    startApacheLinux;
    startPostgreSQLLinux;
  else
    echo "[*] invalid operating system";
  fi
}

main $@;
