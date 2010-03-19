from setuptools import setup, find_packages
import sys, os

version = '0.1r2'

setup(name='PyMoneris',
      version=version,
      description="A Python interface to Moneris APIs.",
      long_description="""\
Currently supports their eselectplus product.

Closely resembles the official Perl interface and may not seem intuitive as such to Python developers.

Future work will be made to make it more Pythonic and support other Moneris products.
""",
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Other/Nonlisted Topic"],
      keywords='ecommerce, moneris, eselectplus',
      author='J Kenneth King',
      author_email='james@agentultra.com',
      url='http://code.google.com/p/pymoneris/',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
