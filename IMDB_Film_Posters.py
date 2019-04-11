# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 21:36:28 2019

@author: S533488
"""

from bs4 import BeautifulSoup
import requests
class FilmDetails():
    
    def _init_(self):
        self.rank = ""
        self.movieName = ""
        self.yearReleased = ""
        self.link = ""
  
def get_film_list():
    getPage = requests.get('https://www.imdb.com/chart/top')
    getPage.raise_for_status()
    MoviesListPage = BeautifulSoup(getPage.text, 'html.parser')
    MoviesList = MoviesListPage.find('tbody',class_="lister-list")
    #print(playersList)
    movies_list = []
    for td in MoviesList.find_all('td',class_="titleColumn"):
        movieDetails=(td.text.strip().replace('\n','').replace('     ',''))
        rank = movieDetails.split('.')[0]
        movieName = movieDetails.split('.')[1].split('(')[0].lstrip()
        yearReleased = movieDetails.split('(')[1][:-1]
        link = td.find('a')

        
        obj  = FilmDetails()
        obj.rank = rank
        obj.movieName = movieName
        obj.yearReleased = yearReleased
        obj.link = link['href']
        
        movies_list.append(obj)
    return movies_list
    
film_list = get_film_list()
for list in film_list:
    print (list.movieName)
    print (list.rank)
    print (list.yearReleased)
    print (list.link)

    
def get_poster(film_list):
    for film in film_list:
        headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        page_url = "https://www.imdb.com/"+film.link
        getPage = requests.get(page_url, headers=headers)
        getPage.raise_for_status()
        MoviePage = BeautifulSoup(getPage.text, 'html.parser')
        poster_div = MoviePage.find('div',class_="poster")
        #print(poster_div)
    
        poster_link = poster_div.find('img')
        poster_image_link = poster_link['src']
        #print(poster_link['src'])
        imageLink = poster_image_link.split('@')[0] + "@._V1_.jpg"
        
        print(imageLink)
        
        imageDownload = open('{0}.jpg'.format(film.movieName.replace(':','')),'wb')
        imageDownload.write(requests.get(imageLink).content)
        imageDownload.close()

get_film_list()
get_poster(film_list)
    