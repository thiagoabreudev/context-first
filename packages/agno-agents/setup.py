from setuptools import setup, find_packages

setup(
    name="agno-agents",
    version="0.1.0",
    description="AI agents for context-first platform",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "agno>=0.0.1",
        "anthropic>=0.40.0",
    ],
)
