from subprocess import call

for burst in xrange(38):
	# -w        Use camera white balance, if possible
	# -k <num>  Set the darkness level
    # -g <p ts> Set custom gamma curve (default = 2.222 4.5)
    # -S <num>  Set the saturation level
    # -W        Don't automatically brighten the image
	command = "../tools/dcraw -w -k 2050 -g 2.4 12.92 -S 15464 -W /afs/cs/academic/class/15769-f16/project/tebrooks/raws/burst" + str(burst) + "_0.CR2"

	call(command, shell=True)

