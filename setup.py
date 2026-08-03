# THIS FILE IS EXCLUSIVELY MAINTAINED by the project aedev.project_tpls v0.3.94
""" setup of ae namespace package portion kivy: core application classes and widgets for GUIApp-conform Kivy apps. """
import pathlib
import sys
from typing import Any
import setuptools


print("SetUp " + __name__ + ": " + sys.executable + str(sys.argv) + f" {sys.path=}")

setup_kwargs: dict[str, Any] = {
    'author': 'AndiEcker',
    'author_email': 'aecker2@gmail.com',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    'description': 'ae namespace package portion kivy: core application classes and widgets for GUIApp-conform Kivy apps',
    'extras_require': {
        'dev': [
            'aedev_project_tpls',
            'ae_ae',
            'anybadge',
            'flake8',
            'mypy',
            'pylint',
            'pytest',
            'pytest-cov',
            'typing',
            'types-setuptools',
        ],
        'docs': [],
        'tests': [
            'anybadge',
            'flake8',
            'mypy',
            'pylint',
            'pytest',
            'pytest-cov',
            'typing',
            'types-setuptools',
        ],
    },
    'install_requires': [
        'kivy==2.3.0',
        'plyer',
        'ae_base',
        'ae_system',
        'ae_files',
        'ae_paths',
        'ae_dynamicod',
        'ae_i18n',
        'ae_core',
        'ae_gui',
        'ae_kivy_glsl',
        'ae_kivy_auto_width',
        'ae_kivy_dyn_chi',
        'ae_kivy_relief_canvas',
    ],
    'keywords': [
        'configuration',
        'development',
        'environment',
        'productivity',
    ],
    'license': 'GPL-3.0-or-later',
    'long_description': (pathlib.Path(__file__).parent / 'README.md').read_text(encoding='utf-8'),
    'long_description_content_type': 'text/markdown',
    'name': 'ae_kivy',
    'package_data': {
        '': [
            'widgets.kv',
        ],
    },
    'packages': [
        'ae.kivy',
    ],
    'project_urls': {
        'Bug Tracker': 'https://gitlab.com/ae-group/ae_kivy/-/issues',
        'Documentation': 'https://ae.readthedocs.io/en/latest/_autosummary/ae.kivy.html',
        'Repository': 'https://gitlab.com/ae-group/ae_kivy',
        'Source': 'https://ae.readthedocs.io/en/latest/_modules/ae/kivy.html',
    },
    'python_requires': '>=3.12',
    'url': 'https://gitlab.com/ae-group/ae_kivy',
    'version': '0.3.131',
    'zip_safe': False,
}

if __name__ == "__main__":
    setuptools.setup(**setup_kwargs)
    ...
