import sys

# if not using python version 3.6.x
# shouldn't be an issue though
if sys.version_info[0] != 3 and sys.version_info[1] != 6:
    raise Exception("Must be using Python 3")
# we are using python 3.6.x, try importing packages
try:
    import pygame
    import discord
    import asyncio
except ImportError: # failed to import pygame
    import subprocess
    subprocess.call([sys.executable, "-m", "pip", "install", "pygame", "-qqq"])