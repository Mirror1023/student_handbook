########## data_prep.py ##########


### LIBRARY/DATA IMPORT ###   ### LIBRARY/DATA IMPORT ###   ### LIBRARY/DATA IMPORT ###   


import pandas as pd
import numpy as np
from typing import List
import PyPDF2

from src.paths import DATA_DIR

def load_pdf_data_from_disk(file_name: str) -> str:
    """
    Loads PDF files that were previously generated and saved locally

    Args:
        file_name (str): name of the PDF file (not the path, just the name)

    Returns:
        str: Extracted text content from the specified PDF file.
    """
    
    with open(DATA_DIR / file_name, "rb") as file:
        # Initialize PDF reader
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from each page
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text


### DATA CLEANSING ###   ### DATA CLEANSING ###   ### DATA CLEANSING ### 


import re

def clean_and_format_text(raw_text: str) -> str:
    """
    Cleans and formats the provided raw text. This involves removing excessive whitespace, 
    irregular characters, fixing known text issues, and reformatting the text for better presentation.

    Args:
        raw_text (str): The raw text string that needs to be cleaned and formatted.

    Returns:
        str: The cleaned and formatted version of the input text.
    """

    # Remove excessive whitespace and newline characters
    cleaned_text = re.sub(r'\n+', '\n', raw_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Remove any irregular characters that are common in PDF extraction
    cleaned_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', cleaned_text)
    
    # Remove spaces before punctuation marks
    cleaned_text = re.sub(r' \.', '.', cleaned_text)
    cleaned_text = re.sub(r' ,', ',', cleaned_text)
    cleaned_text = re.sub(r' !', '!', cleaned_text)
    cleaned_text = re.sub(r' \?', '?', cleaned_text)
    
    # Attempt to fix split words (this might not catch all cases)
    cleaned_text = re.sub(r' ([a-z]) ', r'\1', cleaned_text)
    
    # Fix known issues
    cleaned_text = cleaned_text.replace("sitein", "site in")
    cleaned_text = cleaned_text.replace("offersabalanced", "offers a balanced")
    cleaned_text = cleaned_text.replace("Psychia try", "Psychiatry")
    cleaned_text = cleaned_text.replace("areacommitment", "are a commitment")
    cleaned_text = cleaned_text.replace("asatrainee", "as a trainee")
    
    # Break the text into paragraphs for better presentation
    paragraphs = cleaned_text.split('\n')
    formatted_text = "\n\n".join(paragraphs)
    
    return formatted_text



