安装与升级
==========

目前 wechatpy 支持的 Python 环境有 2.7, 3.5, 3.6, 3.7 和 pypy。

为了简化安装过程，推荐使用 pip 进行安装

.. code-block:: bash

    pip install wechatpy
    # with cryptography （推荐）
    pip install wechatpy[cryptography]
    # with pycryptodome
    pip install wechatpy[pycrypto]

升级 wechatpy 到新版本::

    pip install -U wechatpy

如果需要安装 GitHub 上的最新代码::

    pip install https://github.com/jxtech/wechatpy/archive/master.zip
