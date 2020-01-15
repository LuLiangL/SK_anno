import os
import sys
from multiprocessing import Pool

inpath = ''
outpath = 'cut10Xout'
p_num = 1
barcodeLen = 16

for i in range(len(sys.argv)):
    if sys.argv[i] == '-i':
        inpath = sys.argv[i + 1]
    if sys.argv[i] == '-o':
        outpath = sys.argv[i + 1]
    if sys.argv[i] == '-t':
        p_num = int(sys.argv[i + 1])
    if sys.argv[i] == '-bl':
        barcodeLen = int(sys.argv[i + 1])
    if sys.argv[i] == '-h' or len(sys.argv) <= 2:
        print '''Cut 10X Genomic barcode
        Users:
        python fq2fa.py -i /in/path -o /out/path -t <int> -bl <int>
        -i fastq file input path, use all fastq file from input path
        -o output path
        -t Threads number(default: 1)
        -bl cut barcode length, in pair-ends R1 headd(default: 16)'''
        exit(0)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def cutBarcode(inFileP, outFileP_, BarcodeLen):
    outFileP = open(outFileP_, 'a+')
    countline = 0
    with open(inFileP) as f:
        for i in f:
            countline += 1
            if countline == 1:
                outFileP.writelines(i)
            if countline == 2:
                outFileP.writelines(i[BarcodeLen:])
            if countline == 3:
                outFileP.writelines(i)
            if countline >= 4:
                outFileP.writelines(i[BarcodeLen:])
                countline = 0
    print 'cut', inFileP, 'done'


def cpF(mvIn, mvOut):
    os.system('cp ' + mvIn + ' ' + mvOut)
    print 'cp', mvIn, 'done'


inFileList = os.listdir(inpath)
mkdir(outpath)
p = Pool(p_num)
for f in inFileList:
    if os.path.splitext(f)[1] == '.fastq' or os.path.splitext(f)[1] == '.fq':
        cutInFQ = inpath + f
        cutOutFQ = outpath + os.path.splitext(f)[0] + '_cutB' + os.path.splitext(f)[1]
        if os.path.splitext(f)[0][-6:-4] == 'R1':
            p.apply_async(cutBarcode, args=(cutInFQ, cutOutFQ, barcodeLen))
        if os.path.splitext(f)[0][-6:-4] == 'R2':
            p.apply_async(cpF, args=(cutInFQ, cutOutFQ))
p.close()
p.join()
