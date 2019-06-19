import setuptools

setuptools.setup(
    name = 'linkBudget',
    version = '1.0dev',
    description = 'Link budget calculator for cascaded microwave systems',
    author = 'Adrian K. Sinclair',
    author_email = 'adrian.sinclair@asu.edu',
    url = 'https://github.com/adriankaisinclair/linkBudget',
    packages = setuptools.find_packages(),
    keywords = ['cryogenic', 'cascade', 'microwave'],
    install_requires=['numpy', 'matplotlib','SchemDraw'],
    classifiers = [
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    ],
)
