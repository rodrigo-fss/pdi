
# coding: utf-8

# In[1]:


import cv2
import time


# In[2]:


global NEGATIVO
global THRESHOLD
global ALTURA_MIN
global LARGURA_MIN
global N_PIXELS_MIN

NEGATIVO = 0
THRESHOLD = 200
ALTURA_MIN = 10
LARGURA_MIN = 10
N_PIXELS_MIN = 20


# In[3]:


def binariza (entrada, saida, threshold):
    for altura in range(entrada.shape[0]):
        for largura in range(entrada.shape[1]):
            if entrada[altura][largura] >= threshold:
                saida[altura][largura] = 255
            else:
                saida[altura][largura] = 0
    return saida


# In[4]:


def negativo(imagem):
    for linha in range(len(imagem)):
        for coluna in range(len(imagem[linha])):
            imagem[linha][coluna] = 255 - int(imagem[linha][coluna])
    return imagem


# In[5]:


class Rectangle:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


# In[6]:


class Component:
    def __init__(self, label, n_pixels, rect):
        self.label = label
        self.n_pixels = n_pixels
        self.rect = rect


# In[11]:


def rotula (entrada, componentes, largura_min, altura_min, n_pixels_min):
    label = 0.1
    #Inicia Lista de componentes
    componentes = []
    imagem=entrada.copy()
    
    for altura in range(entrada.shape[0]):
        for largura in range(entrada.shape[1]):
            #Se o pixel for branco
            if entrada[altura][largura] == 255:
                #Comece a inundação
                componente = inunda(label, entrada, altura, largura, 1, Rectangle(largura,largura,altura,altura))
                #Se o objeto inundado tiver mais pixels do que o numero minimo definido
                if componente != 0:
                    if componente.n_pixels >= n_pixels_min:
                        if (componente.rect.x_max - componente.rect.x_min) >= largura_min:
                            if(componente.rect.y_max - componente.rect.y_min) >= altura_min:
                                #Adicione ao lista de componentes e incremente a label
                                componentes.append(componente)
                                label = label+0.1
                                
    #printando todos os componentes encontrados
    for i in componentes:
        imagem = desenhaRetangulo(i, 1, imagem)
#        print 'Componente: ' + str(i.label).replace('.', '') + ' | Numero de pixels: ' + str(i.n_pixels)
#        print 'y min: ' + str(i.rect.y_min) + ' | y max: ' + str(i.rect.y_max)
#        print 'x min: ' + str(i.rect.x_min) + ' | x max: ' + str(i.rect.x_max)
    
    cv2.imwrite( "01 - retangularizada.bmp", imagem);
    return len(componentes)


# In[8]:


def inunda(label, entrada, x, y, ind, rect):
    n_pixels_cont = 1
    entrada[x][y] = label
    
    if y < rect.x_min:
        rect.x_min = y
    elif y > rect.x_max:
        rect.x_max = y
    
    if x < rect.y_min:
        rect.y_min = x
    elif x > rect.y_max:
        rect.y_max = x
    
    #Visite seu quatro vizinhos e verifique se fazem parte do objeto
    if entrada[x-1][y] == 255:
        #Se fizerem, prossiga com a inundação recursiva nessa direção
        n_pixels_cont = inunda(label, entrada, x-1, y, 0, rect) + 1
    if entrada[x][y-1] == 255:
        n_pixels_cont  = inunda(label, entrada, x, y-1, 0, rect) + 1
    if entrada[x+1][y] == 255:
        n_pixels_cont = inunda(label, entrada, x+1, y, 0, rect) + 1
    if entrada[x][y+1] == 255:
        n_pixels_cont  = inunda(label, entrada, x, y+1, 0, rect) + 1
    
    #A variavel ind verifica se estamos na primeira chamada do objeto, assim, se a inundação foi finalizada
    if ind == 1:
        #Se for, verifique se o numero de pixels do objeto é maior que o minimo definido
        if n_pixels_cont >= N_PIXELS_MIN:
            #Se for, crie um componente e retorne
            componente = Component(label, n_pixels_cont, rect)
            return componente
        else:
            return 0
    #Se não for a primeira chamada, retorne a contagem de pixels do objeto para ser incrementada com as outras chamadas
    else:
        return n_pixels_cont


# In[9]:


def desenhaRetangulo(componente, spread, img):
    y_max = componente.rect.y_max + spread
    y_min = componente.rect.y_min - spread
    x_max = componente.rect.x_max + spread
    x_min = componente.rect.x_min - spread
    for i in range(y_min, y_max+1):
        img[i][x_max] = 255
        img[i][x_min] = 255
    
    for i in range(x_min, x_max+1):
        img[y_min][i] = 255
        img[y_max][i] = 255
    
    return img


# In[10]:


##MAIN
image = cv2.imread("pacote2/arroz.bmp",0)

if image is None:
    print 'Erro ao abrir imagem.'
    print 'Verifique se a imagem está em: '
    print 'pacote2/arroz.bmp'
    exit()

if(NEGATIVO > 0):
    imagemBinarizada = negativo(imagemBinarizada)
    
imagemBinarizada = binariza(image, image, THRESHOLD)

#cv2.imwrite( "01 - binarizada.bmp", imagemBinarizada);

start = time.time()   
n_componentes = rotula(imagemBinarizada, 0, ALTURA_MIN, LARGURA_MIN, N_PIXELS_MIN)
end = time.time()
print '\nNumero total de componentes: ' + str(n_componentes)

print'Contagem de componentes executada em: ' + str('%.2f' % (end - start)) + ' segundos'

