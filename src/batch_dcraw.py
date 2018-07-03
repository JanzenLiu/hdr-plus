from subprocess import call
import os

# for burst in xrange(38):
# 	# -w        Use camera white balance, if possible
# 	# -k <num>  Set the darkness level
#     # -g <p ts> Set custom gamma curve (default = 2.222 4.5)
#     # -S <num>  Set the saturation level
#     # -W        Don't automatically brighten the image
# 	command = "../tools/dcraw -w -k 2050 -g 2.4 12.92 -S 15464 -W /afs/cs/academic/class/15769-f16/project/tebrooks/raws/burst" + str(burst) + "_0.CR2"
# 	call(command, shell=True)

# parameter printed by -v -T
# Scaling with darkness 63, saturation 1023, and
# multipliers 2.413098 1.000000 1.231421 1.000000



out_folder = "../input/163256/tmp"
in_folder = "../input/163256/dng"
in_files = os.listdir(in_folder)


if not os.path.exists(out_folder):
    os.mkdir(out_folder)

for in_file in in_files:
    out_file = "{}.tiff".format(in_file.split(".")[0])
    out_path = os.path.join(out_folder, out_file)
    out_path_old = os.path.join(in_folder, out_file)
    in_path = os.path.join(in_folder, in_file)

    # run_command = "../tools/dcraw -w -k 2050 -g 2.4 12.92 -S 15464 -W {}".format(in_path)
    # run_command = "../tools/dcraw -v -w {}".format(in_path)
    # run_command = "../tools/dcraw -v -6 -w -g 1 1 -T -D {}".format(in_path)
    run_command = "../tools/dcraw -v -i {}".format(in_path)
    # run_command = "../tools/dcraw -v -D -6 -W -g 1 1 {}".format(in_path)
    move_command = "mv {} {}".format(out_path_old, out_path)

    call(";".join([run_command, move_command]), shell=True)
    # call(run_command, shell=True)
    break
