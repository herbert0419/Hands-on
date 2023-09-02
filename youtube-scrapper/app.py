from bs4 import BeautifulSoup
import requests
url =   "https://www.youtube.com/user/krishnaik06/videos"

# Step1 : Get the HTML
r = requests.get(url)
htmlContent = r.content
# print(htmlContent)

# Step2: Parse the HTML
soup = BeautifulSoup(htmlContent,'html.parser')
# print(soup)

# Step3:

titles = soup.title
print(titles)

paras = soup.find_all('div')
print(paras)

paras = soup.find('div').get_text
print(paras)

# subscribers = soup.find_all('span',class_='style-scope ytd-grid-video-renderer')
# print(subscribers)




