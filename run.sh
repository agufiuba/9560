if [ $1 = 1 ]; then
	sudo mn --custom 1.py --topo t,$2,$3 --controller remote --arp --mac --switch ovsk
elif [ $1 = 2 ]; then
	sudo mn --custom 2.py --topo t,$2 --controller remote --arp --mac --switch ovsk
else
	echo "No soportado"
fi
