import sys
import re
import xml.etree.ElementTree as ET

tree = ET.parse('publications.xml')
root = tree.getroot()

def format_html(text, cls):
    return '\t<div class="{}">{}</div>'.format(cls, text)

def wl(f, l):
    f.write('{}\n'.format(l))

c = 1

f = open('publications.html', 'w')

wl(f, '<div class="pubs">')

for pubmed_article_elem in root.findall('PubmedArticle'):
    wl(f, '<div class="pub">')
    
    citation_elem = pubmed_article_elem.find('MedlineCitation')
    article_elem = citation_elem.find('Article')
    title_elem = article_elem.find('ArticleTitle')
    journal_elem = article_elem.find('Journal')
    journal_title_elem = journal_elem.find('Title')
    journal_issue_elem = journal_elem.find('JournalIssue')
    
    year = ''
    
    pub_date_elem = journal_issue_elem.find('PubDate')
    
    if pub_date_elem is not None:
        year_elem = pub_date_elem.find('Year')
        
        if year_elem is not None:
            year = year_elem.text
    
    if year == '':
        revised_elem = pubmed_article_elem.find('DateRevised')
        
        if revised_elem is not None:
            year_elem = revised_elem.find('Year')
            
            if year_elem is not None:
                year = year_elem.text
    
    title = title_elem.text
    title = re.sub(r'\.$', '', title)
    title = '{}. {}'.format(c, title)
    
    doi = None
    
    for doi_elem in article_elem.findall('ELocationID'):
        if doi_elem.attrib['EIdType'] == 'doi':
            doi = doi_elem.text
            break
        
    
    if doi is not None:
        doi = 'https://dx.doi.org/{}'.format(doi)
        title = '<a class="link" href="{}">{}</a>'.format(doi, title)
    
    title = format_html(title, 'pub-title')
    wl(f, title)
    
    title = journal_title_elem.text
    title = re.sub(r'\.$', '', title)
    
    
    
    author_list_elem = article_elem.find('AuthorList')
    
    name_list = []
    
    for author_elem in author_list_elem.findall('Author'):
        last_name_elem = author_elem.find('LastName')
        
        if last_name_elem is not None:
            fore_name_elem = author_elem.find('ForeName')
            
            last_name = last_name_elem.text
            fore_name = fore_name_elem.text
            
            name = '{} {}'.format(fore_name, last_name)
            
            name_list.append(name)
    
    if len(name_list) == 0:
        names = ''
    elif len(name_list) == 1:
        names = name_list[0]
    else:
        names = ', '.join(name_list[:-1])
        names = '{}, and {}'.format(names, name_list[-1])
    
    names = format_html(names, 'pub-authors')
    
    wl(f, names)
    
    
    
    title = format_html('{} {}'.format(title, year), 'pub-journal-title')
    wl(f, title)
    
    wl(f, '</div>')
    
    c += 1

wl(f, '</div>')

f.close()