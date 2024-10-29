# PDF to Markdown Converter

This is a tool to convert academic papers in PDF format to Markdown format. The tool separates each section of the paper with a delimiter (`=+=+=+=+=+=+=+=+=`) and converts images to online URLs for easy handling and publishing.

## Features
- Converts PDF paper content to Markdown format.
- Adds a delimiter `=+=+=+=+=+=+=+=+=` between sections for clear content structure.
- Automatically processes images, converting them to online URLs.

## Prerequisites
- Install the required dependencies listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Initialize Configuration File**:
   - Use the `cp` command to rename `.env.example` to `.env`.
   - Get API Keys from [Doc2X](https://open.noedgeai.com/apiKeys) and [aliyun OSS](https://oss.console.aliyun.com/)
   - Fill in required API Keys in the `.env` file.

2. **Prepare Files**:
   - Place the PDF files you want to process in the `Files` folder.

3. **Run the Conversion Program**:
   - Execute the following command to start the conversion:
     ```bash
     python3 pdf_to_md_converter.py
     ```

4. **Check the Output**:
   - The converted Markdown files will be saved in the `Output` folder.

## Project Structure
```plaintext
.git/
├── Files/                 # Directory for PDF files to be processed
├── Output/                # Directory for converted Markdown files
├── .env                   # Configuration file for storing API Key and other settings
├── .env.example           # Example configuration file
├── requirements.txt       # File listing required Python packages
├── pdf_to_md_converter.py # Main program file
└── README.md              # User guide
