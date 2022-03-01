# Object-Detection
To convert python program to windows executable program,
You need to install cx_freeze library.

pip install cx_freeze

Create a setup file :
'''
from cx_Freeze import setup, Executable

setup(name="Simple Object Detection Software", version="0.1",
      description="This software detects objects in real-time",
      executables=[Executable("main.py")])
'''
or 

Run in CMD: python setup.py build
