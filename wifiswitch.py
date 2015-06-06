#!/usr/bin/python

import json
import requests
import datetime
import time

# define the api endpoint
api_endpoint = "https://api.particle.io/v1/"

# json file that has stored Photon info
photon_file = "photons.json"


class photon:
	# Photon object, one for each device

	def __init__(self, name, device_id, access_token, switch_pin, office, room, utc_reboot_hour, notes="none"):
		# constructor, all arguments required except notes
		self.name = name
		self.device_id = device_id
		self.access_token = access_token
		self.switch_pin = switch_pin
		self.office = office
		self.room = room
		self.utc_reboot_hour = utc_reboot_hour
		self.notes = notes

	def api_post(self, action, payload):
		# function to place api POST calls
		# payload is a dictionary of values that will be passed in the POST
		url = api_endpoint+"devices/"+self.device_id+"/"+action
		payload['access_token'] = self.access_token
		return requests.post(url, data=payload)

	def switch(self, state):
		# change state of switch_pin
		payload = {'params': self.switch_pin+","+state}
		return self.api_post("digitalwrite",payload)

	def on(self):
		# turn switch_pin ON
		return self.switch("HIGH")

	def off(self):
		# turn switch_pin OFF
		return self.switch("LOW")

# load objects from json
photons = []
with open(photon_file,'r') as fp:
	data = json.load(fp)
for item in data:
	photons.append(photon(**item))

# find systems that need to be rebooted during current hour
reboots = []
for p in photons:
	if p.utc_reboot_hour == datetime.datetime.utcnow().strftime('%H'):
		reboots.append(p)

# reboot identified systems
if reboots:
	for r in reboots:
		r.off()
	time.sleep(30)
	for r in reboots:
		r.on()
