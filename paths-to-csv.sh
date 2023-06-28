#!/bin/bash


GIT=`which git`

echo ${GIT}

rclone lsf  --format "tsp" --csv --absolute --files-only -R OSN:ees230012-bucket01/AirQualityNetwork/data/raw --exclude-from exclude-file.txt > raw-osn-links.csv

# rclone lsf  --format "tsp" --csv --absolute OSN:ees230012-bucket01/AirQualityNetwork/data/raw --exclude-from exclude-file.txt > raw-osn-links.csv

${GIT} add raw-osn-links.csv
${GIT} commit -m "updating csv of raw-osn-links"
${GIT} push git@github.com:mi3nts/OSN-sync.git main
