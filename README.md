# DoiHarvest

A tool for batch downloading academic paper PDFs from Sci-Hub, Crossref, and Unpaywall.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
## Project Introduction

DoiHarvest is an automated tool designed to help researchers and scholars batch download academic paper PDF files. It supports obtaining papers from Sci-Hub,Crossref,Unpaywall API, featuring multi-threaded downloading, retry mechanisms, and intelligent domain rotation to improve download efficiency and success rate. Additionally, the tool provides Excel to Markdown conversion functionality for convenient literature information management and sharing.

## Features

- Supports reading literature DOI and title information from Excel files
- Automatically downloads paper PDFs from Sci-Hub
- Supports multi-threaded downloading to improve efficiency
- Supports retry mechanisms and random delays to avoid being blocked
- Automatically updates DOI links in Excel files
- Supports converting Excel files to Markdown format for manual downloading
- Provides download status checking functionality
- Supports downloading open access papers via Crossref API
- Supports downloading open access papers via Unpaywall API

## File Descriptions

- `download.py`: Main download script for downloading papers from Sci-Hub
- `config.py`: Configuration file containing Sci-Hub domain pool and download parameters
- `convertxls.py`: Converts .xls files to .xlsx format
- `creat_doi.py`: Generates DOI links for Excel files
- `convert_md.py`: Converts Excel files to Markdown format
- `Crossref_download.py`: Downloads open access papers using Crossref API
- `Unpaywall_download.py`: Downloads open access papers using Unpaywall API
- `judge.py`: Checks literature download status
- `requirements.txt`: Project dependency list

## Configuration Instructions

The following parameters can be adjusted in `config.py`:

- `SCI_HUB_DOMAINS`: Sci-Hub domain pool for rotation to avoid blocking
- `MAX_THREADS`: Number of concurrent download threads
- `RETRY_COUNT`: Number of retries for download failures
- `TIMEOUT`: Request timeout duration
- `MIN_DELAY` and `MAX_DELAY`: Random delay range

## Directory Structure

```
.
├── data/                 # Store Excel files to be processed
├── data_md/              # Store converted Markdown files
├── logs/                 # Store download.py logs
├── output/               # Store PDF files downloaded by download.py
├── download.py           # Download papers from Sci-Hub (may require proxy)
├── config.py             # Configuration file
├── convertxls.py         # xls to xlsx tool
├── creat_doi.py          # Generate DOI links in Excel tables
├── convert_md.py         # Excel to Markdown tool
├── Crossref_download.py  # Crossref download tool (no proxy required)
├── Unpaywall_download.py # Unpaywall download tool (no proxy required)
├── papers/               # Store papers downloaded by Crossref and Unpaywall
├── requirements.txt      # Project dependency file
└── README.md
```
## Install Dependencies

Before running the scripts, ensure the required Python libraries are installed:

```
pip install -r requirements.txt
```

## Usage

1. Place the Excel file containing literature information in the `data` directory
   - The Excel file should contain at least `DOI` column
2. Run `download.py` to start downloading literature
   ```
   python download.py
   ```
3. Downloaded PDF files will be saved in the `output` directory
4. Download status will be automatically updated in the original Excel file (it is recommended to delete the rows that have been downloaded in Excel to reduce the download volume of `Crossref_download.py` and `Unpaywall_download.py`)
5. Run `Crossref_download.py` or `Unpaywall_download.py` to start downloading literature
   ```
   python Crossref_download.py
   ```
   or
   ```
   python Unpaywall_download.py
   ```
6. Downloaded PDF files will be saved in the `papers` directory
7. If download fails and manual download is required, run `creat_doi.py` to generate DOI links and update them to the `DOI Link` column in the Excel file
   ```
   python creat_doi.py
   ```
8. Run `convert_md.py` to convert Excel files to Markdown format for manual downloading
   ```
   python convert_md.py
   ```


## Notes

- Ensure all dependencies are installed, which can be done via the `pip install -r requirements.txt` command
- Please comply with relevant laws and regulations and academic ethics, for personal learning and research only
- Network issues or Sci-Hub access restrictions may be encountered during downloading
- It is recommended to appropriately adjust the number of concurrent threads and delay time to avoid being blocked


## Notes
- `download.py` will automatically skip files already downloaded in output and will not download them repeatedly
- `Crossref_download.py` and `Unpaywall_download.py` will automatically skip files already downloaded in papers and will not download them repeatedly
- Please comply with relevant laws and regulations and academic ethics, for personal learning and research only
- Network issues or Sci-Hub access restrictions may be encountered during downloading
- It is recommended to appropriately adjust the number of concurrent threads and delay time to avoid being blocked
- Some literature may not be downloadable due to copyright protection
- Ensure all dependencies are installed, which can be done via the `pip install -r requirements.txt` command
