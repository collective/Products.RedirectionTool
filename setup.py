import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.3dev'

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    #+ '\n' +
    #read('Products', 'RedirectionTool', 'README.txt')
    #+ '\n' +
    #read('CONTRIBUTORS.txt')
    )

setup(name='Products.RedirectionTool',
      version=version,
      description="The Redirection Tool allows the management of the aliases stored in plone.app.redirector",
      long_description=long_description,
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

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
