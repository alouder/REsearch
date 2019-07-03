from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup

# Check if an element has multiple a tags
def multipleA(parent):
	if len(parent.find_all('a')) > 1:
		return True
	return False

def tagListToDict(parent_list, index, tag, dic):
	for i in parent_list[index].find_all(tag):
		dic[i.string] = parent_list[index - 1].string


# Store open connection to URL into var, store html page into var, and then close connection
neb_url = "https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities"
req = Request(neb_url, headers={'User-Agent': 'Mozilla/5.0'})
uClient = urlopen(req)
neb_initial_html = uClient.read()
uClient.close()

# Store html parse tree into var using BeautifulSoup
neb_initial_soup = soup(neb_initial_html, "html.parser")
total_list = neb_initial_soup.table.find_all("td")

enz_seq_dict = {}
for i in range(0,len(total_list),2):
	if multipleA(total_list[i + 1]):
		# DECIDE TO KEEP: tagListToDict(total_list, i + 1, "a", enz_seq_dict)
		for j in total_list[i + 1].find_all('a'):
			enz_seq_dict[j.string] = total_list[i].string
	else:
		enz_seq_dict[total_list[i + 1].a.string] = total_list[i].string





