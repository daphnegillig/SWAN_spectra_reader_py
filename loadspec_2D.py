# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:52:27 2026

@author: daphne_seaphysics
"""

import numpy as np

def spec2dread(filename):
    try:
        with open(filename,'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError
    #initialize variables
    time = 0
    nloc=0
    index=0
    x,y=[],[]
    nfreq=0
    freq=[]
    ndir=0
    dire=[]
    factor=[]
    S=[]
    #skipping first four lines (=header lines)
    index +=3
    #checking for non-stationary data
    if index<len(lines) and lines[index].startswith('TIME'):
        time=1
        print('time dependent')
        index+=2 
        print(lines[index])
    #get number of locations for timedependent
    if index<len(lines) and lines[index].startswith('LONLAT'):
        index+=1 
        nloc= int(lines[index].split()[0])
        index+=1 
        print(f'{nloc} locations in spherical coordinates')
    #get number of locations
    if index<len(lines) and lines[index].startswith('LOCATION'):
        index +=1
        nloc = int(lines[index].split()[0])
        index+=1 
        print(f'{nloc} locations')
    #append locations to x and y arrays
    for _ in range(nloc):
        if index<len(lines):
            coords = list(map(float, lines[index].split()))
            x.append(coords[0])
            y.append(coords[1])
            index +=1

    if index<len(lines) and lines[index].startswith('AFREQ'):
        index+=1 
        nfreq = int(lines[index].split()[0])
        index+=1
        print(f'{nfreq} frequencies')
    for _ in range(nfreq):
        f = lines[index]
        f=float(f)
        freq.append(f)
        index+=1
        
    if index<len(lines) and lines[index].startswith('CDIR'):
        print(lines[index])
        index+=1
        ndir = int(lines[index].split()[0])
        index+=1
        print(f'{ndir} directions')
    for _ in range(ndir):
        f=lines[index]
        f=float(f)
        dire.append(f)
        index+=1
    #reading spectra
    if index<len(lines) and lines[index].startswith('QUANT'):
        index+=1 
        quant=int(lines[index].split()[0])
        index+=1

    index+=3
    if time == 0:
        for ii in range(nloc):
            if index>=len(lines):
                break
            if lines[index].startswith('NODATA'):
                index+=1
            if lines[index].startswith('FACTOR'):
                index+=1 
                factor.append(lines[index].split()[0])
                index+=1
                spec_mat=[]
                for j in range(nfreq):
                    if index >= len(lines):
                        break
                    row = list(map(float,lines[index].split()))
                    spec_mat.append(row)
                    index+=1
                S.append({'f':freq,'dir':dire,'fact':factor,'S':spec_mat, 'pos':[x[ii],y[ii]],'type':'spec_2d'})
                print(f'loc {ii} ok')
    if time == 1:
        date=[]
        while index<len(lines):
            if lines[index].endswith('date and time'):
                date.append(lines[index].split()[0])
                print(lines[index].split()[0])
                index+=1
                for ii in range(nloc):
                    if index>=len(lines):
                        break
                    if lines[index].startswith('NODATA'):
                        index+=1
                    if lines[index].startswith('FACTOR'):
                        index+=1 
                        factor.append(lines[index].split()[0])
                        index+=1
                    spec_mat=[]
                    for j in range(nfreq):
                        if index >= len(lines):
                            break
                        if lines[index].startswith('****'):
                            index+=nfreq
                            print(lines[index])
                            break
                        if lines[index].startswith('ZERO'):
                            index+=1 
                            break
                        else:
                            row = list(map(float,lines[index].split()))
                            spec_mat.append(row)
                            index+=1
                    S.append({'f':freq,'dir':dire,'fact':factor,'S':spec_mat, 'date':date[-1],'pos':[x[ii],y[ii]],'type':'spec_2d'})
                    print(f'loc {ii} ok')
    print('done')
    return S

