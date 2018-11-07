
# coding: utf-8

# In[ ]:


#Eduardo Darrazão
#Rodrigo Faria


# In[1]:


import cv2
import numpy as np


# In[2]:


def detectaVerde(img, pattern, par):
    hsv = img.shape[2]
    altura = img.shape[0]
    largura = img.shape[1]
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([48, 65, 98])
    upper_green = np.array([80, 255, 255])
    
    # Seleciona apenas as cores dentro do range definido acima 
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.bitwise_not(mask)
    # recorta da imagem apenas os pixels brancos da mascara
    res = cv2.bitwise_and(img, img, mask = mask)
    
    #seleciona pixels de verde que nao sao do fundo e "desverdeia eles"
    res = desverdeia(res.copy(), par)
    #Pega a o retorno do recorte e cola em cima do background
    col = pasteIMG(pattern.copy(), res, mask)
    
    cv2.imwrite('resultados/frame' + str(par) +'.bmp',img)
    #cv2.imwrite('resultados/mask' + str(par) +'.bmp',mask)
    cv2.imwrite('resultados/res' + str(par) +'.bmp',res)
    cv2.imwrite('resultados/col' + str(par) + '.bmp', col)

    return 


# In[3]:


def pasteIMG(background, frame, mask):
    background = background[50:mask.shape[0]+50, 100:mask.shape[1]+100]
    
    for altura in range(mask.shape[0]):
        for largura in range(mask.shape[1]):
            if mask[altura][largura] == 255:
                try:
                    background[altura][largura][:] = frame[altura][largura][:]
                except:
                    continue
        
    return background


# In[4]:


def desverdeia(img, par):
    lower_green = np.array([40, 50, 20])
    upper_green = np.array([100, 255, 255])
    
    #Seleciona apenas as cores dentro do range definido acima
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.bitwise_not(mask)
    
    #escurece verdes que nao sao fundo
    for altura in range(img.shape[0]):
        for largura in range(img.shape[1]):
            if mask[altura][largura]==0:
                hsv[altura][largura][1] /= 5
                hsv[altura][largura][2] /= 1.2
         
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite('resultados/mask' + str(par) +'.bmp',mask)
                
    return img 


# In[5]:


img1 = cv2.imread("img/1.bmp", cv2.COLOR_BGR2HSV)
img2 = cv2.imread("img/2.bmp", cv2.COLOR_BGR2HSV)
img3 = cv2.imread("img/3.bmp", cv2.COLOR_BGR2HSV)
img4 = cv2.imread("img/4.bmp", cv2.COLOR_BGR2HSV)
img5 = cv2.imread("img/5.bmp", cv2.COLOR_BGR2HSV)
img6 = cv2.imread("img/6.bmp", cv2.COLOR_BGR2HSV)
img7 = cv2.imread("img/7.bmp", cv2.COLOR_BGR2HSV)
img8 = cv2.imread("img/8.bmp", cv2.COLOR_BGR2HSV)

pattern = cv2.imread("pattern.bmp")

detectaVerde(img1, pattern, 1)
detectaVerde(img2, pattern, 2)
detectaVerde(img3, pattern, 3)
detectaVerde(img4, pattern, 4)
detectaVerde(img5, pattern, 5)
detectaVerde(img6, pattern, 6)
detectaVerde(img7, pattern, 7)
detectaVerde(img8, pattern, 8)

