import sys,os,re,glob


from konfig import *

# felkeszules a futtatasra
# segedfuggvenyek

def cmdtorun(prog,lang):
  ret=" "+prog
  if lang=="octave":
    return OCTAVE_BIN+ret
  if lang=='python':
    return PYTHON_BIN+ret
  if lang=='julia':
    return JULIA_BIN+ret
#  if lang=='matlab': 
#    return MATLAB_BIN+ret
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
  prog,lang,feladat=0,0,0
  try:
    prog,lang,feladat=sys.argv[1:4]
  except:
    print(help())
    return []

  try:
    open(prog).close()
  except:
    print("nem található a "+prog)
    return []  

  cmd=cmdtorun(prog,lang)
  if len(cmd)<1:
    print("ismeretlen nyelv")
    return []

  fel_kvt=FELADAT_KVT+"/"+feladat
  if not os.path.isdir(fel_kvt):
    print("ismeretlen feladat")
    return []
    

  fel_io_kvt=fel_kvt+"/"+IO_KVT
  if not os.path.isdir(fel_io_kvt):
    print("nincs io könyvtára a feladatnak")
    return []


  in_lst=glob.glob(fel_io_kvt+"/*."+I_EXT)
  out_lst=glob.glob(fel_io_kvt+"/*."+O_EXT)
  #print(out_lst,flush=True)  

  if (len(in_lst)<1) or (len(in_lst) != len(out_lst)) or (set( v.split(".")[0] for v in in_lst) != set( v.split(".")[0] for v in out_lst)):
    print("probléma az io fájlokkal")
    return []

  return [cmd, in_lst, out_lst ]



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

    try: # tulzas?
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
