import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

with open("requirements.txt") as f:
	requirements = "\n".split(f.read())

setuptools.setup(
	name = "nb2pdf",
	version = "0.6.2",
	author = "Chris Pyles & Yanay Rosen",
	author_email = "ds-infra@berkeley.edu",
	description = "Jupyter Notebook to PDF Converter",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/ucbds-infra/nb2pdf",
	license = "BSD-3-Clause",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
	],
	install_requires = [
		"nbformat",
		"nbpdfexport",
		"codecov",
		"IPython"
	],
	scripts=["bin/nb2pdf"]
)