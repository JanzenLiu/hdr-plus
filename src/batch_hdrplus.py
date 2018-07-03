from subprocess import call
import os

# # 10 elems per line for easy counting
#
# #          0            1            2            3            4            5            6            7            8            9
# params = [(4.2, 1.05), (3.8, 1.30), (3.9, 1.10), (3.8, 1.10), (5.0, 1.00), (3.8, 1.50), (3.6, 1.10), (4.0, 1.15), (4.0, 1.00), (3.4, 1.35),
# #          10           11           12           13           14           15           16           17           18           19
# 		  (3.8, 1.45), (4.8, 1.20), (3.6, 1.25), (3.6, 1.25), (4.5, 1.40), (2.0, 1.75), (3.8, 1.00), (3.8, 1.20), (3.6, 1.40), (3.8, 1.42),
# #          20           21           22           23           24           25           26           27           28           29
# 		  (2.0, 1.45), (3.8, 1.45), (3.5, 1.35), (3.2, 1.25), (3.8, 1.20), (3.5, 1.20), (3.8, 1.35), (4.5, 1.45), (3.8, 1.35), (4.0, 1.30),
# #          30           31           32           33           34           35           36           37           38
# 		  (4.0, 1.45), (3.0, 1.35), (3.6, 1.30), (3.8, 1.30), (3.2, 1.30), (3.5, 1.40), (3.8, 1.40), (3.8, 1.55), (3.8, 1.55)]
#
# skip = []  # indices of bursts to skip (useful while tuning params)
# commands = []
#
# # run hdrplus with images with different parameters as input
# for burst in xrange(38):
# 	if burst in skip:
# 		continue
#
# 	(comp, gain) = params[burst]
# 	command = "./hdrplus"
# 	command += (" -c " + str(comp) + " -g " + str(gain))  # compression and gain
# 	command += " /afs/cs/academic/class/15769-f16/project/tebrooks/raws/"  # directory of input images
# 	command += (" /outputs/output" + str(burst) + ".png")  # path of output image
#
# 	for img in xrange(8):
# 		command += (" burst" + str(burst) + "_" + str(img) + ".CR2")  # input images
#
# 	commands += [command]
#
# for command in commands:
# 	call(command, shell=True)


def hdrplus(comp, gain, in_folder, out_folder, burst, n_input):
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)


    out_file = "{}.png".format(burst)
    command = "../build/hdrplus"
    command += (" -c {}".format(comp))  # compression
    command += (" -g {}".format(gain))  # gain
    command += " " + in_folder  # directory of input images
    command += " " + out_file  # path of output image

    for i in xrange(n_input):
        command += " " + "{}{}.dng".format(burst, i)  # input images

    out_path = os.path.join(out_folder, out_file)
    mv_command = "mv {} {}".format(os.path.join(in_folder, out_file), out_path)
    command = ";".join([command, mv_command])

    # print(command)
    call(command, shell=True)


hdrplus(comp=3.8, gain=1.1, in_folder="../input/175239/dng", out_folder="/home/likewise-open/SENSETIME/liuchengtsung/Desktop/hdr-plus/output",
        burst="20171106%2Fbursts%2F0006_20160721_175239_909%2Fpayload_N00", n_input=3)