      ___       __   _______   ________  ___  ___  ________  _________  ________  ___    ___ 
     |\  \     |\  \|\  ___ \ |\   ____\|\  \|\  \|\   __  \|\___   ___\\   __  \|\  \  /  /|
     \ \  \    \ \  \ \   __/|\ \  \___|\ \  \\\  \ \  \|\  \|___ \  \_\ \  \|\  \ \  \/  / /
      \ \  \  __\ \  \ \  \_|/_\ \  \    \ \   __  \ \   __  \   \ \  \ \ \   ____\ \    / / 
       \ \  \|\__\_\  \ \  \_|\ \ \  \____\ \  \ \  \ \  \ \  \   \ \  \ \ \  \___|\/  /  /  
        \ \____________\ \_______\ \_______\ \__\ \__\ \__\ \__\   \ \__\ \ \__\ __/  / /    
         \|____________|\|_______|\|_______|\|__|\|__|\|__|\|__|    \|__|  \|__||\___/ /     
                                                                                \|___|/      

[![Latest Version](https://pypip.in/version/wechatpy/badge.svg)](https://pypi.python.org/pypi/wechatpy/)
[![Build Status](https://travis-ci.org/messense/wechatpy.svg?branch=master)](https://travis-ci.org/messense/wechatpy)
[![Coverage Status](https://coveralls.io/repos/messense/wechatpy/badge.png?branch=master)](https://coveralls.io/r/messense/wechatpy?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/messense/wechatpy/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/messense/wechatpy/?branch=master)
[![Supported Python versions](https://pypip.in/py_versions/wechatpy/badge.svg)](https://pypi.python.org/pypi/wechatpy/)
[![Supported Python implementations](https://pypip.in/implementation/wechatpy/badge.svg)](https://pypi.python.org/pypi/wechatpy/)

微信(WeChat) 公众平台第三方 Python SDK，实现了普通公众平台和企业号公众平台的解析消息、生成回复和主动调用等 API。

阅读文档：[http://wechatpy.readthedocs.org/en/latest/](http://wechatpy.readthedocs.org/en/latest/)

## 安装

推荐使用 pip 进行安装:

    pip install wechatpy

升级版本：

    pip install -U wechatpy

从 0.8.0 版本开始，wechatpy 消息加解密同时兼容 [cryptography](https://github.com/pyca/cryptography) 和 [PyCrypto](https://github.com/dlitz/pycrypto), 
优先使用 cryptography 库。因而不再强制依赖 PyCrypto 库。如需使用消息加解密（企业号平台必须），请自行安装 cryptography 或者 PyCrypto 库：

```bash
# 安装 cryptography
pip install cryptography>=0.8.2
# 或者安装 PyCrypto
pip install pycrypto>=2.6.1
```

> Tips: Windows 用户请先安装 PyCrypto 的二进制包后再使用 pip 安装 wechatpy 。 PyCrypto Windows 的二进制包可以在[这里](http://www.voidspace.org.uk/python/pycrypto-2.6.1/)下载。

## 使用示例

使用示例参见 [examples](examples/)

## 贡献代码

请阅读 [贡献代码指南](CONTRIBUTING.md)

## 捐赠

如果您觉得 ``wechatpy`` 对您有帮助，欢迎请作者一杯咖啡。
![捐赠 wechatpy](assets/alipay.png)

##License

The MIT License (MIT)

Copyright (c) 2014 messense

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
