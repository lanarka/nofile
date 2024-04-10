# Options
output_filename = "files.h"
var_type = "const uint8_t"
prefix = "NOFILE_"
# /Options

import sys
import time, datetime
from hashlib import sha256

ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
sha = lambda data: sha256(data.encode('utf-8')).hexdigest()

class Nofile:
	def __init__(self, files):
		print(files)
		self.files = files

	def proc_file(self, filename):
		data = list(self.load_file(filename))
		done = ""
		per_line = 0
		i = 0
		for b in data:
			i += 1
			if per_line > 15:
				done +="\n "
				per_line = 0
			comma = " " if (len(data)==i) else ","
			done += "0x%02x%s" % (b,comma)
			per_line +=1
		return done

	def load_file(self, filename):
		fh = open(filename, "rb")
		data = fh.read()
		fh.close()
		return data

	def proc_list(self, i, name):
		data = self.load_file(name)
		done = "/*** #%d: %s (%s Bytes) ***/\n" % (i, name, len(data))
		done += "#define %sNAME_%s \"%s\"\n" % (prefix, i, name)
		done += "#define %sHASH_%s 0x%s\n" % (prefix, i, sha(name))
		done += "#define %sSIZE_%s %s\n" % (prefix, i, len(data))
		done += "%s %sDATA_%s[] = {\n %s\n};\n\n" % (var_type, prefix, i, self.proc_file(name))
		done += "\n"
		return done

	def to_source(self):
		done=  "\n// Generated file do not modify !!!"
		done+= "\n// Timestamp: %s\n\n" % ts
		done+= "#ifndef __FILES_H__\n"
		done+= "#define __FILES_H__\n\n"
		count = total = 0
		for file in self.files:
			data = self.proc_list(count, file.strip())
			done += data
			total += len(data)
			count += 1
		done +="#endif\n"
		fh = open(output_filename, "w")
		fh.write(done)
		fh.close()
		print("* Done: Total data size: %d Bytes" % total)


def nofile(list_of_files):
	nf = Nofile(list_of_files)
	nf.to_source()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: %s <file> ..." % sys.argv[0])
		sys.exit()
	if len(sys.argv) > 1:
		files = sys.argv[1:]
		nofile(files)
