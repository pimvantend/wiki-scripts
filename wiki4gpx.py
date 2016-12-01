#!/usr/bin/python
import mechanize
import cookielib
import re
internet=True
plaatsnaam='Bemmel'
#'Alkmaar_(plaats)'
#'Arnhem/Heijenoord_en_Lombok'
#if '/' in plaatsnaam or '_' in plaatsnaam:
instukken=False
doelbestand1=plaatsnaam.replace('/','')
doelbestand1=doelbestand1.replace('_','')
doelbestand1=doelbestand1.replace('(','-')
doelbestand1=doelbestand1.replace(')','')
#'monumenten.gpx'
#else:
doelbestand=doelbestand1.lower()+'.gpx'
doelbestand=open(doelbestand,'w')
# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(False)
br.set_debug_redirects(False)
br.set_debug_responses(False)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

if internet:
    r=br.open('http://nl.wikipedia.org/wiki/Lijst_van_gemeentelijke_monumenten_in_'+plaatsnaam)
else:
#    r=open(plaatsnaam)
    r=open('Lijst_van_gemeentelijke_monumenten_in_'+plaatsnaam)
doelbestand.write( '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
doelbestand.write( '<gpx version="1.1" creator="Locus Android"\n')
doelbestand.write( ' xmlns="http://www.topografix.com/GPX/1/1"\n')
doelbestand.write( ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
doelbestand.write( ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
doelbestand.write( ' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n')
doelbestand.write( ' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"\n')
doelbestand.write( ' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"\n')
doelbestand.write( ' xmlns:locus="http://www.locusmap.eu">\n')
regelnummer=0
betekenis={}
heelbestand=r.read()
heelbestand=heelbestand.replace('<br />\n','')
if '<th>Plaats<br' in heelbestand:
    dorpsnamen=True
else:
    dorpsnamen=False
r=heelbestand.split('\n')
for regel in r:
    regelnummer+=1
    if regelnummer in betekenis.keys():
	if betekenis[regelnummer]=='omschrijving':
#	    print regel
	    omschrijvingslijst=re.findall(r'<td>(.*?)</td>',regel)
	elif betekenis[regelnummer]=='jaartal':
	    jaarlijst=re.findall(r'<td>(.*?)</td>',regel)
	    jaar=jaarlijst[0]
	    jaar=jaar[:4]
	elif betekenis[regelnummer]=='adres':
#	    print regel
	    adreslijst=re.findall(r'<td>(.*?)</td>',regel)
	elif betekenis[regelnummer]=='dorp':
	    dorpsnaam=re.findall(r'<td>(.*?)</td>',regel)
	    omschrijvingslijst[0]+=' '+dorpsnaam[0]
	elif betekenis[regelnummer]=='opladen':
	    lonlijst=re.findall(r'lon=(.*?)"',regel)
	    latlijst=re.findall(r'lat=(.*?)&',regel)
#	    print '  <name>'+adreslijst[0]+' '+omschrijvingslijst[0]+' '+jaar+'</name>'
#	    print '# ',latlijst,lonlijst
	    naamtekst=adreslijst[0]+' '+omschrijvingslijst[0]
	    if instukken:
		naamtekst=naamtekst.replace('<i>','')
		naamtekst=naamtekst.replace('</i>','')
		vindtekst=re.findall(r'<a(.*?)>',naamtekst)
		if len(vindtekst)>0:
#		print '# '+vindtekst[0]
		    naamtekst=naamtekst.replace('<a'+vindtekst[0]+'>','')
		naamtekst=naamtekst.replace('</a>','')
		vindtekst=re.findall(r'<sup(.*?)>',naamtekst)
		if len(vindtekst)>0:
#		print '# '+vindtekst[0]
		    naamtekst=naamtekst.replace('<sup'+vindtekst[0]+'>','')
		naamtekst=naamtekst.replace('</sup>','')
	    vindtekst=re.findall(r'<(.*?)>',naamtekst)
	    for ding in vindtekst:
		naamtekst=naamtekst.replace('<'+ding+'>','')
	    if len(latlijst[0])>0:
		doelbestand.write('<wpt lat="'+latlijst[0]+'" lon="'+lonlijst[0]+'">\n')
		doelbestand.write('  <name>'+naamtekst+' '+'</name>\n')
		doelbestand.write('</wpt>\n')
    elif 'without_image' in regel:
	if not dorpsnamen:
	    betekenis[regelnummer+1]='omschrijving'
#	betekenis[regelnummer+2]='jaartal'
	    betekenis[regelnummer+3]='architect'
	    betekenis[regelnummer+4]='adres'
	    betekenis[regelnummer+5]='geohack'
	    betekenis[regelnummer+6]='nummer'
	    betekenis[regelnummer+7]='opladen'
	else:
	    betekenis[regelnummer+1]='omschrijving'
#	betekenis[regelnummer+2]='jaartal'
	    betekenis[regelnummer+3]='architect'
	    betekenis[regelnummer+4]='adres'
	    betekenis[regelnummer+5]='dorp'
	    betekenis[regelnummer+6]='geohack'
	    betekenis[regelnummer+7]='nummer'
	    betekenis[regelnummer+8]='opladen'
doelbestand.write('</gpx>\n')
exit()
