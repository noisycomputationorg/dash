from setuptools import setup
import json

with open("package.json") as f:
    package = json.load(f)

package_name = str(package["name"].replace(" ", "_").replace("-", "_"))

repo_url='https://github.com/noisycomputation/dash'

setup(
    name=package_name,
    version=package["version"],
    author=package["author"],
    packages=[package_name],
    url=repo_url,
    include_package_data=True,
    license=package["license"],
    description=package.get("description", package_name),
    long_description=f"See <{repo_url}>",
    long_description_content_type='text/markdown',
    install_requires=[],
)
