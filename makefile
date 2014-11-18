
INSTALL_PATH=/usr/local/bin/yalap

install: yalap.py
	install yalap.py $(INSTALL_PATH)

remove: yalap.py
	rm $(INSTALL_PATH)
