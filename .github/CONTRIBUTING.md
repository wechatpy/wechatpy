贡献代码指南
===============

wechatpy 项目欢迎任何人提交 issue 和 Pull Requests 贡献代码，在您创建 Pull Requests 之前，请注意一下事项。

## 开发环境搭建

使用 [poetry](https://python-poetry.org/) 创建和管理项目的 Python 开发环境。

安装 poetry:
```bash
cd wechatpy
pip install -U poetry
```

安装项目环境
```bash
poetry install
```

> Tips: 使用项目Python环境中的命令需要通过 `poetry run` 调用，否则调用的是系统环境中的命令。比如 `poetry run black` 使用的是项目环境中安装的`black`，直接执行 `black` 使用的是系统环境的`black`。

## lint

wechatpy 遵循 [PEP8](https://www.python.org/dev/peps/pep-0008/) 代码风格规范，您贡献的代码应当尽可能遵循 PEP8。
同时，您可以安装 `flake8` 并开启其 git hook 功能自动在每次 commit 之前 lint 代码。

```bash
pip install -U flake8
flake8 --install-hook git
```

推荐设置环境变量 `FLAKE8_STRICT` 为 True：

```bash
export FLAKE8_STRICT=True
```

## 静态类型检查

wechatpy 使用 [mypy](https://github.com/python/mypy/) 进行静态类型检查以提前发现错误。CI 会自动触发这一检查，请在提交 PR 前手动进行检查并修复错误。

```bash
poetry run pip install mypy
poetry run mypy --show-column-numbers --hide-error-context wechatpy
```

## 代码格式化

wechatpy 使用 [black](https://github.com/psf/black/) 自动格式化 Python 代码并在 CI 上进行代码格式检查，请在提交 PR 前进行代码格式化：

```bash
poetry run pip install black
poetry run black -l 120 -t py36 -t py37 -t py38 .
```

## 自动化测试

在您完成对代码的改进和完善之后，请进行自动化测试，确保全部测试通过。

```bash
poetry run pytest
```

wechatpy 希望支持的 Python 版本有 3.5, 3.6, 3.7 和 3.8。
如果您的本地 Python 环境没有安装全面，请尽可能测试全面您已经安装的 Python 版本。

如果出现测试失败，请检查您的修改过的代码或者检查测试用例的代码是否需要更新。

> Tips: 您可以使用 `poetry run pytest -s --pdb` 在测试失败的时候自动进入 pdb 进行调试。

## Pull Requests

在您完成上述所有步骤后，您可以在 [wechatpy](https://github.com/wechatpy/wechatpy) 项目上提交您的 Pull Requests.

在您提交 Pull Requests 之后，[GitHub Actions](https://github.com/wechatpy/wechatpy/actions?query=workflow%3ACI) 会进行全面的自动化测试（测试所有支持的 Python 环境）。
测试成功后 [Codecov](https://codecov.io/github/wechatpy/wechatpy?branch=master) 会给出 coverage 报告，

如果出现测试失败的情况，请您在 [GitHub Actions](https://github.com/wechatpy/wechatpy/actions?query=workflow%3ACI) 的构建日志中查找原因，修复后提交代码。

> Tips: 如果您的修改不是针对代码的，不需要进行自动化测试，可以在 Git commit message 结尾加上 `[ci skip]`.

在所有环节完成之后，wechatpy 项目成员会尽快 review 您的 Pull Requests，予以合并或和您进行进一步的讨论。

Thanks.

## 发布新版本

在发布新版本前需要更新 [changelog 文档](../docs/changelog.rst)，版本号规则参见[Semantic Versioning](https://semver.org/)。

使用 [`bumpversion`](https://github.com/peritus/bumpversion)自动更新和维护项目版本号，配置文件见根目录 `.bumpversion.cfg` 文件。

对于主要版本：

1. 对于 bugfix 版本：`bumpversion patch`
2. 对于小 feature 版本：`bumpversion minor`
3. 大的 breaking change 版本：`bumpversion major`

大部分情况下使用 `bumpversion patch` 即可。

`patch`、`minor` 和 `major` 都会将版本号进入开发状态，既 `<major>.<minor>.<patch>.<release><build>`，此时：
* 如果有问题需要修改，合并代码后，应该使用 `bumpversion build` 更新版本号到 `<major>.<minor>.<patch>.alpha.<build + 1>`
* 如果未发现明显问题，使用 `bumpversion release` 更新版本号到 `<major>.<minor>.<patch>`

配置文件简单设置，目前发布状态（release）只有 `alpha` 和 `stable` 两个。

完成后将 master 分支代码改动和 `bumpversion` 自动产生的 tag 一起 push 到 GitHub 仓库中, 如:

```bash
git push origin master --tags
```

tag 分支在 CI 测试通过后将会被自动发布到 [PyPi](https://pypi.python.org/pypi/wechatpy) 上。
