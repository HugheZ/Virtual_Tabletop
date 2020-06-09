import setuptools

desc = ''

with open("README.md", "r") as f:
    desc = f.read()

setuptools.setup(
    name="virtual_tabletop",
    version="0.0.1",
    author="Zachary Hughes",
    description="A tabletop virtualizer",
    long_description=desc,
    url="https://github.com/HugheZ/Virtual_Tabletop",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Games/Entertainment :: Board Games",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7'
)