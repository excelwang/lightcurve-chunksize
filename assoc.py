import sys,os,numpy as np, multiprocessing as mp

startday=int(sys.argv[1])
stopday=int(sys.argv[2])
tarcnt=173000

def getassocn(day):
    cmd="./assocn %d %ld" %(day,long(tarcnt))
    os.system(cmd) 
    print "finish day %d assoc generation." %day

def multiassocn(startday, stopday):
    pool = mp.Pool(mp.cpu_count()-1)
    results = [pool.apply_async(getassocn, args=(x,)) for x in range(startday, stopday+1)]
    output = [p.get() for p in results]
    pool.close()
    pool.join()

multiassocn(startday, stopday)
