if [ $1 = 1 ]; then
	python pox/pox.py samples.spanning_tree
elif [ $1 = 2 ]; then
	cp f.py pox/pox/samples/firewall.py
	python pox/pox.py samples.firewall forwarding.l2_learning
else
	echo "No soportado"
fi
