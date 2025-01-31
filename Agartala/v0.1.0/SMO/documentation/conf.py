from docs_conf.conf import *
linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*',
    'https://sdnc-web:8453'
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "logo.png"
html_theme_options = {
    'logo_only': True,
    'display_version': False,
}

project = "IOSMCN OAM"
