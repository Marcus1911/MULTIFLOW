#!/bin/sh

echo "\n Welcome to Multiflow Script. The following demo will reproduce all graphs and testbeds \n"
echo "Searching fundamental library..."

sudo apt-get update
sudo apt-get install python-numpy pypy python-matplotlib ipython python-networkx python-setuptools mininet

cd ~/
git clone git://github.com/noxrepo/pox.git
cd pox
git checkout dart
cp ~/MULTIFLOW/Multiflow-Discrete-Time-1.py ../pox/ext/
cp ~/MULTIFLOW/Multiflow-Discrete-Time-2.py ../pox/ext/






