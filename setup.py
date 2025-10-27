# THIS FILE IS EXCLUSIVELY MAINTAINED by the project aedev.project_tpls v0.3.59
""" setup of ae namespace package portion kivy: core application classes and widgets for GUIApp-conform Kivy apps. """
# noinspection PyUnresolvedReferences
import sys
print(f"SetUp {__name__=} {sys.executable=} {sys.argv=} {sys.path=}")

# noinspection PyUnresolvedReferences
import setuptools

setup_kwargs = {
    'author': 'AndiEcker',
    'author_email': 'aecker2@gmail.com',
    'classifiers': [       'Development Status :: 3 - Alpha', 'Natural Language :: English', 'Operating System :: OS Independent',
        'Programming Language :: Python', 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9', 'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed'],
    'description': 'ae namespace package portion kivy: core application classes and widgets for GUIApp-conform Kivy apps',
    'extras_require': {       'dev': [       'aedev_project_tpls', 'ae_ae', 'anybadge', 'coverage-badge', 'aedev_project_manager', 'flake8',
                       'mypy', 'pylint', 'pytest', 'pytest-cov', 'pytest-django', 'typing', 'types-setuptools'],
        'docs': [],
        'tests': [       'anybadge', 'coverage-badge', 'aedev_project_manager', 'flake8', 'mypy', 'pylint', 'pytest',
                         'pytest-cov', 'pytest-django', 'typing', 'types-setuptools']},
    'install_requires': [       'kivy', 'plyer', 'ae_base', 'ae_files', 'ae_paths', 'ae_i18n', 'ae_core', 'ae_gui', 'ae_kivy_glsl',
        'ae_kivy_auto_width', 'ae_kivy_dyn_chi', 'ae_kivy_relief_canvas'],
    'keywords': ['configuration', 'development', 'environment', 'productivity'],
    'license': 'GPL-3.0-or-later',
    'long_description': ('<!-- THIS FILE IS EXCLUSIVELY MAINTAINED by the project ae.ae v0.3.101 -->\n'
 '<!-- THIS FILE IS EXCLUSIVELY MAINTAINED by the project aedev.namespace_root_tpls v0.3.22 -->\n'
 '# kivy 0.3.125\n'
 '\n'
 '[![GitLab develop](https://img.shields.io/gitlab/pipeline/ae-group/ae_kivy/develop?logo=python)](\n'
 '    https://gitlab.com/ae-group/ae_kivy)\n'
 '[![LatestPyPIrelease](\n'
 '    https://img.shields.io/gitlab/pipeline/ae-group/ae_kivy/release0.3.125?logo=python)](\n'
 '    https://gitlab.com/ae-group/ae_kivy/-/tree/release0.3.125)\n'
 '[![PyPIVersions](https://img.shields.io/pypi/v/ae_kivy)](\n'
 '    https://pypi.org/project/ae-kivy/#history)\n'
 '\n'
 '>ae namespace package portion kivy: core application classes and widgets for GUIApp-conform Kivy apps.\n'
 '\n'
 '[![Coverage](https://ae-group.gitlab.io/ae_kivy/coverage.svg)](\n'
 '    https://ae-group.gitlab.io/ae_kivy/coverage/index.html)\n'
 '[![MyPyPrecision](https://ae-group.gitlab.io/ae_kivy/mypy.svg)](\n'
 '    https://ae-group.gitlab.io/ae_kivy/lineprecision.txt)\n'
 '[![PyLintScore](https://ae-group.gitlab.io/ae_kivy/pylint.svg)](\n'
 '    https://ae-group.gitlab.io/ae_kivy/pylint.log)\n'
 '\n'
 '[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_kivy)](\n'
 '    https://gitlab.com/ae-group/ae_kivy/)\n'
 '[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_kivy)](\n'
 '    https://gitlab.com/ae-group/ae_kivy/)\n'
 '[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_kivy)](\n'
 '    https://gitlab.com/ae-group/ae_kivy/)\n'
 '[![PyPIFormat](https://img.shields.io/pypi/format/ae_kivy)](\n'
 '    https://pypi.org/project/ae-kivy/)\n'
 '[![PyPILicense](https://img.shields.io/pypi/l/ae_kivy)](\n'
 '    https://gitlab.com/ae-group/ae_kivy/-/blob/develop/LICENSE.md)\n'
 '[![PyPIStatus](https://img.shields.io/pypi/status/ae_kivy)](\n'
 '    https://libraries.io/pypi/ae-kivy)\n'
 '[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_kivy)](\n'
 '    https://pypi.org/project/ae-kivy/#files)\n'
 '\n'
 '\n'
 '## installation\n'
 '\n'
 '\n'
 'execute the following command to install the\n'
 'ae.kivy package\n'
 'in the currently active virtual environment:\n'
 ' \n'
 '```shell script\n'
 'pip install ae-kivy\n'
 '```\n'
 '\n'
 'if you want to contribute to this portion then first fork\n'
 '[the ae_kivy repository at GitLab](\n'
 'https://gitlab.com/ae-group/ae_kivy "ae.kivy code repository").\n'
 'after that pull it to your machine and finally execute the\n'
 'following command in the root folder of this repository\n'
 '(ae_kivy):\n'
 '\n'
 '```shell script\n'
 'pip install -e .[dev]\n'
 '```\n'
 '\n'
 'the last command will install this package portion, along with the tools you need\n'
 'to develop and run tests or to extend the portion documentation. to contribute only to the unit tests or to the\n'
 'documentation of this portion, replace the setup extras key `dev` in the above command with `tests` or `docs`\n'
 'respectively.\n'
 '\n'
 'more detailed explanations on how to contribute to this project\n'
 '[are available here](\n'
 'https://gitlab.com/ae-group/ae_kivy/-/blob/develop/CONTRIBUTING.rst)\n'
 '\n'
 '\n'
 '## namespace portion documentation\n'
 '\n'
 'information on the features and usage of this portion are available at\n'
 '[ReadTheDocs](\n'
 'https://ae.readthedocs.io/en/latest/_autosummary/ae.kivy.html\n'
 '"ae_kivy documentation").\n'),
    'long_description_content_type': 'text/markdown',
    'name': 'ae_kivy',
    'package_data': {'': ['widgets.kv']},
    'packages': ['ae.kivy'],
    'project_urls': {       'Bug Tracker': 'https://gitlab.com/ae-group/ae_kivy/-/issues',
        'Documentation': 'https://ae.readthedocs.io/en/latest/_autosummary/ae.kivy.html',
        'Repository': 'https://gitlab.com/ae-group/ae_kivy',
        'Source': 'https://ae.readthedocs.io/en/latest/_modules/ae/kivy.html'},
    'python_requires': '>=3.9',
    'url': 'https://gitlab.com/ae-group/ae_kivy',
    'version': '0.3.125',
    'zip_safe': False,
}

if __name__ == "__main__":
    setuptools.setup(**setup_kwargs)
    pass
