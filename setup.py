from setuptools import setup

setup(
    name='backend',
    version='0.0.1',
    packages=['backend'],
    include_package_data=True,
    install_requires=[
        'arrow==0.13.0',
        'bs4==0.0.1',
        'eventlet',
        'Flask==1.0.2',
        'flask-socketio',
        'gunicorn',
        'html5validator==0.3.1',
        'nodeenv==1.3.3',
        'pycodestyle==2.4.0',
        'pydocstyle==3.0.0',
        'pylint==2.2.2',
        'pymongo',
        'pytest==3.8.0',
        'requests==2.21.0',
        'sh==1.12.14',
    ],
)
