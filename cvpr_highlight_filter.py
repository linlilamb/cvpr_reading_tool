import requests
from bs4 import BeautifulSoup
from pdb import set_trace
import search_youtube
from fpdf import FPDF


# URL of the CVPR Accepted Papers page
url = "https://cvpr.thecvf.com/Conferences/2025/AcceptedPapers"

# Fetch the webpage
response = requests.get(url)
highlighted_papers = []
highlighted_papers_arxiv = []
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all paper containers
    highlight_icons = soup.find_all('img', {'title': "Highlight"})  # Assuming titles are in <strong> tags
    
    # Extract highlighted papers
    for icon in highlight_icons:
        # Find the <strong> tag before the <img> tag
        strong_tag = icon.find_previous('strong')
        if strong_tag:
            # print(strong_tag.get_text(strip=True))

            highlighted_papers.append(strong_tag.get_text(strip=True))
            # Check if the paper is available on arXiv
            paper_title = strong_tag.get_text(strip=True)
            arxiv_search_url = f"https://arxiv.org/search/?query={paper_title}&searchtype=all"
            arxiv_response = requests.get(arxiv_search_url)
            if arxiv_response.status_code == 200:
                arxiv_soup = BeautifulSoup(arxiv_response.text, 'html.parser')
                result_list = arxiv_soup.find_all('li', {'class': 'arxiv-result'})
                if result_list:
                    print(f"Paper '{paper_title}' found on arXiv.")
                   # Extract the arXiv link from the first result
                    first_result = result_list[0]
                    arxiv_link_tag = first_result.find('a', {'href': True})
                    if arxiv_link_tag and 'href' in arxiv_link_tag.attrs:
                        arxiv_link = arxiv_link_tag['href']
                        highlighted_papers_arxiv.append(arxiv_link)
                    else:
                        print(f"Abstract link not found for paper '{paper_title}'.")
                        highlighted_papers_arxiv.append("Abstract link not found")
                    
                else:
                    print(f"Paper '{paper_title}' not found on arXiv.")
                    highlighted_papers_arxiv.append("Not found on arXiv")# set_trace()
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")

# Print the highlighted papers
print("ALL number of Highlighted Papers:", len(highlighted_papers))

results = []
for paper in highlighted_papers:
    result = search_youtube.run_rag_youtube_search(paper)
    results.append(result)
    print('TITLE:', paper)
    print("RESULTS:", result)

# Create a PDF instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add a title
pdf.set_font("Arial", style='B', size=16)
pdf.cell(200, 10, txt="Highlighted Papers and YouTube Results", ln=True, align='C')
pdf.ln(10)

# Add each paper and its YouTube result to the PDF
pdf.set_font("Arial", size=12)
for paper, arxiv, result in zip(highlighted_papers, highlighted_papers_arxiv,results):
    pdf.multi_cell(0, 10, txt=f"Paper: {paper}")
    pdf.multi_cell(0, 10, txt=f"Paper link: {arxiv}")
    pdf.multi_cell(0, 10, txt=f"YouTube Result: {result}")
    pdf.ln(5)

# Save the PDF to a file
output_path = r"C:/Users/Lin/OneDrive/Documents/CVPR_reading_tool/highlighted_papers_results.pdf"
pdf.output(output_path)

print(f"PDF saved to {output_path}")