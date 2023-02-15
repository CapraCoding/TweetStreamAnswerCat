import tweepy
import requests
from urllib.request import Request
import config
import urllib.request

#Configurando chaves API Twitter
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

#Fazendo Autenticação
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

import threading

#Recarregar API's
def reloadapi_cat():
    url = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(url)
    images = response.json()

    #Configurando Request na API
    req = Request(
        url=images[0]['url'],
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    #Criando a imagem temporária
    with urllib.request.urlopen(req) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())
            f.close()

    #Pegando imagem temporaria
    path_img = 'temp.jpg'
    media = api.media_upload(filename=path_img)

    return media.media_id

def reloadapi_KW():
    response2 = requests.get('https://api.kanye.rest')
    kfrase = response2.json()
    quote = kfrase['quote'] + ' - Kanye West'
    return quote

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):
    def on_status(self, status):
        #Rodando def para atualizar API de frases e Imagens
        Imagem_Tweet = reloadapi_cat()
        frase = reloadapi_KW()

        #Coletando tweet
        tweets = status.text
        id_tweet = status.id


        #Printando frase da API
        print(frase)
        print(tweets)

        #Respondendo Tweet
        api.update_status(status=frase, in_reply_to_status_id=id_tweet,
                                              auto_populate_reply_metadata=True, media_ids=[Imagem_Tweet])
        print('Respondido')


#Instancia a subclasse para visualiar
printer = IDPrinter(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

# Filtra de qual usuário realizar o stream
printer.filter(follow=['10842792'])



