from setuptools import setup

setup(
    name='backend',
    version='0.0.1',
    packages=['backend'],
    include_package_data=True,
    install_requires=[
        'arrow>=0.14.2',
        'eventlet>=0.25.0',
        'flask>=1.1.1',
        'flask-session>=0.3.0',
        'flask-socketio>=4.1.0',
        'gunicorn',
        'nodeenv>=1.3.3',
        'pycodestyle==2.4.0',
        'pydocstyle==3.0.0',
        'pylint==2.2.2',
        'pymongo',
        'pytest==3.8.0',
        'requests==2.22.0',
        'sh==1.12.14',
    ],
)
