# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:52:27 2026

@author: daphn
"""

import numpy as np

def spec1dread(filename):
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
    S=[]
    #skipping first four lines (=header lines)
    index +=3
    #checking for non-stationary data
    if index<len(lines) and lines[index].startswith('TIME'):
        time=1
        #check to increases index
    #get number of locations
    if index<len(lines) and lines[index].startswith('LOCATION'):
        index +=1
        nloc = int(lines[index].split()[0])
        index+=1 
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
    for _ in range(nfreq):
        f = lines[index]
        f=float(f)
        freq.append(f)
        index+=1
    
    #reading spectra
    if index<len(lines) and lines[index].startswith('QUANT'):
        index+=1 
        quant=int(lines[index].split()[0])
        index+=1
        
    index+=3
    if index<len(lines) and lines[index].startswith('CDIR'):
        print(lines[index])
    index+=5
    if time == 0:
        for ii in range(nloc):
            if index>=len(lines):
                break
            index+=1
            if index<len(lines) and lines[index].startswith('NODATA'):
                index+=1
            if index<len(lines) and lines[index].startswith('LOCATI'):
                index+=1 
                spec=[]
                dire=[]
                spr=[]
                for j in range(nfreq):
                    if index >= len(lines):
                        break
                    spec_line = lines[index].split()
                    spec_line[0], spec_line[1], spec_line[2] = float(spec_line[0]), float(spec_line[1]), float(spec_line[2])
                    spec.append(spec_line[0])
                    dire.append(spec_line[1])
                    spr.append(spec_line[2])
                    index+=1
                
                S.append({'f':freq,'S':spec,'dir':dire,'spread':spr, 'pos':[x[ii],y[ii]],'type':'freq'})
                index-=1 
                
    return S
