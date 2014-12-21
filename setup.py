from setuptools import setup

setup(
    name='beeminder_dow',
    version='0.1',
    description="schedule regular breaks in Beeminder goals",
    url='https://github.com/jshholland/beeminder-dow',
    author='Josh Holland',
    author_email='josh@inv.alid.pw',
    license="BSD",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'beeminder_dow', # this may well be wrong
        ]
    }
)
