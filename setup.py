from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements

setup(
    name='games_seeker',
    version='1.0.0',
    packages=find_packages(),
    include_package_date=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        games_seeker=games_seeker.main:cli
    """,
)
