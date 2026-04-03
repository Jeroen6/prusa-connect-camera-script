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
(Check `crontab -l` or `crontab -e` to do manually)

## And on Windows?
Put a shortcut to the .py file in `C:\Users\%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
Make sure "start in" points to the installation path.

## Debian/Proxmox CT maintenance
To install in debian proxmox, install a debian container. Using (these scripts)[https://community-scripts.org/scripts/debian] for example.

In it you need to install:
```
apt update
apt install git
apt install pip3
git clone https://github.com/Jeroen6/prusa-connect-camera-script.git
cd prusa-connect-camera-script
pip3 install -r requirements.txt
chmod +x *.sh
./cronjob.install.sh
cp secrets.py.example.py secrets.py
nano secrets.py
python3 prusa-connect-camera-upload.py &
``` 

Useful checks to see if autostart works after reboot:

**Check if running**
`pgrep -af prusa-connect-camera-upload.py && echo "running" || echo "not running"`

**Check cron logs**
`journalctl -u cron -b --no-pager | tail -n 120`

**Watch script logs**
`tail -f prusa-connect-camera-upload.log`
`tail -n 50 prusa-connect-camera-upload.log`
