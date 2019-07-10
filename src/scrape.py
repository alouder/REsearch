from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

neb_url = "https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities"

# Open connection, read page into var, close connection
def grabHtml(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	uClient = urlopen(req)
	html_page = uClient.read()
	uClient.close()
	return html_page

# Return BeautifulSoup html object given a url
def getSoup(url):
	return soup(grabHtml(url), "html.parser")

# Check if an element has multiple a tags
def multipleA(parent):
	if len(parent.find_all('a')) > 1:
		return True
	return False

# Return a dictionary from NEB page with enzyme names as keys and restriction sites as values
def initNebSeqDict():
	neb_initial_soup = getSoup(neb_url)
	neb_total_list = neb_initial_soup.table.find_all("td")
	neb_enz_seq_dict = {}
	for i in range(0,len(neb_total_list),2):
		if multipleA(neb_total_list[i + 1]):
			for j in neb_total_list[i + 1].find_all('a'):
				neb_enz_seq_dict[j.string] = neb_total_list[i].string
		else:
			neb_enz_seq_dict[neb_total_list[i + 1].a.string] = neb_total_list[i].string
	return neb_enz_seq_dict

# Return a dictionary with enzyme names as keys and hrefs as values
def initNebHrefDict():
	neb_initial_soup = getSoup(neb_url)
	neb_total_list = neb_initial_soup.table.find_all("td")
	neb_href = {}
	for i in range(0,len(neb_total_list),2):
		if multipleA(neb_total_list[i + 1]):
			for j in neb_total_list[i + 1].find_all('a'):
				neb_href[j.string] = "https://www.neb.com" + j["href"]
		else:
			neb_href[neb_total_list[i + 1].a.string] = "https://www.neb.com" + neb_total_list[i + 1].a["href"]
	return neb_href

# Return a dictionary with enzyme names as keys and prices as values
def initNebPriceDict(dic):
	href_dict = initNebHrefDict()
	price_total_list = []
	neb_price = {}
	for i in dic:
		price_html = grabHtml(href_dict[i])
		price_soup = soup(price_html, "html.parser")
		neb_price[i] = (price_soup.find("table", {"class": "js-pdp-product-grid"}).find("span", {"class": "product-info__size"}).string, price_soup.find("table", {"class": "js-pdp-product-grid"}).find("span", {"class": "product-info__listprice"}).string)
	return neb_price