from setuptools import setup, find_packages
import sys, os

version = '1.2.1'

setup(name='Products.RedirectionTool',
      version=version,
      description="The Redirection Tool allows the management of the aliases stored in plone.app.redirector",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
      ],
      keywords='Redirection Alias Zope Plone',
      author='Plone Solutions AS',
      author_email='',
      url='http://plone.org/products/redirectiontool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/redirectiontool/releases',
      install_requires=[
        'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)
