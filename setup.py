from setuptools import setup, find_packages

setup(
    name='run_anova',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas==2.0.0',
        'scipy==1.11.2'
    ],
    description='Run ANOVA tests between gene knockouts and driver mutations'
)