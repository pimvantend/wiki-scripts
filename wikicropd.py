#!/usr/bin/env python3
telezen='soest1.txt'
west=7.95647
oost=8.21735
noord=51.62098
zuid=51.52320
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
