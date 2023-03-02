import requests
import re
import multiprocessing
import threading
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from networkx import algorithms

##Global Variables##
links = []
tempLinks = []
G = nx.Graph()

##Configuration##
SourceURL = "https://www.reddit.com/"
Mode = "Connection Discovery"
DestinationURL = "https://www.twitter.com/"
WebsiteLimit = 100
threads = 4


def GetSiteURLs(URL):

    #Requesting Site Content
    res = requests.get(URL)
    sop = BeautifulSoup(res.content, features="html.parser")

    for item in sop.findAll('a', attrs={'href': re.compile("^https://")}):
        Result = item.get('href')
        if Result in links:
            print ("URL Already added")
            tempLinks.append(Result)
        else:
            links.append(Result)
            tempLinks.append(Result)
            print(Result) 

    print (str(len(links))+" Unique Hits")


def main():

    MapWebsites()
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def MapWebsites():

    #Runs Function First Time
    GetSiteURLs(SourceURL)

    jobs = []

    G.add_node(SourceURL)

    for item in links:
        G.add_edge(SourceURL, item)

    #Looping through Links DS
    for item in links:
        
        GetSiteURLs(item)
        
        for j in jobs:
            j.start()
            del jobs[:]

        for row in tempLinks:
            if (G.has_node(row)):
                G.add_edge(item, row)
            else:
                G.add_node(row)
                G.add_edge(item, row)
                
        #Resets Temp List
        del tempLinks[:]

        #Check Mode
        if (Mode == 'Connection Discovery'):
            if (len(links) > WebsiteLimit):
                break

        #Check Mode
        if (Mode == 'Path Finder'):
            try:
                if(nx.has_path(G ,SourceURL, DestinationURL)):
                    print("Path Found")
                    Path = nx.astar_path(G, SourceURL, DestinationURL)
                    G.remove_nodes_from(links)
                    G.add_path(Path)
                    break
            except:
                pass

main()
