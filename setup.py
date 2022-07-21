import setuptools

setuptools.setup(
    name="XYZCarDetect4",
    version="2022.07.21.12.01",
    author="HuangKai",
    url="https://github.com/WillEEEEEE/XYZCarPlates4.git",
    packages=setuptools.find_packages(),
    package_data={
        '': ['**/*.ini', '**/*.json']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
