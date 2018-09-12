
# coding: utf-8

# In[1]:


#Eduardo Darrazão
#Rodrigo Faria


# In[1]:


import cv2
import time
import math
import numpy as np

global JANELA
JANELA = 5


# In[2]:


def filtroIngenuo(img):
    imagem = img.copy()
    altura, largura, cor = img.shape[0], img.shape[1], img.shape[2]
    janela = int(JANELA/2)
    
    for k in range(cor):
        for y in range(janela, altura-janela):
            for x in range(janela, largura-janela):
                
                soma = 0
                for alturaJanela in range(y-janela, y+janela):
                    for larguraJanela in range(x-janela, x+janela):
                        soma += imagem[alturaJanela][larguraJanela][k]
                        
                img[y][x][k] = soma/np.power(janela*2, 2)
    return img


# In[3]:


def filtroSeparavel(img):
    imagem = img.copy()
    altura, largura, cor = img.shape[0], img.shape[1], img.shape[2]  
    janela = int(JANELA/2)
        
    for k in range(cor):
        for y in range(janela, altura - janela):
            for x in range(janela, largura - janela):
                
                soma = 0
                for larguraJanela in range(x-janela, x+janela):
                    soma+=imagem[y][larguraJanela][k]
                img[y][x][k] = soma/(janela*2)
                
    for k in range(cor):
        for y in range(janela, altura - janela):
            for x in range(janela, largura - janela):
            
                soma = 0
                for alturaJanela in range(y-janela, y+janela):
                    soma += img[alturaJanela][x][k]
                imagem[y][x][k] = soma/(janela*2)
    
    return imagem


# In[4]:


def filtroSeparavelAproveitando(img):
    imagem = img.copy()
    altura, largura, cor = img.shape[0], img.shape[1], img.shape[2]  
    janela = int(JANELA/2)
        
    for k in range(cor):
        for y in range(janela, altura - janela):
            ind = 0
            for x in range(janela, largura - janela):
                if ind == 0:
                    soma = 0
                    for larguraJanela in range(x-janela, x+janela):
                        soma+=imagem[y][larguraJanela][k]
                    ind = 1
                    
                else:
                    soma -= imagem[y][x-janela-1][k]
                    soma += imagem[y][x+janela-1][k]
                
                img[y][x][k] = soma/(janela*2)
                
    for k in range(cor):
        for x in range(janela, largura - janela):

            ind = 0
            for y in range(janela, altura - janela):
                if ind == 0:
                    soma = 0
                    for alturaJanela in range(y-janela, y+janela):
                        soma += img[alturaJanela][x][k] 
                    ind = 1
                else:
                    soma -= img[y-janela-1][x][k]
                    soma += img[y+janela-1][x][k]
                
                imagem[y][x][k] = soma/(janela*2)
                
                
    return imagem
   


# In[5]:


def imagemIntegral(imagem):
    altura, largura, cor = img.shape[0], img.shape[1], img.shape[2]
    
    for k in range(cor):
        indAltura = 1
        
        for y in range(altura):
            indLargura = 1
            
            for x in range(largura):
                if indLargura != 1 and indAltura != 1: 
                        imagem[y][x][k] += imagem[y-1][x][k]
                        imagem[y][x][k] += imagem[y][x-1][k]    
                        imagem[y][x][k] -= imagem[y-1][x-1][k]
                else:
                    if not(indLargura == 1 and indAltura == 1):
                        if indLargura!=1:
                             imagem[y][x][k] += imagem[y][x-1][k]
                        elif indAltura!=1:
                            imagem[y][x][k] += imagem[y-1][x][k]
                        
                indLargura = 0
                
            indAltura = 0
        
    return imagem

def mediaIntegral(img):
    imagem = img.copy()
    imagem = imagemIntegral(imagem)
    altura, largura, cor = img.shape[0], img.shape[1], img.shape[2]  
    janela = int(JANELA/2)
    
    for k in range(cor):
        for y in range(janela, altura - janela):
            for x in range(janela, largura - janela):
                sigma = imagem[y+janela][x+janela][k] + imagem[y-janela][x-janela][k]
                sigma -= imagem[y+janela][x-janela][k] + imagem[y-janela][x+janela][k]
                
                img[y][x][k] = sigma/np.power(janela*2, 2)
    return img
    


# In[6]:


##MAIN
try: 
    img = cv2.imread("lena.jpg", cv2.IMREAD_COLOR)
    img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
except:
    print('Erro ao abrir imagem')
    exit()    
    
start = time.time()   
ingenuo = filtroIngenuo(img)
end = time.time()

print ("Filtro Ingenuo: ", end-start)

cv2.imshow('image',ingenuo)
cv2.waitKey(0)
cv2.destroyAllWindows()

######################

start = time.time()   
separavel = filtroSeparavel(img)
end = time.time()

print("Filtro Separavel: ", end-start)

cv2.imshow('image',separavel)
cv2.waitKey(0)
cv2.destroyAllWindows()

######################

start = time.time()   
sepAproveitando = filtroSeparavelAproveitando(img)
end = time.time()

print("Filtro Separavel Aproveitando as Somas Anteriores: ", end-start)

cv2.imshow('image',sepAproveitando)
cv2.waitKey(0)
cv2.destroyAllWindows()

######################

start = time.time()   
integral = mediaIntegral(img)
end = time.time()

print ("Filtro integral: ", end-start)

cv2.imshow('image',integral)
cv2.waitKey(0)
cv2.destroyAllWindows()

