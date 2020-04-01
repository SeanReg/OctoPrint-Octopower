# coding=utf-8
from __future__ import absolute_import
import os
import json

import octoprint.plugin
from octoprint.printer.profile import PrinterProfileManager
from octoprint_OctoPower.plugmanager import PlugManager

from octoprint.events import Events

class OctopowerPlugin(octoprint.plugin.StartupPlugin,
						octoprint.plugin.SettingsPlugin,
						octoprint.plugin.TemplatePlugin,
						octoprint.plugin.EventHandlerPlugin,
						octoprint.plugin.SimpleApiPlugin):

	__plugManager = PlugManager()

	def get_api_commands(self):
		return dict(
			on=["printerProfile"],
			off=["printerProfile"]
			)

	def on_api_command(self, command, data):
		if command == "on":
			self._logger.info("Turning on " + data['printerProfile'])

			plug = self.__getPlugFromProfile(data['printerProfile'])
						
			if plug != None:
				plug.on()
		elif command == "off":
			self._logger.info("Turning off "  + data['printerProfile'])

			plug = self.__getPlugFromProfile(data['printerProfile'])
			
			if plug != None:
				plug.off()

	def get_settings_defaults(self):
		return dict(profiles=dict())

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	def get_template_vars(self):
		profiles = self._printer_profile_manager.get_all()
		profileNames = []
		for k in profiles.keys():
			profileNames.append(profiles[k]['name'])

		return dict(plugDevices=[{'name':x.getName(), 'uuid':x.getUUID()} for x in self.__plugManager.discoverPlugs()], profiles = profileNames)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._logger.info("Settings: " + json.dumps(data))

	def __getCurrentPlug(self):
			curProfile = self._printer_profile_manager.get_current_or_default()

			return self.__getPlugFromProfile(curProfile['name'])

	def __getPlugFromProfile(self, profileName):
			plugUUID = self._settings.get(['profiles'])[profileName]

			if plugUUID != "none":
				plug = self.__plugManager.findCachedPlug(plugUUID)
			else:
				return None

			return plug

	def on_event(self, event, payload):
		plug = self.__getCurrentPlug()

		if plug == None:
			return

		if event == Events.POWER_OFF:
			plug.off()
		elif event ==  Events.POWER_ON:
			plug.on()

		if event in (Events.PRINT_DONE, Events.PRINT_FAILED, Events.PRINT_CANCELLED):
			self._logger.info("Turning {} off".format(plug.getName()))

			self._printer.commands("M81")

			
		elif event in (Events.PRINT_STARTED, ):
			self._printer.commands("M80")
			plug.on()

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			OctoPower=dict(
				displayName="Octopower Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="SeanReg",
				repo="OctoPrint-Octopower",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/SeanReg/OctoPrint-Octopower/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Octopower Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctopowerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

