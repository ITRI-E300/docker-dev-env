import setuptools

setuptools.setup(
    name="denv", # 
    version='0.0.1',
    author="Philip Huang",
    author_email="p208p2002@gmail.com",
    description="docker-dev-env",
    url="https://github.com/ITRI-E300/docker-dev-env",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['denv=denv:main'],
    },
    python_requires='>=3.5',
    install_requires = ['requests','loguru']
)