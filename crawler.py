import requests
from bs4 import BeautifulSoup

url = "https://www.kijiji.ca/b-richmond-bc/car/k0l1700288?dc=true"
base_url = "https://www.kijiji.ca/b-cars-trucks/richmond-bc/car"
nodes_to_visit = set()
visited_nodes = set()

nodes_to_visit.add(url)

while(len(nodes_to_visit) != 0):
    current_url = nodes_to_visit.pop()
    print("Now visiting: ")
    print(current_url)

    ######## fetch HTML into beautifulsoup ########
    res = requests.get(current_url)
    soup = BeautifulSoup(res.text, features="html.parser")
    visited_nodes.add(current_url)
    ######## parse info out of the page ########
    info_containers = soup.find_all("div", class_="info-container")

    for info_container in info_containers:
        price = info_container.find("div", class_="price").contents[0].strip()
        title = info_container.find("div", class_="title").a.text.strip()
        url = info_container.find("div", class_="title").a.href
        full_url = requests.compat.urljoin(current_url, url) # use as the unique identifier
        # print(title, price, full_url)
        ######## TODO: Store item info in permanent storage ########

    ######## add child links to nodes to visit if not visited ########
    def is_pagination_link(full_link):
        return full_link.startswith(base_url) # alternative would be to use regex

    def get_full_link(a):
        return requests.compat.urljoin(current_url, a.get('href'))

    def get_child_links():
        full_links = map(get_full_link, soup.find("div", class_="pagination").find_all('a'))
        filtered = filter(is_pagination_link, full_links)
        return list(filtered)

    child_links = get_child_links()

    unvisited_nodes = set(child_links) - visited_nodes

    nodes_to_visit.update(unvisited_nodes)

print("Nodes visited:")
for node in visited_nodes:
    print(node)