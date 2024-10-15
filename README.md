# Assignment-3 Python

## Python VERSION
The python version **`3.12.3`**, and rest packages versions are mentioned in `requirements.txt` file.

## Overview
The `data_extractor` directory houses a set of tools specifically designed to extract data from various file formats and efficiently store the resulting information.

## How to Use
To begin, clone the repository with command `git clone https://github.com/AmanBhattShorthillsAI/Assignment_3_python.git` and run the `requirements.txt` file to install the packages used in the project. <br>Run the project with `python main.py` command in terminal and give the absolute path of file you want to extract as an input.</br>

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
Run the command `sqlite3 <DATABASE_NAME>.db` in the terminal and see the tables made using `.tables` and retrieve the content from the table using `SELECT * FROM <TABLE_NAME>`.

## Functionality
The `data_extractor` offers the following features:

- Extracts data from PDF, DOCX, and PPTX files using the appropriate loaders.
- Saves the extracted data either in a file or in a SQL database using the provided storage options.
- Provides a unified interface for easy access to the extracted data.

## Unit Tests
The unit tests are written using `pytest` framework inside `data_extractor/tests/test_extractor.py` file.

- Run the unit test file using `python -m pytest <FILE_PATH> -vv` command. 
- The `-vv` is for **verbose** to see the exact number of errors and problem where the errors/failures arises

## Purpose
The main goal of the `data_extractor` directory is to deliver a user-friendly and efficient method for extracting data from a variety of file formats and storing that data for subsequent analysis or processing.