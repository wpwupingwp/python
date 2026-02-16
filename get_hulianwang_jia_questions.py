#!/usr/bin/env python
# coding: utf-8

# In[15]:


import bs4
import requests
from time import sleep


filename = "bookmarks.html"

_ = bs4.BeautifulSoup(open(filename))
hrefs = list()
for i in _.find_all("a"):
    hrefs.append(i.attrs["href"])
print(hrefs)


# In[33]:


results = list()
for link in hrefs:
    page = requests.get(link)
    p = bs4.BeautifulSoup(page.text)
    title = p.find(class_="single-line", id="acName").text
    hd_info = p.find(class_="hd-info")
    company = hd_info.find("span").text
    company_info = p.find(style="white-space: pre-wrap;word-break: break-word;").text
    question = p.find(class_="detail-content").text
    results.append((link, title, company, company_info, question))
    sleep(1)
    print(link, "finished")
print(results)


# In[34]:


r2 = list(results)
print(len(r2))


# In[40]:


import csv

out = open("result.csv", "w", newline="", encoding="gbk")
writer = csv.writer(out)
writer.writerow("Link,Title,Company,Company_Info,Question".split(","))
writer.writerows(results)
out.close()


# In[37]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:


# In[5]:


get_ipython().system("pip3 install beautifulsoup4")


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
