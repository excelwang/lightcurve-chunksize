#!/usr/bin/python
import os, sys, socket

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
}
tblno = machine_tableno[socket.gethostname()]
startday=int(sys.argv[1])
stopday=int(sys.argv[2])

for i in range(startday, stopday+1):
    if i == 1:
       os.system("mclient gwacdb -e -s \"drop table assoc%d  \"" %tblno)
       os.system("mclient gwacdb -e -s \"create table assoc%d(uniqueid bigint, targetid bigint, type tinyint) \"" %tblno)
    cmd1="COPY INTO assoc%d FROM '/scratch/meng/gwac/gwac_pipeline/assoc%d.txt' delimiters ','" %(tblno,i)
    cmd="/usr/bin/time -f %e mclient gwacdb -e -s \""+cmd1+"\""
    print cmd
    os.system(cmd)
