# ProxySwitch
> mitmproxy for certain hosts

This tool redirects traffic (http/https) through 
certain instances of mitmproxy allowing you to 
apply certain man in the middle operations specified for 
the host.

## Installation

```console
# Clone the project directory
foo@bar:~$ git clone https://github.com/ethylomat/ProxySwitch.git
foo@bar:~$ cd ProxySwitch
# Create virtual environment 
foo@bar:~$ python3 -m venv venv
# Activate virtual environment 
foo@bar:~$ . venv/bin/activate

# Install python package dependencies
foo@bar:~$ pip install -r requirements.txt
```

## Usage

Add your addon instances to the `addons` list in the `main.py` file and start the 
tool with:

```console
foo@bar:~$ python3 main.py
Starting proxy process on port 8081 with addon: Swap
Starting httpd process on port 8000
127.0.0.1 - - [22/Nov/2018 23:26:19] "GET /proxy.pac HTTP/1.1" 200 -
```

The example addon swap is swapping the words „Fire“ and „Water“ on 
Wikipedia pages with host `*.wikipedia.org`.

<img src="https://static.ethylomat.de/ProxySwitch/ProxySwitch2.png" align="left" width="250px" >

## PAC Server

The default URL for the PAC (Proxy-Auto-Config) file is:
`http://127.0.0.1:8000/proxy.pac`

Add the URL to your proxy settings (automatic proxy configuration):
![https://static.ethylomat.de/ProxySwitch/ProxySwitch1.png](https://static.ethylomat.de/ProxySwitch/ProxySwitch1.png)