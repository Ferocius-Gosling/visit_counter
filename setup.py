from setuptools import setup, find_packages


setup(name='visit_counter',
      version='1.0',
      url='https://github.com/Ferocius-Gosling/visit_counter',
      description='Visit counter that counted visits on your site',
      packages=find_packages(),
      test_suite='tests',
      install_requires=['pymysql==0.9.3', 'Flask==1.1.1', 'pytest'],
      entry_points={
          'console_scripts': ['visit_counter=visit_counter.__main__']
      }
      )
