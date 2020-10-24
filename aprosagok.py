import sys,os,re,glob


from konfig import *

# felkeszules a futtatasra
# segedfuggvenyek

def cmdtorun(prog,lang):
  ret=" "+prog
  if lang=="octave":
    return OCTAVE_BIN+ret
  if lang=="python":
    return PYTHON_BIN+ret
  if lang=="julia":
    return JULIA_BIN+ret
  if lang=="binary":
    return ret
  return ""


def help():
  return """
    használat:
    python checker.py prog nyelv feladat
      a paraméterek:
      prog: a programod neve (elérési úttal)
      nyelv: a nyelv (octave,python,julia)
      feladat: a tesztelendő feladat (pl. bdaymin)
  """


# néhány előzetes ellenőrzés
def precheck():
  ret=dict()
  ret["msg"]="OK"
  while True:
    prog,lang,feladat=0,0,0
    try:
      prog,lang,feladat=sys.argv[1:4]
    except:
      ret["msg"]=help()
      break

    try:
      open(prog).close()
    except:
      ret["msg"]="nem található a "+prog
      break

    cmd=cmdtorun(prog,lang)
    if len(cmd)<1:
      ret["msg"]="ismeretlen nyelv"
      break
    ret["cmd"]=cmd

    fel_kvt=FELADAT_KVT+"/"+feladat
    if not os.path.isdir(fel_kvt):
      ret["msg"]="ismeretlen feladat"
      break
      
    fel_io_kvt=fel_kvt+"/"+IO_KVT
    if not os.path.isdir(fel_io_kvt):
      ret["msg"]="nincs io könyvtára a feladatnak"
      break


    in_lst=glob.glob(fel_io_kvt+"/*."+I_EXT)
    out_lst=glob.glob(fel_io_kvt+"/*."+O_EXT)
    #print(out_lst,flush=True)  

    if (len(in_lst)<1) or (len(in_lst) != len(out_lst)) or (set( v.split(".")[0] for v in in_lst) != set( v.split(".")[0] for v in out_lst)):
      ret["msg"]="probléma az io fájlokkal"
    ret["in_lst"]=in_lst
    ret["out_lst"]=out_lst
    break
  
  return ret



# a hivatalos es az aktualis megoldas osszehasonlitasa
# segedfuggvenyek
def tokensof(allomany):
  f=open(allomany)
  d=f.read().split()
  f.close()
  return [v.strip() for v in d if len(v.strip())>0 ] #paranoia

def compare(d,t):
  if len(d)!=len(t):
    return('az output sok/kevés tokent tartalmaz')
  for sd,st in zip(d,t):
    akt=str
    while True:
      try:
        float(st)
        "." in st
        akt=float
        break
      except:
        pass
      try:
        int(st)
        akt=int
        break
      except:
        pass
      break

    try: # tulzas? (str default...)
      akt(sd)
    except:
      return('hibás adat az outputban')

    vt=akt(st)
    vd=akt(sd)

    while True:
      if akt==str:
        if vt!=vd:
          return('sztring hiba')
      if akt==int:
        if abs(vt-vd)>INT_TOL:
          return('integer hiba')
      if akt==float:
        if abs(vt-vd)>FLOAT_TOL:
          return('lebegőpontos hiba')
      break
  return('OK')
