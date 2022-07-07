import requests
from bs4 import BeautifulSoup as bs
from pyrogram import Client
from pyrogram import enums
from time import sleep

app = Client("maccount")

def eachpage(page_url):
  response = requests.get("https://1337x.to"+page_url)
  soup = bs(response.text, 'html.parser')
  info = soup.find_all('a', href=True)
  magnet = info[31]['href']
  info = soup.find_all('title')
  title = info[0].text[9:len(info[0].text)-16]
  #print(title)
  info = soup.find_all('p')
  try:
    plot = info[2].text[info[2].text.index("Overview")+10:len(info[3].text)-1]
  except:
    try:
      plot1 = info[21].text
      plot2 = info[16].text
      plot = plot1 if (len(plot1)>len(plot2)) else plot2
    except:
      plot = info[3].text[info[3].text.index("Overview")+10:len(info[3].text)-1]
  #print(plot)
  try:
    rating = info[2].text[info[2].text.index("IMDb"):info[2].text.index("Rotten")-3]
  except:
    rating1 = info[5].text
    rating2 = info[4].text
    if "Rotten" in rating1:
      rating1 = info[5].text[info[5].text.index("IMDb"):info[5].text.index("Rotten")-3]
    if "Rotten" in rating2:
      rating2 = info[5].text[info[5].text.index("IMDb"):info[5].text.index("Rotten")-3]
    rating = rating1 if (len(rating1)>len(rating2)) else rating2
    if "IMDb" not in rating:
      try:
        rating = info[3].text[info[3].text.index("IMDb"):info[3].text.index("Rotten")-3]
      except:
        rating = info[3].text[info[3].text.index("IMDb"):info[3].text.index("Meta")-3]
  #print(rating)
  try:
    genres = info[2].text[info[2].text.index("Genres")+7:info[2].text.index("Director")]
  except:
    try:
      genres = info[2].text[info[2].text.index("Genres")+7:info[2].text.index("Actor")]
    except:  
      genres1 = info[9].text
      genres2 = info[8].text
      genres = genres1 if len(genres1)>len(genres2) else genres2
      if "Genre" not in info[2].text:
        try:
          genres = info[3].text[info[3].text.index("Genre")+6:info[3].text.index("Director")].strip()
        except:
          pass
  #print(genres)
  info = soup.find_all('span')
  size = info[15].text
  if "GB" not in size:
    size = info[14].text
  #print(size)
  #print(magnet)

  message = title+"\n\n<i>"+plot+"</i>\n\n"+genres+"\n\n"+rating+"\n\n"+size+"\n\n<code>"+magnet+"</code>"
  async def main():
      async with app:
          await app.send_message(-1001764381179, message, parse_mode=enums.ParseMode.HTML)
  app.run(main())

user_url = "/user/QxR/"
response = requests.get("https://1337x.to"+user_url)
soup = bs(response.text, "html.parser")
info = soup.find_all('a', href=True)
previous_links = []
new_links = []
#uncomment this to not send current links when the bot starts
#for i in info: 
#  if 'HEVC' in i['href']: previous_links+=[i['href']]
#print(previous_links)
#for i in previous_links: print(i)
while True:
  response = requests.get("https://1337x.to"+user_url)
  soup = bs(response.text, 'html.parser')
  info = soup.find_all('a', href=True)
  for i in info: 
    if 'HEVC' in i['href']: new_links+=[i['href']]
  for i in reversed(new_links):
    if i not in previous_links:
      print("Sending message of "+i)
      eachpage(i)
    else:
      pass
  previous_links = new_links
  print("Sleeping for 10 minutes now...")
  sleep(600)