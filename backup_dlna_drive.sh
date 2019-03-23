#!/bin/bash
# crontab command for execution: 
# /usr/local/sbin/backup_dlna_drive.sh >> /var/log/backup.dlna_drive.log 2>&1

SOURCE_DIR=/media/dlna_drive/
DESTINATION=/media/backup_drive/
 
echo "Start backup: $(date)"
 
rm -rf "$DESTINATION/backup.dlna_drive.3"
mv "$DESTINATION/backup.dlna_drive.2" "$DESTINATION/backup.dlna_drive.3"
mv "$DESTINATION/backup.dlna_drive.1" "$DESTINATION/backup.dlna_drive.2"
cp -al "$DESTINATION/backup.dlna_drive.0" "$DESTINATION/backup.dlna_drive.1"
rsync -a --delete $SOURCE_DIR "$DESTINATION/backup.dlna_drive.0/"
 
echo "Backup finished: $(date)"
