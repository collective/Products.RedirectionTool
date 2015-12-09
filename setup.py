from setuptools import setup, find_packages

version = '1.4.0'

setup(name='Products.RedirectionTool',
      version=version,
      description="The Redirection Tool allows the management of the aliases "
                  "stored in plone.app.redirector",
      long_description=open('README.rst').read() + '\n' + open('CHANGES.rst').read(),
      classifiers=[
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
      ],
      keywords='Redirection Alias Zope Plone',
      author='Jarn AS',
      author_email='info@jarn.com',
      url='http://pypi.python.org/pypi/Products.RedirectionTool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.form'
      ],
      extras_require={
          'test': [
              'Products.PloneTestCase',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """)
