#!/usr/bin/env python

import re, os, sys
import numpy as np

def get_E( ofiles, E):

    pat = re.compile(r'Excitation energy :')
    for i in range(len( ofiles )):
        tmp = []
        for j in open(ofiles[i]).readlines():
            if pat.search(j):
                tmp.append( float(j[22:37] ) )
        if len(tmp) != len(E):
            print 'File %s has wrong number of roots' %ofiles[i]
            print 'fler rotter hittade';raise SystemExit
        for j in range(len(tmp)):
            E[j][i] = tmp[j]
    return E

def get_f( ofiles, f):

    pat = re.compile(r'Oscillator strength ')
    for i in range(len( ofiles )):
        tmp = []
        for j in open(ofiles[i]).readlines():
            if pat.search(j):
                tmp.append( float(j.split()[9] ) )
        if len(tmp) != 3*len(f):
            print 'File %s has wrong number of roots' %ofiles[i]
            print 'fler rotter hittade';raise SystemExit

        for j in range(len(tmp)):
            if j%3 == 0:
                f[j%8][i][0] = tmp[j]
            if j%3 == 1:
                f[j%8][i][1] = tmp[j]
            if j%3 == 2:
                f[j%8][i][2] = tmp[j]
    return f


def get_d( ofiles, d):
    pat = re.compile(r'STATE NO: +')
    for i in range(len( ofiles )):
        tmp = []
        for j in open(ofiles[i]).readlines():
            if pat.search(j):
                tmp.append( float(j.split()[6] ) )
        if len(tmp) != 3*len(d):
            print 'File %s has wrong number of roots' %ofiles[i]
            print 'fler rotter hittade';raise SystemExit

        for j in range(len(tmp)):
            if j%3 == 0:
                d[j%8][i][0] = tmp[j]
            if j%3 == 1:
                d[j%8][i][1] = tmp[j]
            if j%3 == 2:
                d[j%8][i][2] = tmp[j]
    return d



def run_argparse( ):
    import argparse
    A1 = argparse.ArgumentParser(add_help=False)
    A1.add_argument('-r','--roots', type = int, default = '6')
    A1.add_argument('--out', type = str)
#    A1.add_argument('--one', action='store_true', default = False)
    A1.add_argument('--spectra', action='store_true', default = False)
    args1  = A1.parse_args( sys.argv[1:] )
    return args1

def get_E( ofiles, E):
    pat = re.compile(r'Excitation energy :')
    for i in range(len( ofiles )):
        tmp = []
        for j in open(ofiles[i]).readlines():
            if pat.search(j):
                tmp.append( float(j[22:37] ) )
        if len(tmp) != len(E):
            print 'File %s has wrong number of roots' %ofiles[i]
            print 'fler rotter hittade';raise SystemExit
        for j in range(len(tmp)):
            E[j][i] = tmp[j]
    return E
def get_f( ofiles, f):
    N = len(f)
    M = len(ofiles)
    pat = re.compile(r'Oscillator strength ')
    for i in range(len( ofiles )):
        tmp = []
        for j in open(ofiles[i]).readlines():
            if pat.search(j):
                tmp.append( float(j.split()[5] ) )
        if len(tmp) != 3*len(f):
            print 'File %s has wrong number of roots' %ofiles[i]
            print 'fler rotter hittade';raise SystemExit

        x =[];y =[]; z=[]
        for j in range(len(tmp)):
            if j%3 == 0:
                x.append(tmp[j])
            if j%3 == 1:
                y.append(tmp[j])
            if j%3 == 2:
                z.append(tmp[j])
        if len(x) != N:
            print "wrong in f_get"
            raise SystemExit
        tmp = []
        for j in range(len(x)):
            tmp.append([])
            tmp[j] = [x[j], y[j], z[j]]

        for j in range(len(tmp)):
            f[j][i] = tmp[j]
    return f
def get_d( ofiles, d):
    pat = re.compile(r'STATE NO: +')
    N = len(d)
    for i in range(len( ofiles )):
        tmp = []
        for j in open(ofiles[i]).readlines():
            if pat.search(j):
                tmp.append( float(j.split()[6] ) )
        if len(tmp) != 3*len(d):
            print 'File %s has wrong number of roots' %ofiles[i]
            print 'fler rotter hittade';raise SystemExit

        for j in range(len(tmp)):
            if j%3 == 0:
                d[j%N][i][0] = tmp[j]
            if j%3 == 1:
                d[j%N][i][1] = tmp[j]
            if j%3 == 2:
                d[j%N][i][2] = tmp[j]
    return d

def main():
#Number of excitations N, configurations M
    args = run_argparse()
    N = args.roots
#Run in current directory
    cwd = os.getcwd()
    au2eV = 27.2116
    eV2au = 1./27.2116
    au2cm=219475.1598
    aunm= 45.562595

    ofiles = [f for f in os.listdir(cwd) if f.endswith('.out') ]

    if args.out:
        ofiles = [args.out]

    M = len(ofiles)
    if M == 0:
        print 'No dalton .out files detected, exiting ...'
        raise SystemExit

    pass
#Energy, osci, dipole
#E is in au, matrix N x M, f and d are tensor N x M x 3
    E = np.empty( (N,M) )
    f = np.empty( (N,M,3) )
    d = np.empty( (N,M,3) )

#pythagoras sum dipole is N x M

    d_mean = np.empty( (N,M) )

#average energy, oscillator str, dip moment, all are vectors size N x 1
    E_ave = np.empty( (N) )
    f_ave = np.empty( (N) )
    d_ave = np.empty( (N) )

#standard deviation, for E and d
    E_std = np.empty( (N) )
    d_std = np.empty( (N) )

#Retriving all data
    E = get_E(ofiles,E)
    f = get_f(ofiles,f)
    d = get_d(ofiles,d)

# Concert E to fitting value, now nanometer
    E = aunm /E 
#average energy N x 1
    for i in range(N):
        E_ave[i] = np.average(E[i])

#pythagoras sum dipole moment, N x M
    for i in range(N):
        for j in range(len(d[i])):
            d_mean[i][j] = np.sqrt(d[i][j][0]**2 + d[i][j][1]**2 + d[i][j][2]**2)

#average dipole
    for i in range(N):
        d_ave[i] = np.average(d_mean[i])
#average oscillator
    for i in range(N):
        tmp = []
        for j in range(len(f[i])):
            tmp.append( np.sum(f[i][j]) )
        f_ave[i] = np.sum(tmp)/M

#standard dev for E and d
    for i in range(N):
        d_std[i] = np.std(d_mean[i])
    for i in range(N):
        E_std[i] = np.std(E[i])
    if M == 1:
        for i in range(N):
            E_std[i] = 10.
#fit oscillators to energy
    x_init = E_ave - E_std
    x_end = E_ave + E_std
    n_inter = (x_end - x_init) +1

    mu = E_ave 
    sig = E_std 

    x = np.r_[250:1000:100j]
    y = np.empty( (N,len(x)) )

    for i in range(N):
        y[i] = f_ave[i] * np.exp( -(x - mu[i])**2/ (2*sig[i]**2))
############### PRINTING SECTION
#print out average values:
    print 'Printing out the average values'
    print "State\tEnergy [nm]\tOscillator strength:\t"
    for i in range(N):
        print "{0:2d}:\t{1:8f}\t{2:8f}".format(i+1,  E_ave[i] , f_ave[i])
#
#    print "State\tWavelength [nm]\t\tOscil.\t"
#    for i in range(N):
#        print "{0:2d}:\t{1:8f}\t{2:8f}".format(i+1,aunm / E_ave[i] ,f_ave[i], )
#    print "\nThe highest wavelengths are:"
#    print "  ".join(map(lambda x:"%.2f"%x, aunm / E_ave[:4] ))
#
#    print "\nState\tWavenumber [cm^-1]\tWavelength [au]\t"
#    for i in range(N):
#        print "{0:2d}:\t{1:8f}\t\t{2:8f}".format(i+1,f_ave[i], aunm / E_ave[i])

############### WRITING SECTION
#define name of files to be written, spectra1, spectra2 .., spectraN
    if not args.spectra:
        sys.exit()


    wfiles = []
    if args.out:
        #Write spectra for one file
        for i in range(N):
            wfiles.append( os.path.join(cwd,'%s_spectra%s'%(args.out.rstrip('.out').lstrip('opa_'),str(i+1) )) )
        for i in range(N):
            f = open(wfiles[i], 'w')
            for j in range(len(x)):
                f.write( "{0:20s}{1:20s}\n".format( str(x[j]),str(y[i][j])) )
#write spectraTOT
        f = open( os.path.join(cwd,'%s_spectraTOT'%args.out.rstrip('.out').lstrip('opa_')), 'w')
        for i in range(len(x)):
            f.write( "{0:20s}{1:20s}\n".format( str(x[i]),str(np.sum(y[:,i])) )) 

    else:
#Write spectra for combination of files
        for i in range(N):
            wfiles.append( os.path.join(cwd,'ave_spectra%s'% str(i+1) )) 
        for i in range(N):
            f = open(wfiles[i], 'w')
            for j in range(len(x)):
                f.write( "{0:20s}{1:20s}\n".format( str(x[j]),str(y[i][j])) )
#write spectraTOT
        f = open( os.path.join(cwd,'ave_spectraTOT'), 'w')
        for i in range(len(x)):
            f.write( "{0:20s}{1:20s}\n".format( str(x[i]),str(np.sum(y[:,i])) )) 




if __name__ == "__main__":
    main()
