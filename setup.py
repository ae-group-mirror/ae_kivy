# THIS FILE IS EXCLUSIVELY MAINTAINED by the project aedev.project_tpls v0.3.79
""" setup of ae namespace package portion kivy: core application classes and widgets for GUIApp-conform Kivy apps. """
import sys
# noinspection PyUnresolvedReferences
import pathlib
# noinspection PyUnresolvedReferences
import setuptools


print("SetUp " + __name__ + ": " + sys.executable + str(sys.argv) + f" {sys.path=}")

setup_kwargs = {
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
        'Kivy==2.3.0',
        'plyer==2.1.0',
        'ae_base==0.3.85',
        'ae_system==0.3.3',
        'ae_files==0.3.27',
        'ae_paths==0.3.44',
        'ae_i18n==0.3.35',
        'ae_core==0.3.86',
        'ae_gui==0.3.117',
        'ae-kivy-glsl==0.3.16',
        'ae_kivy_auto_width==0.3.26',
        'ae_kivy_dyn_chi==0.3.12',
        'ae_kivy_relief_canvas==0.3.14',
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
    'version': '0.3.127',
    'zip_safe': False,
}

if __name__ == "__main__":
    setuptools.setup(**setup_kwargs)
    pass
