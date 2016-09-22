run:
	./py/bin/python run.py

env:
	virtualenv -p python3 py

deps:
	./py/bin/pip install -r requirements.txt

zwave:
	wget -O NodeDefender/iCPE/ZWave/__init__.py https://raw.githubusercontent.com/CTSNE/NodeDefender-ZWave/master/__init__.py
	wget -O NodeDefender/iCPE/ZWave/commandclasses.py https://raw.githubusercontent.com/CTSNE/NodeDefender-ZWave/master/commandclasses.py

db:
	./py/bin/python manage.py db init

dbmigrate:
	./py/bin/python manage.py db migrate

dbupgrade:
	./py/bin/python manage.py db upgrade

install: env deps zwave db dbmigrate dbupgrade
