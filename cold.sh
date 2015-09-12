#!/bin/bash
mclient gwacdb -e -s "select count(*) from assoc13;"
mitosis=1
nomitosis=0

echo
echo "1st run: uid=1 and cold no-mitosis."
sudo sysctl -w vm.swappiness=0
monetdb stop gwacdb
echo 3 |sudo tee /proc/sys/vm/drop_caches
monetdb start gwacdb
date
echo
echo "cold run no-MTS"
/usr/bin/time -f %e python lightcurve-assoc.py 1 $nomitosis

echo
echo "warm up no-MTS"
for run in {1..2}; do /usr/bin/time -f %e python lightcurve-assoc.py 1 $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)

echo
echo "hot runs no-MTS"
for run in {1..6}; do /usr/bin/time -f %e python lightcurve-assoc.py 1 $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)


echo "2nd run: RANDOM uid and cold no-mitosis."
sudo sysctl -w vm.swappiness=0
monetdb stop gwacdb
echo 3 |sudo tee /proc/sys/vm/drop_caches
monetdb start gwacdb
date
echo
echo "cold run no-MTS"
/usr/bin/time -f %e python lightcurve-assoc.py $RANDOM $nomitosis

echo
echo "warm up no-MTS"
for run in {1..2}; do /usr/bin/time -f %e python lightcurve-assoc.py $RANDOM $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)

echo
echo "hot runs no-MTS"
for run in {1..6}; do /usr/bin/time -f %e python lightcurve-assoc.py $RANDOM $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)


echo
echo "3rd run: RANDOM uid and cold mitosis."
sudo sysctl -w vm.swappiness=0
monetdb stop gwacdb
echo 3 |sudo tee /proc/sys/vm/drop_caches
free -g
monetdb start gwacdb
date

echo "cold run mitosis"
/usr/bin/time -f %e python lightcurve-assoc.py $RANDOM $mitosis

echo
echo "warm up no-mitosis"
for run in {1..2}; do /usr/bin/time -f %e python lightcurve-assoc.py $RANDOM $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)

echo
echo "hot runs no-mitosis"
for run in {1..6}; do /usr/bin/time -f %e python lightcurve-assoc.py $RANDOM $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)

echo
echo "4th run: uid=1 and cold mitosis."
sudo sysctl -w vm.swappiness=0
monetdb stop gwacdb
echo 3 |sudo tee /proc/sys/vm/drop_caches
monetdb start gwacdb
date

echo
echo "cold run MTS"
/usr/bin/time -f %e python lightcurve-assoc.py 1 $mitosis

echo
echo "warm up no-MTS"
for run in {1..2}; do /usr/bin/time -f %e python lightcurve-assoc.py 1 $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)

echo
echo "hot runs no-MTS"
for run in {1..6}; do /usr/bin/time -f %e python lightcurve-assoc.py 1 $nomitosis; done 2>&1 | tee >(grep -o ^[0-9.]* |awk '{print $1}' | ./minmaxavg)

