"""
GRAVITYchat - main chat file
--------------------------------
This script serves as the main executable for GRAVITYchat, a system that acts as
1. a search tool
2. a factual summarizer of documentation

It aims to do this through finetuning using
1. LIGO related whitepapers
2. Gravity Spy related publications
3. Gravity Spy Talk and Wiki
4. aLOGs

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

# Standard Libraries
import requests

# Third-party Libraries
import dotenv
import openai
import pandas
#import panoptes_client

# Local Libraries
import __prompt__

# 1. Data Collection and Preprocessing
#   a. PDF Processing
#   b. Text Cleaning
# 2. Train the LLM
#
# 3.


def chat(input):
    """

    Args:
        input (str): The text input provided by a volunteer
    Returns:

    Notes:

    """

print(__prompt__.prompt)

"""
BACKLOG:
    1. Create an outline of project and start filling it in

"""
