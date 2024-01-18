#!/usr/bin/env python

import argparse
from termcolor import colored
import subprocess

parser = argparse.ArgumentParser(description="This can help to correct the G2A and C2T error types in your bacterial assembly.")
parser.add_argument("--read", type=str, metavar="", required=True, help="the path of duplex reads.")
parser.add_argument("--ref", type=str, metavar="", required=True, help="the bacterial assembly.")
parser.add_argument("--cpu", type=str, metavar="", required=False, help="the CPU number. (default:10)", default="10")
parser.add_argument("--bed", type=str, metavar="", required=False, help="the position of potential modification sites identified by Hammerhead.")

args = parser.parse_args()

def cmd_shell(cammands, string):
    process = Popen(cammands.split(' '), stdout=subprocess.DEVNULL, universal_newlines=True)
    process.wait()
    err = process.communicate()

    if process.returncode == 0:
        pass
    else:
    	print(colored(err, "red"))

def duplex_mapping():
	mapping = ["minimap2", "-ax", "map-ont", "-o", "duplex.sam", "-t", args.cpu, args.ref, args.read]
	view = ["samtools", "view", "-bS", "-F4", "-@", args.cpu, "-o", "duplex.bam", "duplex.sam"]
	sort = ["samtools", "sort", "-@", args.cpu, "-o", "duplex.sort.bam", "duplex.bam"]
	remove = ["rm", "duplex.sam", "duplex.bam"]
	mpileup = ['samtools', 'mpileup', '-q', '30','-l', args.bed ,'-f', args.ref , '--no-output-ins', '--no-output-ins', '--no-output-del', '--no-output-del', '--no-output-ends', '-o', 'duplex.mpileup.txt', 'duplex.sort.bam']

	for i, cmd in enumerate([mapping, view, sort, remove, mpileup]):
		try:
			subprocess.run(cmd, check=True)

		except subprocess.CalledProcessError as e:
			print(e.output)
			raise Exception("Data processing failed")	


def stats_num(input_base, input_string):
	data = {}

	if input_base == "A":
		num_A = input_string.count('.') + input_string.count(',')
		num_T = input_string.count('T') + input_string.count('t')
		num_C = input_string.count('C') + input_string.count('c')
		num_G = input_string.count('G') + input_string.count('g')

	elif input_base == "T":
		num_T = input_string.count('.') + input_string.count(',')
		num_A = input_string.count('A') + input_string.count('a')
		num_C = input_string.count('C') + input_string.count('c')
		num_G = input_string.count('G') + input_string.count('g')

	elif input_base == "C":
		num_C = input_string.count('.') + input_string.count(',')
		num_T = input_string.count('T') + input_string.count('t')
		num_A = input_string.count('A') + input_string.count('a')
		num_G = input_string.count('G') + input_string.count('g')

	elif input_base == "G":
		num_G = input_string.count('.') + input_string.count(',')
		num_T = input_string.count('T') + input_string.count('t')
		num_C = input_string.count('C') + input_string.count('c')
		num_A = input_string.count('A') + input_string.count('a')

	data["A"] = num_A
	data["T"] = num_T
	data["C"] = num_C
	data["G"] = num_G
	total = num_A + num_T + num_G + num_C

	if total != 0:
		P_A = num_A / total
		P_T = num_T / total
		P_G = num_G / total
		P_C = num_C / total
	else:
		P_A = 0
		P_T = 0
		P_G = 0
		P_C = 0

	mes = str(num_A) + "\t" + str(num_T) + "\t" + str(num_G) + "\t" + str(num_C) + "\t" + str(P_A) + "\t" + str(P_T) + "\t" + str(P_G) + "\t" + str(P_C)

	tmp1 = P_C
	tmp2 = P_G

	if P_C >= 0.3 and P_T >= 0.3:
		tmp1 = P_C * 1.5

	elif P_G >= 0.3 and P_A >= 0.3:
		tmp2 = P_G * 1.5

	max1 = max(P_A, P_T)
	max2 = max(tmp1, tmp2)
	max3 = max(max1, max2)

	if max3 == P_A:
		mes += "\tA"

	elif max3 == tmp2:
		mes += "\tG"

	elif max3 == P_T:
		mes += "\tT"

	elif max3 == tmp1:
		mes += "\tC"	

	return(mes)


def loading_info():
	outfile = open("corrected_site.bed", "w")
	outfile.write("chr\tpos\tbase\tN_A\tN_T\tN_G\tN_C\tP_A\tP_T\tP_G\tP_C\tpolish_base\n")
	with open("duplex.mpileup.txt") as ff:
		for i in ff:
			i = i.replace("\n", "")
			i = i.split("\t")
			chr = i[0]
			pos = i[1]
			base = i[2]
			string = i[4]

			if i[3] != 0:
				fre = stats_num(base, string)
				if base != fre.split("\t")[8]:		
					if base == "C" and float(fre.split("\t")[5]) >= 0.6 and float(fre.split("\t")[5]) < 1.0:
						# print(colored(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre), "red"))
						outfile.write(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre) + "\t*\n")
					elif str(base.upper()) == "G" and float(fre.split("\t")[4]) >= 0.6 and float(fre.split("\t")[4]) < 1.0:
						# print(colored(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre), "red"))
						outfile.write(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre) + "\t*\n")
					else:
						# print(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre))
						outfile.write(str(chr) + "\t" + str(pos) + "\t" + str(base) + "\t" + str(fre) + "\n") 
				else:
					pass

	ff.close()
	outfile.close()

if __name__=="__main__":
	duplex_mapping()
	loading_info()