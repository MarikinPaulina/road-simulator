from setuptools import setup

setup(
    name='Inzynierka',
    packages=['urban_street_simulation'],
    author='paulina',
    install_requires=[
        'networkx',
        'shapely',
        'numpy',
        'tqdm',
        'matplotlib',
        'scipy',
        'numba'
        ]
)
