from setuptools import setup, find_packages


# Function to read the list of dependencies from requirements.txt
def read_requirements():
    with open('requirements.txt', 'r') as req:
        return req.read().splitlines()


setup(
    name="evaluableai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    author_email="contactus@evaluable.ai",
    description="SDK for interacting with EvaluableAI web application",
)
