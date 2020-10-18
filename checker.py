from aprosagok import *

# kell a tmp
if not os.path.exists("tmp"): os.makedirs("tmp")

print()
ret = precheck()
if len(ret)>0:
  [cmd,in_lst,out_lst]=ret
  #print(cmd)


  for infile in in_lst:
    [eleje,vege]=infile.split(".")
    print('---> {0:s} ---> '.format(eleje),end='')
    res=os.system(cmd+"< "+ infile + " > tmp/o")
    if res!=0:
      print('futás közbeni hiba')
      continue
    print(compare(tokensof("tmp/o"),tokensof(eleje+"."+O_EXT)))

print()
sys.stdout.flush()