import subprocess
import argparse
from termcolor import colored
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description="A tool help to find the potential modification sites")
parser.add_argument("--ref", type=str, metavar="", required=True, help="Input reference (FASTA)")
parser.add_argument("--read", type=str, metavar="", required=True, help="Input reads (FASTQ)")
parser.add_argument("--cpu", type=str, metavar="", required=False, help="CPU number. (default:10)", default="10")
parser.add_argument("--cut", type=float, metavar="", required=False, help="Cutoff value [0, 1]. (default:0.35)", default=0.35)
parser.add_argument("--min_depth", type=int, metavar="", required=False, help="The minimum depth. (default:50)", default=50)
parser.add_argument("--min_depth_strand", type=int, metavar="", required=False, help="The minimum depth for forward strand and reverse strand. (default:25)", default=25)
args = parser.parse_args()

def cmd_shell(cammands, string):
    process = Popen(cammands.split(' '), stdout=subprocess.DEVNULL, universal_newlines=True)
    process.wait()
    err = process.communicate()

    if process.returncode == 0:
        pass
    else:
    	print(colored(err, "red"))

def Preprocess():
	mapping = ["minimap2", "-ax", "map-ont", "-o", "mapping.sam", "-t", args.cpu, args.ref, args.read]
	view = ["samtools", "view", "-bS", "-F4", "-@", args.cpu, "-o", "mapping.bam", "mapping.sam"]
	sort = ["samtools", "sort", "-@", args.cpu, "-o", "mapping.sort.bam", "mapping.bam"]
	remove = ["rm", "mapping.sam", "mapping.bam"]
	mpileup = ['samtools', 'mpileup', '-q', '30', '--no-output-ins', '--no-output-ins', '--no-output-del', '--no-output-del', '--no-output-ends', '-o', 'mapping.mpileup.txt', 'mapping.sort.bam']

	for i, cmd in enumerate([mapping, view, sort, remove, mpileup]):
		try:
			subprocess.run(cmd, check=True)

		except subprocess.CalledProcessError as e:
			print(e.output)
			raise Exception("Data processing failed")

def calculate_distance(chrom, pos, string, cutoff):
	def calcualte_abs(num_1, num_2, total_1, total_2):
		value_1 = int(num_1)/int(total_1)
		value_2 = int(num_2)/int(total_2)
		abs_value = float(format(abs(value_1 - value_2), '.3f'))
		return(abs_value)

	dict = {}
	for i in string:
		dict[i] = dict.get(i, 0) + 1

	for i in ["A", "T", "G", "C", "a", "t", "g", "c"]:
		if i not in dict.keys():
			dict[str(i)] = 0 

	Forward_depth = dict["A"] + dict["C"] + dict["G"]+ dict["T"]
	Reverse_depth = dict["a"] + dict["c"] + dict["g"]+ dict["t"]
	min_depth = args.min_depth_strand

	if Forward_depth >= min_depth and Reverse_depth >= min_depth:
		absA = calcualte_abs(dict["A"], dict["a"], Forward_depth, Reverse_depth)
		absT = calcualte_abs(dict["T"], dict["t"], Forward_depth, Reverse_depth) 
		absG = calcualte_abs(dict["G"], dict["g"], Forward_depth, Reverse_depth)
		absC = calcualte_abs(dict["C"], dict["c"], Forward_depth, Reverse_depth)
		Manhattan_distance = absA + absT + absC + absG
		MAE = float(format(Manhattan_distance / 2, '.3f'))

		if MAE >= float(cutoff):
			mes = str(chrom) + "\t" + str(pos) + "\t" + str(MAE) + "\t"
			mes += str(absA) + "\t" + str(absT) + "\t" + str(absG) + "\t" + str(absC) + "\t"
			mes += str(dict["A"]) + "," + str(dict["T"]) + "," + str(dict["G"]) + "," + str(dict["C"]) + ","
			mes += str(dict["a"]) + "," + str(dict["t"]) + "," + str(dict["g"]) + "," + str(dict["c"])
			return(mes)
	else:
		pass

def get_direction_info(cutoff):
	header = "Chr\tPos\tMAE\tabsA\tabsT\tabsG\tabsC\tA,T,G,C,a,t,g,c"
	with open("potential_modification_site_detail.txt", "w") as fo:
		fbed =  open("potential_modification_site_detail.bed", "w")
		fo.write(header + "\n")
		with open("mapping.mpileup.txt") as ff:
			for base in ff:
				base = base.replace("\n", "")
				base = base.split("\t")

				if int(base[3]) >= args.min_depth:
					chrom = str(base[0])
					pos = str(base[1])
					string = str(base[4])
					
					if calculate_distance(chrom, pos, string, float(cutoff)):
						fo.write(calculate_distance(chrom, pos, string, float(cutoff)) + "\n")
						fbed.write(str(chrom) + "\t" + str(int(pos) - 1) + "\t" + str(pos) + "\n")
		ff.close()
	fo.close()
	fbed.close()

if __name__=="__main__":
	Preprocess()
	get_direction_info(args.cut)
