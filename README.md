# mchat
A simple LAN chat tool



## server

### windows

```cmd
cd /server/example/mqtt-server
make
./example.exe
```



### ubuntu

```shell
sudo apt install emqx
emqx start
```

or

```shell
cd /server/example/mqtt-server
make
./example
```



## client

run 

```shell
conda create mchat python=3.8
conda activate mchat
pip install pyside6
pip install paho-mqtt
python main.py
```



build

```shell
python setup.py build
```



