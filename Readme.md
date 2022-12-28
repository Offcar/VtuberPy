# 2D Vtuber pygame

An imaged-based Vtuber tool written in Python 3 with Pygame.
Capturing audio levels from your microphone to interact with images of your character.

## Features

+ Simple configuration.
+ Customizable settings.

## Requirements

+ PortAudio
+ Python3
+ pygame module
+ numpy module

## Setup
+ Install Python3 (https://www.python.org/) and all required modules through pip.

### Setting up your Character
Setting up your character is a simple as loading images to the **/src/** folder.

**Ex**: Loading your character's idle images of your character:
> './src/your_character/idle.png'

*Make sure to add this path as the selected charater in main.py*

---

By default, VtuberPy includes a simple character on **/src/template/**
for simpler setup, replace **/src/template/idle.png** with your own's character **idle.png** image.
