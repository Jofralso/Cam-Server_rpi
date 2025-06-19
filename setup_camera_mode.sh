#!/bin/bash
set -e

# Enable camera and disable SPI for standalone camera mode
# Adapt for DietPi or Raspberry Pi OS config location
CONFIG_FILE="/boot/config.txt"

# Backup config
cp $CONFIG_FILE ${CONFIG_FILE}.bak_$(date +%F-%T)

# Enable camera
grep -q "^start_x=1" $CONFIG_FILE || echo "start_x=1" >> $CONFIG_FILE
grep -q "^gpu_mem=128" $CONFIG_FILE || echo "gpu_mem=128" >> $CONFIG_FILE

# Disable SPI (if exists)
sed -i '/^dtparam=spi=on/d' $CONFIG_FILE
echo "dtparam=spi=off" >> $CONFIG_FILE

echo "Camera enabled and SPI disabled. Please reboot."
