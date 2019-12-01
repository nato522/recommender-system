# Collaborative-Filtering Recommender System
This project consists on analyzing the results of applying a CFRS to the same matrix of ratings, in the first case with
25% of the matrix empty and in the second case with the 75% of the matrix empty.

## Getting started

For this project we are going to need Python 3. In the case you don't have Python 3 installed [you can find it
here](https://www.python.org/downloads/release/python-373/).

To make sure you have installed it correctly you can execute the command `python --version`, and if the version is still
not *3.7.3* try with `python3 --version`.

Then, use the `pip` tool to install all the needed packages. For that, execute the following command from the project
root folder:

`pip install --user numpy xlsxwriter`

## How it works

Now that you have everything installed, you can execute the program using the command:

`python recommender_system.py` or `python3 recommender_system.py`

The results will appear in the folder `./results`.