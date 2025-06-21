#!/bin/bash
echo "Releasing GPIO pins for camera server..."

# Kill any processes that might be using the camera or GPIO
pkill -f python3 || true
pkill -f libcamera || true

# Release GPIO pins if needed
for pin in 27 22 17; do
  if [ -e /sys/class/gpio/gpio$pin ]; then
    echo "Releasing GPIO $pin"
    echo $pin > /sys/class/gpio/unexport 2>/dev/null || true
  fi
done

# Make sure SPI is enabled
if grep -q "dtparam=spi=off" /boot/config.txt; then
  echo "Warning: SPI is disabled, Inky display may not work"
fi

# Wait for pins to be released
sleep 2
echo "GPIO pins released"
exit 0
