from socket import socket
from socket_srever import tcpServer
from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def obit():
    if tcpServer() == 1:
        return redirect('http://www.baidu.com')
    else:
        return redirect('https://cn.bing.com/')


if __name__ == '__main__':
    app.run()
