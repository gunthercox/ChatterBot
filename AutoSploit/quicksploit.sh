#!/bin/bash

#
# this script quickly runs a query list of search keywords provided from a file on ALL of the
# available APIs. (Censys, Zoomeye, and Shodan) from there it will save all of them to the hosts.txt
# file and you can do as you will with that
#

function doQuick() {
  for item in $(cat $1); do python autosploit.py -A -a -f etc/json/default_modules.json -q $item; done
}

function helpPage() {
  echo "./quicksploit.sh FILENAME";
  exit 1;
}

function main() {
  if [[ $EUID -ne 0 ]]; then
    echo "[!] must run script as root!";
    exit 1;
  elif [[ ! -f $1 ]]; then
    helpPage;
  else
    echo "[+] starting quicksploit searching!";
    doQuick $1;
  fi
}

main $@;