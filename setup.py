# sherpa-py-ldap is available under the MIT License. https://github.com/Identicum/sherpa-py-ldap/
# Copyright (c) 2026, Identicum - https://identicum.com/
#
# Authors:
# Gustavo J Gallardo - ggallard@identicum.com
#

from setuptools import setup

setup(
    name='sherpa-py-ldap',
    version='1.1.1',
    description='Python LDAP utilities',
    url='git@github.com:Identicum/sherpa-py-ldap.git',
    author='Identicum',
    author_email='ggallard@identicum.com',
    license='MIT License',
    install_requires=['python-ldap'],
    packages=['sherpa', 'sherpa.ldap'],
    zip_safe=False,
    python_requires='>=3.0'
)
