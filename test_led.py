# Test script to verify LED behavior
from led import indicate
import time

print("Testing LED indicators...")
print("1. White (ready state)")
indicate('ready')
time.sleep(3)

print("2. Flashing GREEN (photo)")
indicate('photo')
time.sleep(4)  # Wait for flashing to complete

print("3. Solid BLUE (gif)")
indicate('gif')
time.sleep(4)  # Wait for blue state to complete

print("Done - should be back to WHITE")
