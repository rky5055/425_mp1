import os
import logging
import pathlib
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class ConfigItem:
	def __init__(self,NodeID="", NodeHost="", NodePort=""):
		self.NodeID=NodeID   
		self.NodeHost=NodeHost
		self.NodePort=NodePort

def ConfigParser(path):
	configItems= ConfigItemsParser(path)
	return configItems

def ConfigItemsParser(path):
	absPath = pathlib.Path(path).absolute()
	print(absPath)
	with absPath.open("r") as f:
		configItems = []
		for line in f.readlines()[1:]:
			print(line)
			fields = line.split(" ")
			if len(fields) != 3:
				logging.error("Invalid input format")
				continue
			nodeIDStr = fields[0]
			nodeHostStr = fields[1]
			nodePortStr = int(fields[2])
			configItem = ConfigItem(nodeIDStr,nodeHostStr,nodePortStr)
			configItems.append(configItem)

	return configItems