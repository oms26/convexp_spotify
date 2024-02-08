# Spotify Service
Experiments team assessment - using Spotify API

## Project Description
This Python package uses the Spotify Web API to retrieve data on artists and tracks, perform basic analysis, and visualise the data. 

## Setup
Create a Spotify app on your 'Spotify for Developers' dashboard.

### Virtual Environment
This package uses Python 3.10. Ensure you have Anaconda/Miniconda installed compatible with Python 3.10.

To create your virtual environment, in the project root directory, run:

`conda env create -f environment.yml`

### Environment Variables
Replace the CLIENT_ID and CLIENT_SECRET environment variables in .env.example with your client ID and client secret from your Spotify app.

Rename .env.example to .env

## Usage
`main.ipynb` is the Jupyter notebook to run. This file uses functions located in `src`.
