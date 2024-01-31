# Energy Price Analysis and Visualization with FastAPI
In this project, you will have a look at the energy price analysis and visualization using Python, FastAPI, and Altair. The primary goal of this assignment is to create a robust FastAPI web application capable of fetching, analyzing, and presenting electricity prices in an interactive and visually appealing manner. 

## Installation
To get started, ensure you have Python 3.8 or above installed on your system. To install the in3110_instapy package, use pip in your project's root directory:

```
python3 -m pip install .
```

## Required dependencies
Make sure you have the following dependencies installed before running the code:

Installed the pacakges with this command:
```
    python -m pip install altair==4.*
    python -m pip install altair-viewer
    python -m pip install beautifulsoup4
    python -m pip install "fastapi[all]"
    python -m pip install pandas
    python -m pip install pytest
    python -m pip install requests
    python -m pip install requests-cache
    python -m pip install uvicorn
```
## Displaying the graphic visualization
Run the Strompris.py:
```
python strompris.py
```

## Displaying the webpage
Run the FastAPI app:
```
python app.py 
```
Access the webpage by following the link, like http://127.0.0.1:5000/, to open your web browser.

## Starting with Sphinx documentation
Sphinx provides a way to quickly generate a documentation page for the project, using information you’ve already provided in your docstrings.  

Install Sphinx 
```
python -m pip install sphinx
```
Create a directory inside your project to hold your docs:
```
cd /path/to/project
mkdir docs
```
Run sphinx-quickstart in there:
```
cd docs
sphinx-quickstart
```
Once done, you'll have files like index.rst, conf.py, and others. 

Now, open the index.rst file and share some key information about your project. You can include as many details as you want. Afterward, build the documents to see how they look.
```
make html
```
or for Windows PowerShell
```
sphinx-build -b html . _build
```
Now your documentation has been transformed from the index.rst file to an index.html file, and you can find it in your directory, usally docs/_build/html. Simply open this file in your web browser to view your documentation easily.

## Summary
After finishing the assignment, you have mastered crafting a web-based energy price visualization for Norway using the Hva Koster Strømmen API is evident. The development includes building functions to fetch and present energy prices, creating a FastAPI web app, and documenting the process using Sphinx.