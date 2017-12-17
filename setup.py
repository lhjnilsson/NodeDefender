from setuptools import setup

setup(
    name="NodeDefender",
    description="Manage Nodes with CTS-iCPE",
    version="0.6",
    author="Henrik Nilsson",
    author_email="henrik.nilsson@ctsystem.se",
    license="BSD",
    url="https://github.com/CTSNE/NodeDefender",
    packages=['NodeDefender'],
    scripts=['manage.py'],
    entry_points = {
        'console_scripts' : ['nodedefender=nodedefender.bin.manage:main']
    },
    include_package_data=True,
    install_requires = [
        "alembic==0.9.1",
        "amqp==2.1.4",
        "aniso8601==1.2.0",
        "appdirs==1.4.2",
        "APScheduler==3.3.1",
        "bcrypt==3.1.3",
        "billiard==3.5.0.2",
        "blinker==1.4",
        "celery==4.0.2",
        "cffi==1.9.1",
        "click==6.7",
        "enum-compat==0.0.2",
        "eventlet==0.20.1",
        "Flask==0.12.1",
        "Flask-Assets==0.12",
        "Flask-Bcrypt==0.7.1",
        "Flask-Login==0.3.2",
        "Flask-Mail==0.9.1",
        "Flask-Migrate==2.0.3",
        "Flask-Moment==0.5.1",
        "Flask-RESTful==0.3.5",
        "Flask-Script==2.0.5",
        "Flask-SocketIO==2.8.5",
        "Flask-SQLAlchemy==2.2",
        "Flask-WTF==0.14.2",
        "geopy==1.11.0",
        "gevent==1.2.1",
        "greenlet==0.4.12",
        "itsdangerous==0.24",
        "Jinja2==2.9.6",
        "kombu==4.0.2",
        "Mako==1.0.6",
        "MarkupSafe==1.0",
        "packaging==16.8",
        "paho-mqtt==1.2",
        "passlib==1.7.1",
        "psycopg2==2.7.1",
        "pycparser==2.17",
        "PyMySQL",
        "pyparsing",
        "python-dateutil==2.6.0",
        "python-editor==1.0.3",
        "python-engineio==1.2.4",
        "python-socketio==1.7.1",
        "pytz==2016.10",
        "redis==2.10.5",
        "redlock==1.2.0",
        "requests==2.13.0",
        "six==1.10.0",
        "SQLAlchemy==1.1.6",
        "tzlocal==1.3",
        "vine==1.1.3",
        "webassets==0.12.1",
        "Werkzeug==0.12.1",
        "WTForms==2.1",
        "xmltodict==0.10.2",
        ],
        zip_safe=False)
