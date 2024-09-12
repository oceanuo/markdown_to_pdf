# Markdown to PDF App

A Streamlit application that converts Markdown to PDF with customizable styling options.

## Demo

Try the live demo: [https://oceanuo.streamlit.app](https://oceanuo.streamlit.app)

## Features

- Upload or input Markdown text
- Convert Markdown to HTML with table support
- Preview HTML output
- Customize font size, font family, and line height
- Generate and download PDF

## Requirements

- Python 3.7+
- Streamlit
- markdown2
- pdfkit

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/markdown-to-pdf-app.git
   cd markdown-to-pdf-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install wkhtmltopdf:
   - On Ubuntu: `sudo apt-get install wkhtmltopdf`
   - On macOS: `brew install wkhtmltopdf`
   - On Windows: Download from https://wkhtmltopdf.org/downloads.html

## Usage

Run the Streamlit app: