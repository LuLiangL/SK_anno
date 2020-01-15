import sys
import os
from multiprocessing import Pool

inpath = ''
outpath = ''
p_num = 1
prefixN = 'IP_out'
for i in range(len(sys.argv)):
    if sys.argv[i] == '-p':
        p_num = int(sys.argv[i + 1])
    if sys.argv[i] == '-i':
        inpath = sys.argv[i + 1]
    if sys.argv[i] == '-o':
        outpath = sys.argv[i + 1]
    if sys.argv[i] == '-n':
        prefixN = sys.argv[i + 1]
    if sys.argv[i] == '-h' or len(sys.argv) <= 2:
        print '''Mult process run interproscan
        Users:
        python MultRunInterpro.py -i /input/foleder/ -o /output/path/ -n <prefix> -p <int>

        -i input folder
        -o output path 
        -n prefix name
        -p process num'''
        exit(0)

def runInterPro(inP, outP):
    InterproCMD = '/home/software/interproscan-5.22-61.0/interproscan.sh -f XML -f HTML -iprlookup -goterms '
    inputCMD = '-i ' + inP + ' '
    outputCMD = '-b ' + outP
    logOut = ' &> ' + outP + 'interproOut.log'
    os.system(InterproCMD + inputCMD + outputCMD + logOut)
    print inP, 'done'


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


print '''Mult InterPro start
-----------------
'''
print 'Input File path: ', inpath
print 'Process use:     ', p_num
print 'Output path:     ', outpath
print 'Output prefix:   ', prefixN
inFilelist = os.listdir(inpath)
print 'All file list:   ', inFilelist

p = Pool(p_num)
for file in inFilelist:
    mkdir(outpath + '/' + os.path.splitext(file)[0] + '/' + prefixN)
    p.apply_async(runInterPro, args=(inpath + file, outpath + '/' + os.path.splitext(file)[0] + '/' + prefixN + '/'))

p.close()
p.join()