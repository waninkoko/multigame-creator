from struct import pack, unpack
import os, sys

def roundup(n, a):
	if (n % a):
		n += a - (n % a)
	return n


# Welcome message
print '+------------------------+'
print '| Multigame Creator v1.0 |'
print '| developed by Waninkoko |'
print '+------------------------+'
print '|  www.teknoconsolas.es  |'
print '+------------------------+'
print ''

# Given arguments
outfile = sys.argv[1]
infiles = sys.argv[2:]

# Open output file
outf = open(sys.argv[1], 'w')

# Write disc ID
outf.write("MGLW")

# Write number of entries
nbgames = pack(">I", len(infiles))
outf.write(nbgames)

# Write game entries
for filename in infiles:
	inf = open(filename, 'r')

	# Get game info
	header = inf.read(128)
	offset = pack(">Q", outf.tell())
	size   = pack(">Q", os.path.getsize(filename))

	inf.close()

	# Write game entry
	outf.write(header)
	outf.write(offset)
	outf.write(size)

# Alignment
outf.seek(roundup(outf.tell(), 0x20000))

# Write games
for filename in infiles:
	inf = open(filename, 'r')

	inf.seek(32)

	# Show gamename
	print '[+] Writing "{0}", please wait...'.format(inf.read(64))

	inf.seek(0)

	# Write game and align
	outf.write(inf.read())
	outf.seek(roundup(outf.tell(), 0x20000))

	inf.close()

print ''

# Close output file
outf.close()
