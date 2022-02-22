# Tesla Vortex
This panel app is able to generate an images of a "Vortex" as described 
in the "Mathologer" YouTube [video](https://youtu.be/6ZrO90AI0c8)

## Installation

To run the app locally you need python-3.8.

It is suggested to create a virtual environment. 

Open a shell, navigate in the code directory, and enter the command: 

```shell
python -m virtualenv venv_vortex
```

This will create a local directory that containing the python environment 
and all the packages that you will need to install. 

To do that you first need to enter the newly created environment:

```shell
source ./venv_vortex/bin/activate
```

and then install the required packages:

```shell
pip install -r ./requirements.txt
```

## Run the app Locally
The app can be executed locally with the command:

```shell
panel serve app.py
```
The app will now be available on a normal internet browse at the address: http://localhost:5006/app?theme=dark

If you want to make the app accessible from other computer in your network 
use the following options: 

```shell
panel serve app.py --address 0.0.0.0  --allow-websocket-origin="*"
```

## How to get a vortex image
Uncomment line 98 of the ```app.py``` file by changing:
```python
        # dwg.save()
```

into

```python
        dwg.save()
```

NOTE: In Python the indentation of code is an integral part of the syntax, 
so make sure to maintain it.

WARNING: This modification will make the app much slower for higher numbers of
nodes, since it will write the file at each update!

## On-line version
The app is also available [on-line](https://mathologer-modular-time-table.lm.r.appspot.com/app?theme=dark)