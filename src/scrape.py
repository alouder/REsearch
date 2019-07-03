from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Store open connection to URL into var, store html page into var, and then close connection
# neb_url = "http://rebase.neb.com/rebase/supps/N:__New_England_Biolabs.html"
# uClient = uReq(neb_url)
# neb_initial_html = uClient.read()
# uClient.close()

# Store html parse tree into var using BeautifulSoup
with open("REBASE supplier N - New England Biolabs.html") as neb_initial_html:

	neb_initial_soup = soup(neb_initial_html, "html.parser")
	initial_table_list = neb_initial_soup.find_all('table', limit=11)
	target_table = initial_table_list[10]
	del initial_table_list

	links = []
	url_prefix = "http://rebase.neb.com"
	for i in target_table.find_all('a'):
		links.append(url_prefix + i['href'])

	rec_seq_list = []
	for i in links:
		url = i
		uClient = uReq(i)
		re_html = uClient.read()
		uClient.close()
		
		re_soup = soup(re_html, "html.parser")
		rec_list = re_soup.find_all('font', limit=8)
		target_font = rec_list[7]
		del rec_list

		rec_seq_list.append(target_font.string)

	rec_seq_file = open("recognition_sequences.txt", "w")
	for i in rec_seq_list:
		rec_seq_file.write(i + "\n")
	rec_seq_file.close()

	# USE NEW FOUND SITE
	# EMAIL NEB ABOUT USING SITE



