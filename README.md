# DEPRECATED

![no-maintenance-intended](https://img.shields.io/maintenance/no/2017?style=plastic)

# Garbanzo
Playing game with Spotippos.

> Deprecated, obsolete and archived.
> 
> This was part of the interview process at Maplink in 2017.
> 
> I keep the code here for historical purposes only.
> 

Requirements
---------------------
* Internet ;-)
* Linux or MacOS box;
* python;
* python-pip;

Setup
---------------------
The setup can be made at a docker, vagrant image, an Ansible playbook, inside a Python virtualenv or even at your machine. For the sake of simplicity, I'll let "where" up to you - and keep an eye on the requirements section :-). Once you decided, just do the following:
```
$ git clone 'https://github.com/arglbr/garbanzo.git'
$ cd garbanzo
$ bin/garbanzo --install
```
If no errors occurs:
```
$ bin/garbanzo --start 
```
or, if you want to debug it:
```
$ bin/garbanzo --start --debug
```
Your API root will be:
```
http://<host>:9832/garbanzo-api/
```
Here follows some example requests:
* http://{host}:9832/garbanzo-api/provinces
* http://{host}:9832/garbanzo-api/properties
* http://{host}:9832/garbanzo-api/properties/2
* http://{host}:9832/garbanzo-api/properties?ax=630&ay=680&bx=685&by=675

If you want to run the tests:
```
$ bin/garbanzo --run-tests
```

Why 'Garbanzo'? What name is this??
---------------------
Blame Github.

