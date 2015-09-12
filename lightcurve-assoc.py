import scipy as S
import monetdb.sql     #need sudo ipython
import os, socket, sys
machine_tableno = {
    'stones01.scilens.private' :   0,
    'stones02.scilens.private' :   1,
    'stones03.scilens.private' :   2,
    'stones04.scilens.private' :   3,
    'stones05.scilens.private' :   4,
    'stones06.scilens.private' :   5,
    'stones07.scilens.private' :   6,
    'stones08.scilens.private' :   7,
    'stones09.scilens.private' :   8,
    'stones10.scilens.private' :   9,
    'stones11.scilens.private' :   10,
    'stones12.scilens.private' :   11,
    'stones13.scilens.private' :   12,
    'stones14.scilens.private' :   13,
    'stones15.scilens.private' :   14,
    'stones16.scilens.private' :   15,
    'gwacdb'                   :   16
}
tblno = machine_tableno[socket.gethostname()]

def draw_flux(uid, mitosis):
    connection = monetdb.sql.connect(username="monetdb", password="monetdb", hostname="localhost", database="gwacdb")
    cursor = connection.cursor()
    cursor.arraysize = 100

    if mitosis == False:
        print "disable mitosis optimizer pipe"
        cursor.execute("set optimizer='no_mitosis_pipe';")
    cursor.execute("declare table tmp(flux double, imageid int)")
    cursor.execute('insert into tmp select flux,imageid from targets%d t, (select targetid from assoc%d where uniqueid=%d and type=3) t0 where t.id=t0.targetid;' %(tblno,tblno,uid))
    cursor.execute('select i.jd, tmp.flux from tmp, image%d i where tmp.imageid=i.imageid' %tblno)
    mylist=cursor.fetchall()
    dd = S.array(mylist)   #convert list to array
    #S.savetxt("lightcurve_jd_flux_%d.txt" %uid,dd)

    if dd.size == 0:
        print "source "+str(uid)+" has no targetid in assoc%d." %tblno
    else:
        print "source "+str(uid)+" has %d targetid in assoc%d." %(len(dd),tblno)

    cursor.close()
    connection.close()
    return dd

uniqueid=int(sys.argv[1])
mitosis=int(sys.argv[2])
draw_flux(uniqueid, mitosis)
