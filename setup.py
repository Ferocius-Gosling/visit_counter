from setuptools import setup, find_packages


setup(name='visit_counter',
      version='1.0',
      url='https://github.com/Ferocius-Gosling/visit_counter',
      description='Game renjuu where you should put 5 stones in line',
      packages=find_packages(),
      test_suite='tests',
      install_requires=['pygame==1.9.6', 'pytest'],
      entry_points={
          'console_scripts': ['visit_counter=visit_counter.__main__']
      }
      )
