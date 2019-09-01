#!/usr/bin/python3.6
# -*- coding=utf-8 -*-

from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(
    ('144.202.93.164', 22),#Step 2连接远端服务器SSH端口
    ssh_username="root",
    ssh_password="starBB002347",
    local_bind_address=('192.168.1.101',2323),  #Step 1连接本地地址'10.1.5.205',2323
    remote_bind_address=('127.0.0.1', 12345))  #Step 3跳转到本地服务器'127.0.0.1', 22)

server.start()
