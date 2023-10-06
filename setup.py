import os
import os.path as pathos
import msvcrt

from pyinstall import install_requirements

req_path = os.getcwd() + "\\requirements.txt"

print("Checking requirements...")

#install required python modules
if pathos.exists(req_path):
    install_requirements(req_path)

print("\nPress any key to exit...", end="")
msvcrt.getch()