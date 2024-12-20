#!/usr/bin/env python3
import urllib.request,urllib.parse
def wikihaald(gemeente,land,txtdirectory):
  aan=False
  gemeente1=gemeente.replace(r'/','-').replace(r"'",'')
  schrijfbestand=open(gemeente1.lower()+'.txt','wb')
  if land=='de':
    opvraging='https://de.wikipedia.org/w/index.php?title=Liste_der_Baudenkm%C3%A4ler_in_'+urllib.parse.quote(gemeente)+'&action=edit'
  else:
    opvraging='https://nl.wikipedia.org/w/index.php?title=Lijst_van_gemeentelijke_monumenten_in_'+urllib.parse.quote(gemeente)+'&action=edit'
  with urllib.request.urlopen(opvraging) as response:
    for regel in response:
      plaats=regel.find(b' name="wpTextbox1">')
      regel1=regel.replace(b'&amp;',b'&')
      regel1=regel1.replace(b'&lt;',b'<')
      if plaats>0:
        aan=True
        regel1=regel1[plaats+19:]
      if aan and regel.startswith(b'</textarea>'):
        aan=False
      if aan:
        schrijfbestand.write(regel1)
  schrijfbestand.close()

if __name__ == "__main__":
  import sys
  txtdirectory=sys.argv[-1]
  wikihaald(sys.argv[-2],'nl',txtdirectory)