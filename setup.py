import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='desword',
    version='0.0.5',
    author='Tom Lockwood',
    author_email='tom@lockwood.dev',
    description="A markdown worldbuilder's assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tomlockwood/desword',
    project_urls={
        "Bug Tracker": "https://github.com/tomlockwood/desword/issues"
    },
    packages=['desword', 'desword.lib', 'desword.templates'],
    install_requires=['Markdown==3.3.4'],
    include_package_data=True,
)
