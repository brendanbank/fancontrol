import gzip
import ulogging as logging
import gc

log = logging.getLogger(__name__)

STATIC_DIR = "static"


def load_into(fiel):
    fiel = gzip.open(fiel)
    content = fiel.read()
    return(content)


def free(full=True):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

def main():
    print (free())
    
    fiel = '/Users/brendan/src/fancontrol/static/bootstrap.min.css.gz'
    content = load_into('/Users/brendan/src/fancontrol/static/bootstrap.min.css.gz')
    print(len(content))
    print (free())
    content = ""
    print (free())
    gc.collect()
    print (free())

if __name__ == '__main__':
    print (free())
    main()
    print (free())
