#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import parse
import pyperclip

'''
华南农业大学 WebVPN 远程接入系统链接生成与还原工具
Author:     interestingcn01@gmail.com  
Version:    22.8.1
'''

# 定义webVpn服务器地址信息
webVpnGateWayUrl = 'vpn.scau.edu.cn:8118'
webVpnScheme = 'http'


def welcome():
    text = '''
   _____ _________   __  __  _       __     __  _    ______  _   __   
  / ___// ____/   | / / / / | |     / /__  / /_| |  / / __ \/ | / /   
  \__ \/ /   / /| |/ / / /  | | /| / / _ \/ __ \ | / / /_/ /  |/ /    
 ___/ / /___/ ___ / /_/ /   | |/ |/ /  __/ /_/ / |/ / ____/ /|  /     
/____/\____/_/  |_\____/____|__/|__/\___/_.___/|___/_/   /_/ |_/      
                      /_____/                                                                                                                                 
                                                                                                     
    华南农业大学 WebVPN 远程接入系统链接生成与还原工具
    Author:interestingcn01@gmail.com  Ver:22.8.1
    Github: https://github.com/interestingcn/SCAU_WebVPNTools
    '''
    print(text)

# [ Direct ==> WebVPN ]
def url_to_webVpn(url):
    # 去除结尾多余的 ’/‘
    if str(url).endswith('/'):
        url = url[:-1]
    url = parse.urlparse(url)
    if url.scheme == 'https':
        scheme_sign = '-s'
    else:
        scheme_sign = ''
    if url.port != 80 and url.port != None:
        port_sign = f'-{url.port}-p'
    else:
        port_sign = ''
    hostname = url.hostname.replace('.','-')
    if url.query != '':
        generateWebVpnUrl = f'{webVpnScheme}://{hostname}{port_sign}{scheme_sign}.{webVpnGateWayUrl}{url.path}?{url.query}'
    else:
        generateWebVpnUrl = f'{webVpnScheme}://{hostname}{port_sign}{scheme_sign}.{webVpnGateWayUrl}{url.path}'

    return generateWebVpnUrl

# [ WebVPN ==> Direct ]
def webVpn_to_url(url):
    # 去除结尾多余的 ’/‘
    if str(url).endswith('/'):
        url = url[:-1]
    url = parse.urlparse(url)

    hostname = url.netloc.replace('.'+webVpnGateWayUrl,'')
    hostname = hostname.split('-')
    if 's' in hostname:
        scheme = 'https'
        del hostname[hostname.index('s')]
    else:
        scheme = 'http'
    if 'p' in hostname:
        port = ':' + hostname[hostname.index('p') - 1]
        # 因依赖参数'p'进行定位，此处销毁元素需注意先后顺序
        del hostname[hostname.index('p') - 1]
        del hostname[hostname.index('p')]
    else:
        port = ''
    hostname = '.'.join(hostname)
    if url.query != '':
        return f'{scheme}://{hostname}{port}{url.path}?{url.query}'
    else:
        return f'{scheme}://{hostname}{port}{url.path}'

def isUrl(url):
    url = parse.urlparse(url)
    if url.netloc == '':
        return False
    else:
        return True

def isWebVpnUrl(url):
    url = parse.urlparse(url)
    return str(url.netloc).endswith(webVpnGateWayUrl)


if __name__ == '__main__':
    welcome()
    print('[ Tips: 请直接从浏览器中复制所需URL粘贴至此(包括http/https),结果将自动保存在剪切板中. ]')
    while True:
        print('')
        input_url = input('输入链接: ')

        # 快速结束
        if input_url == ' ':
            exit()

        # 从剪切板获取链接，需添加输入暂停代码
        # input_url = pyperclip.paste()

        if isUrl(input_url) == False:
            print('当前地址有误，请重新输入')
            continue

        if isWebVpnUrl(input_url):
            url_res =  webVpn_to_url(input_url)
            print('[ WebVPN ==> Direct ]: ' + url_res)
            pyperclip.copy(url_res)
            continue
        else:
            url_res = url_to_webVpn(input_url)
            print('[ Direct ==> WebVPN ]: ' + url_res)
            pyperclip.copy(url_res)
            continue
    exit()






