贡献代码指南
===============

wechatpy 项目欢迎任何人提交 issue 和 Pull Requests 贡献代码，在您创建 Pull Requests 之前，请注意一下事项。

## 开发环境搭建

使用 `virtualenv` 创建和系统库隔离的 Python 开发环境，并安装所有依赖:

```bash
cd wechatpy
virtualenv .
source bin/activate
python setup.py develop
```

为了方便测试，需要安装 tox:

```bash
pip install -U tox
```

> Tips: 安装 [autoenv](https://github.com/kennethreitz/autoenv) 可以让您在进入 wechatpy 文件夹时自动激活虚拟环境，省去每次手动执行 `source bin/activate`

## lint

wechatpy 遵循 [PEP8](http://legacy.python.org/dev/peps/pep-0008/) 代码风格规范，您贡献的代码应当尽可能遵循 PEP8。
同时，您可以安装 `flake8` 并开启其 git hook 功能自动在每次 commit 之前 lint 代码。

```bash
pip install -U flake8
flake8 --install-hook git
```

推荐设置环境变量 `FLAKE8_STRICT` 为 True：

```bash
export FLAKE8_STRICT=True
```

## 自动化测试

在您完成对代码的改进和完善之后，请使用 tox 完成自动化测试，确保全部测试通过。

```bash
tox -l | xargs tox -e
```

wechatpy 希望支持的 Python 版本有 2.6, 2.7, 3.3, 3.4, 3.5, 3.6, pypy 和 pypy3.
如果您的本地 Python 环境没有安装全面，请尽可能测试全面您已经安装的 Python 版本。
如您本地安装了 Python 2.7 和 Python 3.6，则运行：

```bash
tox -e py27-pycrypto,py36-cryptography
```

或者您也可以直接用 `py.test` 测试：

```bash
pip install -U -r dev-requirements.txt
py.test -v
```

如果出现测试失败，请检查您的修改过的代码或者检查测试用例的代码是否需要更新。

> Tips: 您可以使用 `pytest -s --pdb` 在测试失败的时候自动进入 pdb 进行调试。

## Pull Requests

在您完成上述所有步骤后，您可以在 [wechatpy](https://github.com/jxtech/wechatpy) 项目上提交您的 Pull Requests.

在您提交 Pull Requests 之后，[Travis CI](https://travis-ci.org/jxtech/wechatpy) 会进行全面的自动化测试（测试所有支持的 Python 环境）。
测试成功后 [Coveralls](https://coveralls.io/r/jxtech/wechatpy?branch=master) 会给出 coverage 报告，
[Scrutinizer CI](https://scrutinizer-ci.com/g/jxtech/wechatpy/?branch=master) 会给出代码质量分析报告。

如果出现测试失败的情况，请您在 [Travis CI](https://travis-ci.org/jxtech/wechatpy) 的构建日志中查找原因，修复后提交代码。

> Tips: 如果您的修改不是针对代码的，不需要进行自动化测试，可以在 Git commit message 结尾加上 `[ci skip]`.

在所有环节完成之后，wechatpy 项目成员会尽快 review 您的 Pull Requests，予以合并或和您进行进一步的讨论。

Thanks.

## 发布新版本

在发布新版本前需要更新 [changelog 文档](../docs/changelog.rst)，使用 [`bumpversion`](https://github.com/peritus/bumpversion)
工具更新代码中的版本号信息：

1. 对于 bugfix 版本：`bumpversion patch`
2. 对于小 feature 版本：`bumpversion minor`
3. 大的 breaking change 版本：`bumpversion major`

大部分情况下使用 `bumpversion patch` 即可。完成后将 master 分支代码改动和 `bumpversion` 自动产生的 tag 一起 push 到 GitHub 仓库中, 如:

```bash
git push origin master --tags
```

tag 分支在 CI 测试通过后将会被自动发布到 [PyPi](https://pypi.python.org/pypi/wechatpy) 上。
