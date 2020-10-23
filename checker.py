from aprosagok import *

# https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
from tabulate import tabulate

# kell a tmp
if not os.path.exists("tmp"): os.makedirs("tmp")

ret = precheck()

eredlista=[["precheck", ret["msg"]]]
if ret["msg"]=="OK":
  cmd=ret["cmd"]
  in_lst=ret["in_lst"]
  out_lst=ret["out_lst"]
  #print(cmd)



  for infile in in_lst:
    [eleje,vege]=infile.split(".")
    szam=eleje.split("/")[-1]
#    print('---> {0:s} ---> '.format(eleje),end='')
    res=os.system(cmd+"< "+ infile + " > tmp/o")
    if res!=0:
      res="futás közbeni hiba"
    else:
      res=compare(tokensof("tmp/o"),tokensof(eleje+"."+O_EXT))
    eredlista.append([szam,res])


print()
print(tabulate(eredlista, headers=["eset", "eredmény"]))
print()
sys.stdout.flush()