# wifiswitch
Basic switch control using Particle Photon

This is meant to be used with a Powerswitch Tail or other relay device connected to a Particle Photon wifi microcontroller.

The script will check photons.json and toggle the switch off and on if it is during the "reboot" hour specified for the photon.

Suggested usage is to set up an hourly crontab to run the python script.
