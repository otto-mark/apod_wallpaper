# NASA APOD desktop wallpaper (WIN10/WIN11)

This is a python script that let's you set the [Astronomical Picture Of the Day](https://apod.nasa.gov/apod/) as your desktop wallpaper on a windows machine so you can start each day mesmerized by the beauty of space and science.


## Getting started

APODwallpaper runs on Python 3.x (tested on Python 3.8). If you don't have Python installed yet, donwload it from [here](https://www.python.org/downloads/).

### Requirements
- Python 3.x (at least 3.8)
    - from Python standard library:
        - os, sys, urllib, ctypes
    - requests
    - Python Image Library (PIL)

Install the required packages running
```pip install -r requirements.txt```

### Setup
Open `config.py` in an editor of your choice and fill in sensible values.

If you intend to use this script frequently, [please get an API key for the official APOD API from this link](https://api.nasa.gov/) and set it as your access token.

## Run

Run ```python main.py``` in a terminal to run the script.

## Note

The images retrieved by this script may be copyrighted, as displayed after the execution of the script.