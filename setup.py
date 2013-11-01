from setuptools import setup, find_packages


setup(name='devuart',
      version="0.1",
      author="Mike Spindel",
      author_email="mike@spindel.is",
      license="MIT",
      keywords="serial uart ioreg iokit",
      packages=find_packages(exclude=['ez_setup']),
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python"])
