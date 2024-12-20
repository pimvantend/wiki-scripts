#!/usr/bin/env python3
import glob
apparaatidentificatie=glob.glob(r'/storage/')
if len(apparaatidentificatie) == 0:
  txtdirectory=r'./'
  gpxdirectory=r'../gpx2/'
  plaatjesdirectory=r'/home/zeeman/Pictures/'
  coredirectory=r'../../core/'
else:
  txtdirectory=r'/storage/sdcard/'
  gpxdirectory=r'/storage/sdcard/'
  plaatjesdirectory=r'/storage/sdcard/'
  coredirectory=r'/storage/sdcard/'
#import piexif
#wikihaald
import re
import subprocess
import sys
appendofwrite='w'
telezen='hengelo_(overijssel).txt'
dirvoorvoegsel='/home/zeeman/Pictures/170623-woestehoeve/'
datumwens='2021-08-02 16:24'
datum=datumwens
catwens="Hengelo,_Overijssel"
jaar='24'
gewensteplaats="Hengelo"
provincie='Overijssel'
if len(sys.argv)>1:
    optehalen=sys.argv[-1]
    print(optehalen)
    subprocess.call(['python3','./wikihaald.py',optehalen,txtdirectory])
    telezen=optehalen.lower().replace(r'/','-').replace("'",'')+'.txt'
#    print telezen
else:
    import piexif
