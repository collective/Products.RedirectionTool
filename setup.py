from setuptools import setup, find_packages

version = '1.3.1'

setup(name='Products.RedirectionTool',
      version=version,
      description="The Redirection Tool allows the management of the aliases "
                  "stored in plone.app.redirector",
      long_description = open('README.txt').read() + '\n' +
                         open('CHANGES.txt').read(),
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
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
