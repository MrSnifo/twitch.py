from setuptools import setup

setup(
    name='twitchify',
    version='1.0.0',
    python_requires='>=3.8.0',
    packages=['twitch', 'twitch.types'],
    author='Snifo',
    author_email='Snifo@mail.com',
    description='A Python Twitch API wrapper',
    url='https://github.com/mrsnifo/twitchify',
    install_requires=['aiohttp>=3.8.0'],
    license='MIT',
)