sedbestandnaam=txtdirectory+telezen.replace('.txt','.bash')
sedbestand=open(sedbestandnaam,'w')
subprocess.call(['chmod','a+xwr',sedbestandnaam])
gpxbestandnaam=telezen.replace('.txt','.gpx')
gpxbestand=open(gpxdirectory+gpxbestandnaam,'w')
gpxbestand.write( '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
gpxbestand.write( '<gpx version="1.1" creator="Locus Android"\n')
gpxbestand.write( ' xmlns="http://www.topografix.com/GPX/1/1"\n')
gpxbestand.write( ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
gpxbestand.write( ' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"\n')
gpxbestand.write( ' xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n')
gpxbestand.write( ' xmlns:gpxtrkx="http://www.garmin.com/xmlschemas/TrackStatsExtension/v1"\n')
gpxbestand.write( ' xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v2"\n')
gpxbestand.write( ' xmlns:locus="http://www.locusmap.eu">\n')
wikibestand=open(txtdirectory+telezen,'r')
wikibestand=wikibestand.read()
wikibestand=wikibestand.replace('\n',' ')
if not(len(sys.argv)>1):
  opdrachtbestandsnaam=coredirectory+'oplaad-'+telezen.replace('.txt','.bash')
  opdrachtbestand=open(opdrachtbestandsnaam,appendofwrite)
  subprocess.call(['chmod','a+xwr',opdrachtbestandsnaam])
#print wikibestand
regulierltgt=re.compile('(<.*?>)')
lijstltgt=regulierltgt.findall(wikibestand)
for dingltgt in lijstltgt:
        wikibestand=wikibestand.replace(dingltgt,'')
#wikibestand=wikibestand.replace(' =','=')
wikibestand=wikibestand.replace('commonscat=','commonscat =')
wikibestand=wikibestand.replace('image=','image =')
reguliera=re.compile('({{[^T].*?}})')
lijst1=reguliera.findall(wikibestand)
#print lijst1
for ding in lijst1:
    wikibestand=wikibestand.replace(ding,'')
reguliere=re.compile('{{Tabelrij gemeentelijk monument(.*?)}')
lijst=reguliere.findall(wikibestand)
#print lijst
dictmeervoudige={}
dictiolijst=[]
regulierd=re.compile(r'([_a-z]*?) =')
reguliere=re.compile(r'(image)=')
regulierf=re.compile(r'=(.*?)\|')
regulierg=re.compile(r'image=(.*?)\.')
regulierh=re.compile(r'([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]\.JPG)')
for ding in lijst: #lijst bevat de tabelrijen
    ding+='|'
    dictio={}
    dictio['postcode']=''
    dictio['image']=''
    dictio['architect']=''
    dictio['commonscat']=''
    dictio['aangewezen']=''
    dictio['oorspr_fun']=''
    dictio['kadaster']=''
    dictio['bouwjaar']=''
#    print ding
    dinggesplitstlijst=ding.split('|')
#    print dinggesplitstlijst
    for iets in dinggesplitstlijst:
        ietslijst=iets.split('=')
        if len(ietslijst)==2 or len(ietslijst)==3:
            sleutel=ietslijst[0].strip()
            waarde=ietslijst[-1].strip()
            dictio[sleutel]=waarde
    plaatjesnaam=dictio['image'].strip()
    if plaatjesnaam=='' and 'lat' in list(dictio.keys()) and 'lon' in list(dictio.keys()):
#    if 'lat' in dictio.keys() and 'lon' in dictio.keys():
        if len(dictio['lat'])>0 and len(dictio['lon'])>0:
            gpxbestand.write('<wpt lat="'+dictio['lat']+'" lon="'+dictio['lon']+'">\n')
            gpxnaam='  <name>'+dictio['adres']+' '+dictio['object']
            gpxnaam+=' '+dictio['bouwjaar']
            gpxnaam=gpxnaam.replace(';','')
            gpxnaam=gpxnaam.replace('&','')
            gpxbestand.write(gpxnaam)
            gpxbestand.write('</name>\n')
            gpxbestand.write('</wpt>\n')
#    print plaatjesnaam
    lijst3=regulierh.findall(plaatjesnaam)
#    if plaatjesnaam.startswith('IMG_') and plaatjesnaam.endswith('.JPG'):
    if ( plaatjesnaam.startswith('06') or plaatjesnaam.startswith('IMG_') )\
    and (plaatjesnaam.endswith('.JPG') or (plaatjesnaam.endswith('.jpg') and\
    len(plaatjesnaam)==len('IMG_20240826_133126.jpg') ) ):
        lijst3=[plaatjesnaam]
    elif len(plaatjesnaam)>12:
        lijst3=[]
#    print lijst3
    if len(lijst3)==1:
#        print lijst3
#        print dictiolijst
        dictio['postcode']=dictio['postcode'][:4]+' '+dictio['postcode'][4:].strip()
        regurliera=re.compile('([0-9])')
        cijfermatch=regurliera.search(dictio['adres'])
        if cijfermatch:
            dictio['straatnaam']=dictio['adres'][:cijfermatch.start()].strip()
            dictio['huisnummer']=dictio['adres'][cijfermatch.start():].strip()
        else:
            dictio['straatnaam']=dictio['adres'].strip()
            dictio['huisnummer']=''
#        straat=dictio['adres'].split(' ')[0]
        if plaatjesnaam not in dictmeervoudige:
            dictmeervoudige[plaatjesnaam]=[]
            dictiolijst+=[dictio]
        else:
            dictmeervoudige[plaatjesnaam]+=[(dictio['objnr'],dictio['straatnaam'],dictio['huisnummer'],dictio['postcode'])]
#            print dictmeervoudige
for dictio in dictiolijst:
#        print dictio
        plaatjesnaam=dictio['image']
        dictio['plaats']=gewensteplaats
        plaats=dictio['plaats']
        if '.JPG' in plaatjesnaam:
          gewenstenaam=plaats.replace(' ','')+'-'+dictio['straatnaam'].lower().replace('.','').replace(' ','')+'-'+jaar+plaatjesnaam.lower()
        else:
          gewenstenaam=plaats.replace(' ','')+'-'+dictio['straatnaam'].lower().replace('.','').replace(' ','')+'-'+plaatjesnaam.lower()
        gewenstenaam=gewenstenaam.replace('img_','').replace(r'/','-')
        gewenstenaam=gewenstenaam.replace('-&apos;','')
        gewenstenaam=gewenstenaam.replace(';','')
        gewenstenaam=gewenstenaam.replace("'",'')
#        print
        oorspronkelijkenaam=plaatjesnaam
        sedbestand.write(r'sed -i "s/'+oorspronkelijkenaam+r'/'+gewenstenaam+r'/" "'+telezen+'"\n')
        plaatjezoeken=glob.glob(plaatjesdirectory+jaar+'*/'+oorspronkelijkenaam)
        if len(plaatjezoeken)==1:
            oorspronkelijkpad=plaatjezoeken[0]
        else:
            oorspronkelijkpad=dirvoorvoegsel+oorspronkelijkenaam
        beschrijving='== {{int:filedesc}} ==\n{{Information\n'
        if dictio['object']=='':
            beschrijving+='|description={{nl|1='+'Gemeentelijk monument'
        else:
            beschrijving+='|description={{nl|1='+dictio['object']
        if not dictio['architect']=='':
            beschrijving+=', architect '+dictio['architect']
        if not dictio['bouwjaar']=='':
            beschrijving+=', bouwjaar '+dictio['bouwjaar']
        if not dictio['aangewezen']=='':
            beschrijving+=', gemeentelijk monument sinds '+dictio['aangewezen']
        if not dictio['oorspr_fun']=='':
            beschrijving+=', oorspronkelijk '+dictio['oorspr_fun']
        if not dictio['kadaster']=='':
            beschrijving+=', kadasteraanduiding '+dictio['kadaster']
#++', '+dictio['postcode']+' '+dictio['plaats']+'\n'
        beschrijving+='}}'
        beschrijving+='{{Gemeentelijk monument|'+dictio['gemcode']+'/'+dictio['objnr']+'}}\n'
        for ding2 in dictmeervoudige[plaatjesnaam]:
            (objnr2,straatnaam2,huisnummer2,postcode2)=ding2
            beschrijving+='{{Gemeentelijk monument|'+dictio['gemcode']+'/'+objnr2+'}}\n'
        beschrijving+='{{Building address\n'
#        adresbestanddelenlijst=dictio['adres'].rsplit()
#        straatnaam=' '.join(adresbestanddelenlijst[:-1])
#        huisnummer=adresbestanddelenlijst[-1]
        beschrijving+='| Street name = '+dictio['straatnaam']+'\n'
        beschrijving+='| House number = '+dictio['huisnummer']+'\n'
        beschrijving+='| Postal code = '+dictio['postcode']+'\n'
        beschrijving+='| City = '+dictio['plaats']+'\n'
        beschrijving+='| State = '+provincie+'\n'
        beschrijving+='| Country = NL'+'\n'
        beschrijving+='}}\n'
        for ding2 in dictmeervoudige[plaatjesnaam]:
            (objnr2,straatnaam2,huisnummer2,postcode2)=ding2
            beschrijving+='{{Building address\n'
            beschrijving+='| Street name = '+straatnaam2+'\n'
            beschrijving+='| House number = '+huisnummer2+'\n'
            beschrijving+='| Postal code = '+postcode2+'\n'
            beschrijving+='| City = '+dictio['plaats']+'\n'
            beschrijving+='| State = '+provincie+'\n'
            beschrijving+='| Country = NL'+'\n'
            beschrijving+='}}\n'
        beschrijving=beschrijving.replace('[[','').replace(']]','')
        exifdict=piexif.load(oorspronkelijkpad)
        for ifd in ('0th','Exif','GPS','1st'):
            for tag in exifdict[ifd]:
                if piexif.TAGS[ifd][tag]["name"]=='DateTime':
                    print(exifdict[ifd][tag])
                    naarstring=str(exifdict[ifd][tag])
                    datum=naarstring.replace(':','-',2)
                    datum=str(datum).replace("b'",'')
                    datum=datum.replace("'",'')
                    print(datum)
        if datum<'2005':
            datum=datumwens
        beschrijving+='|date='+datum+'\n'
        beschrijving+='|source={{own}}'+'\n'
        beschrijving+='|author=[[User:Pimvantend|Pim van Tend]]'+'\n'
        beschrijving+='|permission='+'\n'
        beschrijving+='|other versions='+'\n'
        beschrijving+='}}\n'
        beschrijving+='{{Object location dec|'+dictio['lat']+'|'+dictio['lon']+'}}\n'
        beschrijving+='\n'
        beschrijving+='== {{int:license-header}} ==\n'
        beschrijving+='{{self|cc-by-sa-4.0}}\n'
        beschrijving+='\n'
        if dictio['commonscat']=='':
            beschrijving+='[[Category:Gemeentelijke monumenten in '+catwens+']]'
#            beschrijving+='[[Category:2023 in Hilversum']]'
#+'\n[[Category:Uploaded via Campaign:wlm-nl]]'+'\n{{Wiki Loves Monuments 2017|nl}}'
        else:
            beschrijving+='[[Category:'+dictio['commonscat']+']]'
#+'\n[[Category:Uploaded via Campaign:wlm-nl]]'+'\n{{Wiki Loves Monuments 2017|nl}}'
#        print beschrijving
        alsopdracht='python3 pwb.py scripts/upload.py '
        alsopdracht+='-filename:'+gewenstenaam+' '+oorspronkelijkpad+' "'+beschrijving+'"'
        if not(len(sys.argv)>1):
          opdrachtbestand.write(r'echo -e "\n\n"')
          opdrachtbestand.write(r'|')
          opdrachtbestand.write(alsopdracht)
          opdrachtbestand.write('\n')
gpxbestand.write('</gpx>\n')
gpxbestand.close()
