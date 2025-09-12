"""
Setup script for Faculty and Class Management System
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="faculty-class-management",
    version="1.0.0",
    author="Faculty Management System",
    author_email="admin@facultymanagement.com",
    description="A comprehensive Python-based automated system for managing faculty, classes, students, and enrollments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/faculty-class-management",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "faculty-management=main:main",
        ],
    },
    keywords="faculty management, class management, student management, education, school management",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/faculty-class-management/issues",
        "Source": "https://github.com/yourusername/faculty-class-management",
    },
)