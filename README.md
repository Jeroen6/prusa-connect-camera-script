# prusa-connect-camera-script
Python script to upload Octoprint camera to PrusaConnect API

This scripts pulls a still from OctoPrint and uploads it to the Prusa Connect API

https://connect.prusa3d.com/docs/cameras/#tag/cameras

## How to setup?
- Create your variant of `secrets.py` based on the given example file.
- Run the script `./prusa-connect-camera-upload.py &`

## How to automatically start it on boot
Run `./cronjob_install.sh`

## How to stop the script
Run `./cronjob_stop.sh`

## And on Windows?
Put a shortcut to the .py file in `C:\Users\%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
Make sure "start in" points to the installation path.