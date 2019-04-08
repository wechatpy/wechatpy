      ___       __   _______   ________  ___  ___  ________  _________  ________  ___    ___
     |\  \     |\  \|\  ___ \ |\   ____\|\  \|\  \|\   __  \|\___   ___\\   __  \|\  \  /  /|
     \ \  \    \ \  \ \   __/|\ \  \___|\ \  \\\  \ \  \|\  \|___ \  \_\ \  \|\  \ \  \/  / /
      \ \  \  __\ \  \ \  \_|/_\ \  \    \ \   __  \ \   __  \   \ \  \ \ \   ____\ \    / /
       \ \  \|\__\_\  \ \  \_|\ \ \  \____\ \  \ \  \ \  \ \  \   \ \  \ \ \  \___|\/  /  /
        \ \____________\ \_______\ \_______\ \__\ \__\ \__\ \__\   \ \__\ \ \__\ __/  / /
         \|____________|\|_______|\|_______|\|__|\|__|\|__|\|__|    \|__|  \|__||\___/ /
                                                                                \|___|/

[![Build Status](https://travis-ci.org/jxtech/wechatpy.svg?branch=master)](https://travis-ci.org/jxtech/wechatpy)
[![Build status](https://ci.appveyor.com/api/projects/status/sluy95tvbe090af1/branch/master?svg=true)](https://ci.appveyor.com/project/messense/wechatpy-den93/branch/master)
[![codecov.io](https://codecov.io/github/jxtech/wechatpy/coverage.svg?branch=master)](https://codecov.io/github/jxtech/wechatpy?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/jxtech/wechatpy/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/jxtech/wechatpy/?branch=master)
[![PyPI](https://img.shields.io/pypi/v/wechatpy.svg)](https://pypi.org/project/wechatpy)
[![Downloads](https://pepy.tech/badge/wechatpy)](https://pepy.tech/project/wechatpy)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjxtech%2Fwechatpy.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjxtech%2Fwechatpy?ref=badge_shield)
[![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com)

微信(WeChat) 公众平台第三方 Python SDK。

[【阅读文档】](https://wechatpy.readthedocs.org/zh_CN/master/) [【快速入门】](https://wechatpy.readthedocs.org/zh_CN/master/quickstart.html)

[![Join the chat at https://gitter.im/messense/wechatpy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/messense/wechatpy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## 功能特性

1. 普通公众平台被动响应和主动调用 API
2. 企业微信 API
3. 微信支付 API

## 安装

推荐使用 pip 进行安装:

```bash
pip install wechatpy
# with cryptography (推荐）
pip install wechatpy[cryptography]
# with pycryptodome
pip install wechatpy[pycrypto]
```

升级版本：

    pip install -U wechatpy


## 使用示例

使用示例参见 [examples](examples/)

## 贡献代码

请阅读 [贡献代码指南](.github/CONTRIBUTING.md)

## 问题反馈

我们主要使用 [GitHub issues](https://github.com/jxtech/wechatpy/issues) 进行问题追踪和反馈。

QQ 群：176596300

![wechatpy QQ 群](https://raw.githubusercontent.com/jxtech/wechatpy/master/docs/_static/images/qq-group.png)


## License

This work is released under the MIT license. A copy of the license is provided in the [LICENSE](./LICENSE) file.

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjxtech%2Fwechatpy.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjxtech%2Fwechatpy?ref=badge_large)
