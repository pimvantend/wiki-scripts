#!/usr/bin/env python3
telezen='soest1.txt'
west=7.95647
oost=8.21735
noord=51.62098
zuid=51.52320
telezen='minden1.txt'
west=8.79574
oost=9.14177
noord=52.50378
zuid=52.25168
telezen='herford1.txt'
west=8.56608
oost=8.76573
noord=52.17635
zuid=52.05634
telezen='halle_(westfalen)1.txt'
west=8.0
oost=8.5
noord=53.0
zuid=51.0
telezen='werther_(westf.)1.txt'
west=8.29
oost=8.51
noord=52.13
zuid=52.02
telezen='unna1.txt'
west=7.63792
oost=7.82285
noord=51.61466
zuid=51.49755
telezen='höxter1.txt'
west=9.24908
oost=9.44958
noord=51.86844
zuid=51.69235
telezen='minden1.txt'
west=8.79454
oost=9.009225
noord=52.36778
zuid=51.25154
telezen='aachen-burtscheid1.txt'
west=6.08058
oost=6.12693
noord=50.77871
zuid=50.74246
telezen='aachen-walheim1.txt'
west=6.11789
oost=6.21333
noord=50.73732
zuid=50.67470
telezen='euskirchen1.txt'
west=6.70057
oost=6.90475
noord=50.80005
zuid=50.73186
telezen='aachen-mitte_(p–z)1.txt'
west=6.02797
oost=6.13646
noord=50.80222
zuid=50.67470
teschrijven=telezen.replace('1.txt','2.txt')
telezen=open(telezen,'r')
teschrijven=open(teschrijven,'w')
for regel in telezen:
  if regel.replace(' ','').startswith('|NS='):
    nsregel=regel
    nslijst=regel.split('=')
    nswaarde=nslijst[-1].strip()
  elif regel.replace(' ','').startswith('|EW='):
    ewregel=regel
    ewlijst=regel.split('=')
    ewwaarde=ewlijst[-1].strip()
    if len(ewwaarde)>0:
      nsfloat=float(nswaarde)
      ewfloat=float(ewwaarde)
      if nsfloat<noord and nsfloat>zuid and ewfloat>west and ewfloat<oost:
        teschrijven.write(nsregel)
        teschrijven.write(ewregel)
      else: # buiten gemeente
        positiensis=nsregel.find('=')
        positieewis=ewregel.find('=')
        teschrijven.write(nsregel[:positiensis+1]+'\n')
        teschrijven.write(ewregel[:positieewis+1]+'\n')
    else: # geen coordinaten aanwezig
      teschrijven.write(nsregel)
      teschrijven.write(ewregel)
  else: # niet een coordinatenregel
    teschrijven.write(regel)
#+'/n')
