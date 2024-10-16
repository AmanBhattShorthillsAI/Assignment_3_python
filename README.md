# Assignment-4 Python

## Python VERSION
The python version **`3.12.3`**, and rest packages versions are mentioned in `requirements.txt` file.

## Overview
The `data_extractor` directory houses a set of tools specifically designed to extract data from various file formats and efficiently store the resulting information.

## Installation
To begin, clone the repository with command file to install the packages used in the project. 

```bash
git clone https://github.com/AmanBhattShorthillsAI/Assignment_3_python.git
``` 
and run the `requirements.txt` 
```bash
pip install -r requirements.txt
```
Run the project with `python main.py` command in terminal and give the absolute path of file you want to extract as an input.

## Run the project
After cloning the project, run the `main.py` file.
```bash
python main.py
```
and provide the path of file as an **input**.

## Loaders
The `data_extractor` directory features the following loaders, which facilitate data extraction from various file types:

- **PDFLoader**: Validate and Load the data from PDF files.
- **DOCXLoader**: Validate and Load the data from DOCX files.
- **PPTLoader**: Validate and Load the data from PPTX files.

## Data Extraction
The `data_extractor` leverages the specified loaders to collect data from supported file formats, providing a unified interface for accessing the extracted information.
- **PDFExtractor**: Extracts the data from the PDF files.
- **DOCXExtractor**: Extracts the data from DOCX files.
- **PPTXExtractor**: Extracts the data from PPTX files.

## Storage Options
The `data_extractor` directory offers the following storage solutions for managing the extracted data:

- **FileStorage**: Saves the extracted data as a directory structure.
- **SQLStorage**: Saves the extracted data in a SQLite database.

## How to see the database
Run the command 
```bash
sqlite3 <DATABASE_NAME>.db
``` 
in the terminal and see the tables made using `.tables` and retrieve the content from the table using 
```bash
SELECT * FROM <TABLE_NAME>
```

## Functionality
The `data_extractor` offers the following features:

- Extracts data from PDF, DOCX, and PPTX files using the appropriate loaders.
- Saves the extracted data either in a file or in a SQL database using the provided storage options.
- Provides a unified interface for easy access to the extracted data.

## Unit Tests
The unit tests are written using `pytest` framework inside `data_extractor/tests/test_extractor.py` file.

- Run the unit test file using 
```bash
python -m pytest <FILE_PATH> -vv
``` 
command. 
- The `-vv` is for **verbose** to see the exact number of errors and problem where the errors/failures arises

## Purpose
The main goal of the `data_extractor` directory is to deliver a user-friendly and efficient method for extracting data from a variety of file formats and storing that data for subsequent analysis or processing.