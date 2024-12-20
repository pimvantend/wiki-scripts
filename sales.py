#!/usr/bin/env python
# dit script is bedoeld om gedraaid te worden
# in de bash schil onder grass
import subprocess,os.path,glob
invoerlijst=glob.glob('./Pictures/gpx2/grave_*.gpx')
#invoerbestand='./Pictures/gpx2/bergen_(limburg).gpx'
for invoerbestand in invoerlijst:
  uitvoerkaart=os.path.basename(invoerbestand).replace('.gpx','')
  uitvoerkaart=uitvoerkaart.replace('(','').replace(')','').replace('-','')
  subprocess.call(['v.in.ogr','-o','-e',
                 '--verbose','--overwrite',
                 'input='+invoerbestand,
                 'output='+uitvoerkaart])
  subprocess.call(['v.db.select',uitvoerkaart])
  subprocess.call(['v.category',uitvoerkaart,'op=report'])
  subprocess.call(['v.to.lines','input='+uitvoerkaart,
                 'output='+uitvoerkaart+'_lines','--overwrite'])
  subprocess.call(['v.net',uitvoerkaart+'_lines',
                 'points='+uitvoerkaart,'out='+uitvoerkaart+'_net',
                 'op=connect','thresh=500','--overwrite'])
  subprocess.call(['v.net.salesman',uitvoerkaart+'_net',
                 'out='+uitvoerkaart+'_salesman','--overwrite',
                 'center_cats=1-99999','-g'])
  subprocess.call(['v.out.ogr', 'type=line', 'format=GPX',
                 '--verbose','--overwrite',
                 'input='+uitvoerkaart+'_salesman',
                 'output='+invoerbestand.replace('.gpx','_salesman.gpx')])
#  subprocess.call(['v.net.steiner',uitvoerkaart+'_net',
#                 'out='+uitvoerkaart+'_steiner','--overwrite',
#                 'terminal_cats=1-99999','-g'])
#  subprocess.call(['v.out.ogr', 'type=line', 'format=GPX',
#                 '--verbose','--overwrite',
#                 'input='+uitvoerkaart+'_steiner',
#                 'output='+invoerbestand.replace('.gpx','_steiner.gpx')])
  subprocess.call(['v.net.spanningtree','input='+uitvoerkaart+'_net',
                 'output='+uitvoerkaart+'_spanningtree','--overwrite','-g'])
  subprocess.call(['v.out.ogr', 'type=line', 'format=GPX',
                 '--verbose','--overwrite',
                 'input='+uitvoerkaart+'_spanningtree',
                 'output='+invoerbestand.replace('.gpx','_spanningtree.gpx')])
