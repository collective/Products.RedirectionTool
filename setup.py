from setuptools import setup, find_packages

version = '1.4.1'

setup(name='Products.RedirectionTool',
      version=version,
      description="The Redirection Tool allows the management of the aliases "
                  "stored in plone.app.redirector",
      long_description=open('README.rst').read() + '\n' + open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.0',
          # 'Framework :: Plone :: 5.1',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='Redirection Alias Zope Plone',
      author='Jarn AS',
      author_email='info@jarn.com',
      url='https://github.com/collective/Products.RedirectionTool',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'AccessControl',
          'plone.app.redirector',
          'plone.memoize',
          'Products.CMFCore',
          'Products.CMFPlone',
          'Products.GenericSetup',
          'Products.statusmessages',
          'setuptools',
          'z3c.form',
          'zope.component',
          'zope.deprecation',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'Products.CMFFormController',
              'Products.PloneTestCase',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """)
