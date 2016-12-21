from setuptools import setup
import unittest
with open('README.rst', 'r') as f:
    readme = f.read()
def testsuite():
	test_loader = unittest.TestLoader()
	test_suite = test_loader.discover('tests', pattern='test*.py')
	return test_suite
setup(name='daemonmgr',
      version='0.0.9',
      long_description=readme,
      description='Create daemons from commands',
      author='Gerard Duval',
      author_email='gerard.duval@gdsoftconsulting.com',
      url='https://github.com/gduvalsc/daemonmgr',
      scripts=['scripts/daemonmgr'],
      license='BSD',
      packages=['daemonmgr'],
      classifiers=[ "Development Status :: 3 - Alpha", "Topic :: Utilities", "License :: OSI Approved :: BSD License"],
      test_suite="setup.testsuite",
      zip_safe=False)
