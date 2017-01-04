#!/usr/bin/env python
import geocoder,re,time
bestand=open('venlo2.txt','r')
opvraging=''
for regel in bestand:
    if regel.startswith('| adres ='):
	reguliere=re.compile(r'\| adres =(.*?)$')
	straatlijst=reguliere.findall(regel)
	straat=straatlijst[0]
	straat=straat.replace('[','')
	straat=straat.replace(']','')
	straat=straat.replace(' bij ','')
	if ',' in straat:
	    locatiekomma=straat.find(',')
	    straat=straat[:locatiekomma]
	if r'/' in straat:
	    locatieslash=straat.find(r'/')
	    straat=straat[:locatieslash]
	if r'-' in straat:
	    locatiestreepje=straat.find(r'-')
	    straat=straat[:locatiestreepje]
#	    print straat
#	    exit()
	print regel[:-1]
    elif regel.startswith('| plaats ='):
	reguliere=re.compile(r'\| plaats =(.*?)$')
	plaatslijst=reguliere.findall(regel)
	plaats=plaatslijst[0]
	plaats=plaats.replace('[','')
	plaats=plaats.replace(']','')
	plaats=plaats.replace('Tegelen (Steyl)','Steyl')
	opvraging=straat+plaats+' The Netherlands'
	g=geocoder.osm(opvraging)
	if not postcodeaanwezig:
	    if 'addr:postal' in g.osm:
		print '| postcode = '+g.osm['addr:postal']
	    else:
		print '| postcode = '
	print regel[:-1]
    elif regel.startswith('| lat ='):
	if 'y' in g.osm and '5' not in regel:
	    print regel[:-1]+str(g.osm['y'])
	else:
	    print regel[:-1]
    elif regel.startswith('| lon ='):
	if 'x' in g.osm and '6' not in regel:
	    print regel[:-1]+str(g.osm['x'])
	else:
	    print regel[:-1]
    elif regel.startswith('| postcode ='):
	if '5' in regel:
	    print regel[:-1]
#	else:
#	    print regel[:-1]
	    postcodeaanwezig=True
	else:
	    postcodeaanwezig=False
    else:
#	time.sleep(0.1)
	print regel[:-1]