from base64 import b64encode, b64decode
import pickle
import os

storage_file = "picklejar/"
extension = ".pickle.b64"

def save(obj, name):
	global storage_file, extension
	open(storage_file + name + extension, "w").write(b64encode(pickle.dumps(obj)))

def load(name):
	global storage_file, extension
	return pickle.loads(b64decode(open(storage_file + name + extension, "r").read()))

def remove(name):
	global storage_file, extension
	os.remove(storage_file + name + extension)