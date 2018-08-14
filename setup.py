import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

standard_exclude_directories = [
    ".*", "./django_ldap_user_registration/*", "./build",
    "./dist", "EGG-INFO", "*.egg-info",
]
# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ldap-user-registration',
    version='1.0',
    packages=find_packages(exclude=standard_exclude_directories),
    include_package_data=True,
    license='GPL v3',  # example license
    description='A Django web front-end that provides user registration and password reset to an LDAP server.',
    long_description=README,
    url='https://github.com/KENET-KE/django-ldap-user-registration/',
    author='Ronald Osure',
    author_email='sureronald@gmail.com',
    keywords ='django ldap registration password reset idp federation catch-all',
    install_requires=[
        'Django >= 2.0',
        'python-ldap>=3.1.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
