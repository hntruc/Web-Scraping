import requests
from bs4 import BeautifulSoup
import json
import pandas

trailer, description, cate, cate_temp, review_temp, review, age_label, new_cate, name, rating, cast, temp, new_cast, link_img = [], [], [], [], [], [], [], [], [], [], [], [], [], []
link = ''
pos, i = 0, 0

page = requests.get('https://www.imdb.com/chart/top/?sort=ir,desc&mode=simple&page=1')
soup = BeautifulSoup(page.text, 'html.parser')

film_list = soup.find(class_='lister-list')

for film_name in film_list.find_all('a'):
    n = film_name.contents[0]
    if n != ' ' and i<100:
        name.append(n)
        i+=1
    elif i >= 100:
        i = 0
        break

#get_film_rating
for film_rating in film_list.find_all('strong'):
    if i < 100:
        rating.append(film_rating.contents[0])
        i+=1
    else:
        i = 0
        break

for film_name in film_list.find_all('a'):
    if film_name.contents[0] != ' ' and pos<100:
        URL = 'https://www.imdb.com'+film_name.get('href')
        new_page = requests.get(URL)
        soup = BeautifulSoup(new_page.content, 'html.parser')

        img_l = soup.find(class_='poster').img['src']
        link_img.append(img_l)

        film_cast = soup.find(class_=['cast_list','primary_photo'])

        for c in film_cast.find_all('img'):
            temp.append(c.get('title'))
        cast.append(temp)
        temp = []

        result = str(soup.find("script", type = "application/ld+json"))
        start_index = 0
        for i in range(len(result)):
            if result[i] == '{':
                start_index = i
                break
        string_result = result[start_index:]
        string_result = string_result[:-9]
        print(pos)
        #description
        a_film = json.loads(string_result)
        description.append(a_film['description'])

        #genre
        cate_temp = a_film['genre']
        cate.append(cate_temp)
        cate_temp = []

        #trailer
        if('trailer' in a_film.keys()):
            trailer.append('https://www.imdb.com'+a_film['trailer']['embedUrl'])
        else:
            trailer.append('')

        #age_label
        age_label.append(a_film['contentRating'])

        pos+=1
    elif pos>=100:
        break

for c in cate:
    if len(c) > 1 and type(c) != str:
        cates = ','.join(map(str, c)) 
    else:
        cates = c
    new_cate.append(cates) 

for c in cast:
    casts = ','.join(map(str, c)) 
    new_cast.append(casts)

film = pandas.DataFrame({
        "Name": name,
        "Description": description,
        "Genre": new_cate,
        "Rating": rating,
        "Trailer": trailer,
        "Age": age_label,
        "Casts": new_cast
})

film.to_csv('data.csv',index=True,header=True,encoding='utf-8-sig')

link = pandas.DataFrame(
    {
        "Name": name,
        "Image link": link_img
    }
)

link.to_csv('link_img.csv', index = True, header = True, encoding = 'utf-8-sig')