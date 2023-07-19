
from hashlib import sha256
sha = lambda data: sha256(data.encode('utf-8')).hexdigest()

import time, datetime
ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

output_filename = "files.h"

class Nofile:
	def __init__(self, files):
		self.files = files

	def proc_file(self, filename):
		code = list(self.load_file(filename))
		body = str([ "0x%02x" % b for b in code ])
		body = body.replace("]", "")
		body = body.replace("[", "")
		body = body.replace("'", "")
		body = body.replace(",", ",\n")
		return body

	def load_file(self, filename):
		fh = open(filename, "rb")
		data = fh.read()
		fh.close()
		return data

	def proc_list(self, i, name):
		data = self.load_file(name)
		done = "// *** %s #%d (%s Bytes) ***\n" % (name, i, len(data))
		done += "#define _NOFILE_NAME_%s \"%s\"\n" % (i, name)
		done += "#define _NOFILE_HASH_%s 0x%s\n" % (i, sha(name))
		done += "#define _NOFILE_SIZE_%s %s\n" % (i, len(data))
		done += "const uint8_t _NOFILE_DATA_%s[] = {\n %s\n};\n\n" % (i, self.proc_file(name))
		done += "\n"
		return done

	def to_source(self):
		done=  "\n// Generated file do not modify !!!"
		done+= "\n// Timestamp: %s\n\n" % ts
		done+= "#ifndef __NOFILE_H__\n"
		done+= "#define __NOFILE_H__\n\n"
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
		print("* Conversion done!")
		print("* Total data size: %d Bytes" % total)


def nofile(list_of_files):
	nf = Nofile(list_of_files)
	nf.to_source()

import sys
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: %s <file1> <file2> ..." % sys.argv[0])
		sys.exit()
	if len(sys.argv) > 1:
		files = sys.argv[-1:]
		nofile(files)
