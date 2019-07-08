from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

# Check if an element has multiple a tags
def multipleA(parent):
	if len(parent.find_all('a')) > 1:
		return True
	return False

def openUrlConnection(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	uClient = urlopen(req)
	html_page = uClient.read()
	uClient.close()
	return html_page


# Store open connection to URL into var, store html page into var, and then close connection
neb_url = "https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities"
neb_initial_html = openUrlConnection(neb_url)

# Store html parse tree into var using BeautifulSoup
neb_initial_soup = soup(neb_initial_html, "html.parser")
neb_total_list = neb_initial_soup.table.find_all("td")

# MODULARIZE
neb_enz_seq_dict = {}
for i in range(0,len(neb_total_list),2):
	if multipleA(neb_total_list[i + 1]):
		for j in neb_total_list[i + 1].find_all('a'):
			neb_enz_seq_dict[j.string] = neb_total_list[i].string
	else:
		neb_enz_seq_dict[neb_total_list[i + 1].a.string] = neb_total_list[i].string





