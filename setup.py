from setuptools import setup
import re


def version() -> str:
    with open('twitch/__init__.py', encoding='utf-8') as file:
        text = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)
        return text


setup(version=version())
