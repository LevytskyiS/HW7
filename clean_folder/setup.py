from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='It sorts your files',
    url='https://github.com/LevytskyiS/HW7',
    author='Levytskyi Serhii',
    author_email='berzerksn@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
    )