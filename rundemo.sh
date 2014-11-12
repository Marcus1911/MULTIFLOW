#!/bin/sh


MyMenu()
{
	dialog --backtitle "Multiflow Demo" --title "Multiflow Demonstration" --menu "Move using [UP] [DOWN],[Enter] to\
Select" 15 90 3\
	CAPABLE/JOIN "Disjointed paths by MP_CAPABLE and MP_JOIN"\
	Hash-Table "Disjointed paths by using MP_JOIN Receiver tokens"\
	Admin-Edit "Edit Multiflow (Only for expert users)" 2>/tmp/menuitem.$$

	menuitem=`cat /tmp/menuitem.$$`

	opt=$?

	case $menuitem in
	CAPABLE/JOIN) ~/pox/pox.py Multiflow-Discrete-Time-1.py --filename=../MULTIFLOW/mptcp_test.pcap;;
	Hash-Table) ~/pox/pox.py Multiflow-Discrete-Time-2.py --filename=../MULTIFLOW/mptcp_test.pcap;;
	Admin-Edit) vim ../MULTIFLOW/mptcp_test.py;;
	esac	
        
}


dialog --title  "Multiflow Demonstration"  --backtitle  "Multiflow Demo "  --yesno  "\
Welcome to the Multiflow demonstration. Here we'll show the basically work of Multiflow. Do you want to proced with this Demo?" 9 50 

sel=$?
case $sel in
   0) MyMenu;;
   1) clear;; 
   255) echo "Canceled by user by pressing [ESC] key";;
esac
