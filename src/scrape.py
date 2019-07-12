from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

# URL of the initial NEB web page with table of enzymes and recognition sequences
neb_url = "https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities"
# Dictionary to hold the names of enzymes and (unit size, price). To be filled by initNebPriceDict
neb_price = {}

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
	global neb_url
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
	global neb_url
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

# Return a list of tuples (size 2) with enzyme name as first element and href as second
def initNebHrefList():
	global neb_url
	neb_initial_soup = getSoup(neb_url)
	neb_total_list = neb_initial_soup.table.find_all("td")
	neb_href = []
	for i in range(0,len(neb_total_list),2):
		if multipleA(neb_total_list[i + 1]):
			for j in neb_total_list[i + 1].find_all('a'):
				neb_href.append((j.string, "https://www.neb.com" + j["href"]))
		else:
			neb_href.append((neb_total_list[i + 1].a.string, "https://www.neb.com" + neb_total_list[i + 1].a["href"]))
	return neb_href

# Store enzyme name to key of dictionary and (unit size, enzyme price) to value. To be called by multithreading function.
# Requests the page of a given url from initNebHrefDict as defined by the parameter and adds the value to the price dictionary.
def initNebPriceDict(name):
	global neb_price
	href_dict = initNebHrefDict()
	price_html = grabHtml(href_dict[name])
	price_soup = soup(price_html, "html.parser")
	neb_price[name] = (price_soup.find("table", {"class": "js-pdp-product-grid"}).find("span", {"class": "product-info__size"}).string, price_soup.find("table", {"class": "js-pdp-product-grid"}).find("span", {"class": "product-info__listprice"}).string)