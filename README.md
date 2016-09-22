<img src="logo.png">
NodeDefender is an Open- Source program for controlling multiple Z-Wave devices connected to multiple gateways.
This programs is exclusivly designed to work with [CTS-iCPE](http://cts-icpe.com). 

Current version is Alpha-1 so do not expect this to be at it's full potential. More functions will be added in a rapid phase.

## Requirements
Before we can start we need to make sure we have all the tools needed. Below is a list of what is needed
```
 Linux System(OSX may work, not tested)
 Make
 virtualenv
```
## Quick install and run
This will get you up and running under a minute. After installation you should be able to access your application through 127.0.0.1:5000. Gunicorn can be added to run the application as a Deamon.
```sh
# Downloads NodeDefender- application
git pull https://github.com/ctsne/NodeDefender
# Changes into the downloaded application
cd NodeDefender
# Runs the Makefile and the steps explained below
make install
# Starts up the Application
./run.py
```
## Details of the Makefile and installation

>  Make env

Installs the python local virtualenv. So we dont install alot of otherwise not so used stuff in system- libary

> Make deps

Installs the requirements to the local enviroment. Flask and more

> Make zwave

Downloads the latest support of Z-Wave Classes 

> Make db

Make a local SQLite instance that will hold all the data used by the application. MySQL/ MariaDB and PostgreSQL support will be added later.

## Things to do before Beta- release
#### - [ ] Fix the Threading- issue

*Currently issues with Threading. System can lock itself when exiting, leave some threads as zombie. Just a few megabytes of the memory that will be wasted - but nevertheless something that needs to be fixed before "production-ready"*

#### - [ ] More system- logging to app.log

*All exceptions should be saved in app.log and information about node- states should be saved if Information- level is requested.*

#### - [ ] Mail Support

*Send mails to configured sources when specific events occur. Also for Account- validation*

#### - [ ] Make the frontend more modular and structured.

*Migrating the sourcecode over to Flask-Blueprints will provide a better structure.*

#### - [ ] Restful API Support

*Create a Restful API with support for Token- based authentication. Making it possible to use external applications to talk to it through Ajax and such.*

#### - [ ] Enahance MQTT Support

*Possibility to listen to more than 1 MQTT- channel. Authentication support and also support for encryption*

#### - [ ] Demostrate Basic Rules

*That an event should occur during a given time. Or that some event can trigger another. Configured to a user-friendly configuration.*

#### - [ ] Flask-Principal

*Ability to have teams and roles that can affect what you can se and do. Some iCPEs and Nodes could only be configured by a given Team. Admin, Technician and User could be some of the roles.*

#### - [ ] Overall better sctucture
 
*This will be ongoing for long time. But things should be as clear as possible for others to join the development*

#### - [ ] Collection of Node- Data and proper expression of it

*Collect Heat, power and other events and display then in an elegant way.*
