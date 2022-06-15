import os
import sys
import prosgrafana.cli.gui as g
sys.argv.append("dbname=karmanyaah user=karmanyaah password=" + os.environ.get("PGPWD")+ " host=debiandocker1.lab.bhscs2.club port=4001")

sys.argv.append(os.environ.get("PGTABLE"))
g.gui('')
