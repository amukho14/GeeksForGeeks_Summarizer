__author__ = 'amukhopadhyay'

from Queue import Queue
from threading import Thread
import threading

from mechanize import Browser
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
import ConfigParser


def substitute_html_entities(str):
    # return EntitySubstitution.substitute_html(str)
    # return EntitySubstitution.substitute_html(str).replace("&acirc;&euro;&trade;","\'").replace("&acirc;&euro;&oelig;","\"").replace("&acirc;&euro;","\"").replace("&gt",">")\
    return EntitySubstitution.substitute_html(str).replace("&ldquo;","\"").replace("&rdquo;","\"").replace("&rsquo;","'")



def getOneExperience(q, path):
    while True:

        url = q.get()
        print url
        # pathToFile = "C:\\Users\\amukhopadhyay\\Desktop\\gfg.html"
        # pathToFile = path
        writeToFile=""

        br = Browser()
        br.set_handle_robots(False)
        br.set_handle_equiv(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        # url= raw_input("givepath:")
        # url = "http://www.geeksforgeeks.org/amazon-interview-experience-set-158-off-campus/"
        try:
            br.open(url)
        except:
            print "what experience is this man? " + url
        soup = BeautifulSoup(str(br.response().read()), from_encoding="utf-8")
        # print(soup.prettify(formatter=substitute_html_entities))
        soup = BeautifulSoup(soup.prettify(formatter=substitute_html_entities))

        for i in soup.find_all('h2',{'class':'post-title'}, limit=1):
            writeToFile +="<h2>"+i.string.encode('utf-8')+"</h2>"

        flag=0
        for i in soup.find_all('div',{'id':'content'}):
            # print i.prettify()
            soup2 = BeautifulSoup(i.prettify())
            if flag == 1:
                break
            for j in soup2.find_all('p'):
                if flag == 1:
                    break
                if j.string is not None:
                    if len(j.string.strip()) >25:
                        if j.string.strip()[:25] == "If you like GeeksforGeeks":
                            flag=1
                            j="\n\n\n"
                writeToFile+=(j.encode('utf-8').replace("\'",""))


        MY_LOCK.acquire()
        with open(path, 'a') as f:
            f.write(writeToFile)
            f.close()
        MY_LOCK.release()
        q.task_done()
        # return

    # q.task_done()

def hitPage(url = "http://www.geeksforgeeks.org/tag/amazon/"):
    #from the page extract all the interviewExperiencesLinks
    br = Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    try:
        br.open(url)
    except:
        print "what page for interview exp is this, man? " + url
        return
    #different thread for link on same page
    #same thread to iterate of each of the pages
    q = Queue(maxsize=0)


    #thirteen links on each page and of course, lucky number thirteen.
    num_threads = 13
    soup = BeautifulSoup(str(br.response().read()), from_encoding="utf-8")


    for i in soup.find_all('h2',{'class':'post-title'}):
        soup2=BeautifulSoup(i.prettify())
        for j in soup2.find_all('a'):
            q.put(str(j.get('href')))


    for i in range(num_threads):
        worker = Thread(target=getOneExperience, args=(q,path))
        worker.setDaemon(True)
        worker.start()

    q.join()
    return


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
x= ConfigSectionMap('Paths')
path = ConfigSectionMap("Paths")['path']
MY_LOCK = threading.Lock()
for i in range(2,17):
    url = "http://www.geeksforgeeks.org/tag/amazon/page/"+str(i)+"/"
    hitPage(url)
