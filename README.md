# CVPR Reading Tool

## Overview
The **CVPR Reading Tool** is a Python-based utility designed to streamline the process of exploring and analyzing CVPR (Conference on Computer Vision and Pattern Recognition) accepted papers. It automates the following tasks:
- Scraping highlighted papers from the CVPR website.
- Searching for papers on arXiv and extracting their links.
- Searching for relevant YouTube videos and transcripts.
- Generating a structured PDF report summarizing the findings.

This tool is particularly useful for researchers and enthusiasts who want to efficiently explore cutting-edge research in computer vision.

Take a look at the .pdf file in this repo as an example. To generate this, the tool goes over >2000 paper, finds ~330 highlighted paper, gets youtube link if there is any, and summarize the transcript. All the process will cost you < $0.005.
You will be very superised how many AI gen video/podcasts are in youtube now.
---

## Repository Structure
### 1. **`cvpr_highlight_filter.py`**
   - **Purpose**: 
     - Scrapes the CVPR website for highlighted papers.
     - Searches for related papers on arXiv.
     - Generates a PDF report summarizing the highlighted papers and their corresponding YouTube results.
   - **How to Use**:
     1. Ensure all dependencies are installed (see [Installation](#installation)).
     2. Run the script:
        ```bash
        python cvpr_highlight_filter.py
        ```
     3. The script will generate a PDF report (`highlighted_papers_results.pdf`) in the repository directory.

### 2. **`search_youtube.py`**
   - **Purpose**:
     - Searches YouTube for videos related to a given query.
     - Extracts video transcripts for further analysis.
   - **How to Use**:
     - This script is used as a helper function by [cvpr_highlight_filter.py]:
       ```python
       from search_youtube import collect_context
       result = collect_context("Your search query")
       print(result)
       ```
     You can also use it independently and allow for flexible input. Currently, we use it to search the cvpr paper. But I have tested to search other things e.g. other papers or concepts. Give it a try!
---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/linlilamb/cvpr_reading_tool.git
   cd cvpr_reading_tool
   pip install -r requirements.txt
   ```
2. Get openAI API token and add it to search_youtube.py

## To Do :rocket:
1. make cvpr_highlight_filter.py more flexible to enable other searching, e.g. medical imaging application
2. use openAI API and CVPR 2025 as database to create a RAG for more acurate topic searching
3. Enable automate catogrization of CVPR 2025.
4. Build multi-agent to integrate all the functions 
