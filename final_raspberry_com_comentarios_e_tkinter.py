#bibliotecas/library
import tkinter as tk                                        #tkinter já vem no raspberry pi-tkinter already comes with raspberry pi
import time                                                 #tempo, chama para prover atrasos/time, calling for time to provide delays in program
import math                                                 #bibliteca matematica/math library
from PIL import ImageTk, Image                              #biblioteca pillow/pillow library
#letra no desenho da imagem é arialblack 170/letter used in the draw is arialblack 170
from smbus import SMBus                                     #usado para i2c/used for i2c

import RPi.GPIO as GPIO                                     #usado para um rele especial/used for special relay
GPIO.setwarnings(False)                                     #desativa notificações do gpio/disables notifications of gpio



addr = 0x8                                                  #endereço de envio i2c/ bus address i2c
bus = SMBus(1)                                              #indica /dev/ic2-1/ indicates /dev/ic2-1
z=0
#--------------------------------------------------------
#funções/functions
def inicial():                                              #configura a primeira configuração/set up the first position
    enviadados(Estados_zero)                                #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino
    GPIO.setmode(GPIO.BCM)                                  #ajusta portas/set doors
    GPIO.setup(17, GPIO.OUT)                                #ajusta porta 17 como saida/set door 17 as outpút
    GPIO.output(17, GPIO.HIGH)                              #liga porta 17/turn 17 door on
    time.sleep(2.0)                                         #tempo de delay/time of delay
    enviadados(Estado_reset)                                #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
    time.sleep(4.0)                                         #tempo de delay/time of delay
    enviadados(Estados_zero)                                #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino
        

def enviadados(estados):                                    #função que envia dados para o arduino/function that send data to arduino
    bus.write_byte(addr, 3)                                 #primeiro dado sendo um 3 para indicar o inicio do envio de dados/ first data being a 3 to indicate the start of sending data
    for a in estados:                                       #laço de repetição/looping
        bus.write_byte(addr, a)                             #envia bit por bit da estados/send bit by bit from "estados"


def chama_botoes(button):                                   #chama botões/call buttons
    Estados = []                                            #declara estados e zero locais/ local declaration of "estate" and "zero"
    Estados_zero = [0]*48
    if type(button)==int or type(button)==str:              #seleciona o botão quando é inteiro ou texto/select button when it is a integers or char
        action(button,0)                                    #chama função da ação com o botão selecionado/call "ação" function with the button selected
    else:                                                   #seleciona quando é uma lista/select when it is list
        cont = 0
        for x in button:                                    #percorre a lista/traveled the list
            cont+=1
            if x == 1:                                      #quando pressionado/when pressed
                    action(int(math.floor(cont/2)),1)       #chama a função ação quando o for numero inteiro/call the function action when the number is integers
                    if cont/2-math.floor(cont/2) != 0:      #chama quando não for inteiro/call when it is no integers
                        if cont!=1:
                            action(int(math.floor(cont/2)),0)#chama action/call action
    for x in Estados_das_portas:                            #separa as portas com duas saidas, uma saida e a luz/separate gate with one way out, two ways and light
        e=Estados_das_portas
        if e[x][3] == 'limpo':                              #uma saída, define se é um ou zero/one way out, defines if it is one or zero
            if e[x][1] == 0:
                Estados.append(0)
            else:
                Estados.append(1)
        elif e[x][3] == 'dois':                             #segunda porta, especial/second door, special
            if e[x][1] == 1:
                Estados[0]=0
                Estados[1]=0
                Estados.append(1)
                Estados_das_portas['a2'][1] = 0
            else:
                Estados.append(0)
        elif e[x][3] == 'luz':                              #comando da luz/light command
            if e[x][1] == 1:
                Estados.insert(3, 1)
                Estados_zero[3]=1
            else:
                Estados.insert(3, 0)
                Estados_zero[3]=0
        else:                                               #duas saídas, define se é um ou zero/two way out, defines if it is one or zero
            if e[x][1] == e[x][2]:
                Estados.append(1)
                Estados.append(0)
            else:
                Estados.append(0)
                Estados.append(1)
                
    enviadados(Estados)                                     #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
    time.sleep(4.0)                                         #tempo de delay/time of delay
    enviadados(Estados_zero)                                #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino

    
def action(button, varios_comandos):                        #comanda a troca de imagens e estados/command the pictures and states change 
    try:                                                    #prevenção de erros/ error prevention
        if button == '':                                    #quando é valor digitado/when it is a value typed
            button = int(input_troca.get())-1
            input_troca.delete(0, 'end')                    #limpa input/clean input
        elif button =='luz_button':                         #botão da luz/light button
            if Estados_das_portas['a27'][1]==1:
                Estados_das_portas['a27'][1]=0
            else:
                Estados_das_portas['a27'][1]=1
        trocar = "a"+str(button+1)                          #para acessar valores no map/to acess value in the map
        if button == 1:                                     #configura imagem 1/set up figure 1
            butao_numero="pyimage"+str(1)                   
            imagem_numero=Estados_das_imagens[ butao_numero]
            btns[0].configure(image=imagem_numero)
            Estados_das_portas[trocar][1] = 1
        elif button > 18 and button < 24:                   #não trocam imagem/ dont change image
            print("Chama apenas o barulho nas portas")
        else:                                               #configura outras imagens, quando possuem mais de uma imagem
            butao_numero="pyimage"+str(2*button+1)          #set up the other images , when it has more then one picture
            butao_numero1= "pyimage"+str(2*button+2)
            imagem_numero=Estados_das_imagens[ butao_numero]#lê de um map com todas elas contidas/ read from a map with all of then
            imagem_numero1=Estados_das_imagens[ butao_numero1]
            if btns[button].cget('image') == butao_numero1 and varios_comandos==0:#configura para a aprimeira ou para a segunda imagem/ set to the first or to the second image
                btns[button].configure(image=imagem_numero1)
                Estados_das_portas[trocar][1] = Estados_das_portas[trocar][3]                
            else:
                btns[button].configure(image=imagem_numero)
                Estados_das_portas[trocar][1] = Estados_das_portas[trocar][2]
    except:                                                 #excessão, de quando pressionado o troca sem nada digitado/exception, when pressed to change without any type
        if button != "luz_button":
            print("algum botão errado")
            input_troca.delete(0, 'end')

            
#estados das portas ou imagens/states of gates and pictures
Estados_das_imagens={}
Estado_reset = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estado_a = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estado_b = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estado_c = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estado_d = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estado_e = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estado_f = [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Estados_zero = [0]*48

#organização dos estados das portas:                                    organization of port states:
                                    #quantidade de saidas                           amount of doors
                                    #porta que tá                                   last door
                                    #porta 1                                        door 1
                                    #porta 2                                        door 2
                                    #imagem 1                                       image 1
                                    #imagem 2                                       image 2
                                    #tamanho da imagem em x                         size of the image in x
                                    #tamanho da imagem em y                         size of the image in y
                                    #local do x                                     place in x
                                    #local do y                                     place in y
Estados_das_portas = {
    'a1': [2,0,0,1,"img/c1_1.png", "img/c1_2.png",40,45, 64, 549],
    'a2': [1,0,2,"dois","img/c2_1.png", "img/creta2.png",40,45, 150, 587],
    'a3': [2,4,4,5,"img/creta1.png", "img/creta2.png",409,11, 501, 533],
    'a4': [2,6,6,7,"img/creta1.png", "img/creta2.png",250,11, 107, 322],
    'a5': [2,8,8,9,"img/creta1.png", "img/creta2.png",250,11, 106, 277],
    'a6': [2,10,10,11,"img/creta1.png", "img/creta2.png",180,11, 123, 185],
    'a7': [2,12,12,13,"img/creta1.png", "img/creta2.png",409,11, 918, 582],
    'a8': [2,14,14,15,"img/c8_1.png", "img/c8_2.png",101,27, 270, 50],
    'a9': [2,16,16,17,"img/c9_1.png", "img/c9_2.png",85,44, 277, 90],
    'a10': [2,18,18,19,"img/c10_1.png", "img/c10_2.png",106,36, 271, 563],
    'a11': [2,20,20,21,"img/c11_1.png", "img/c11_2.png",99,27, 372, 82],
    'a12': [2,22,22,23,"img/c12_1.png", "img/c12_2.png",101,51, 352, 512],
    'a13': [2,24,24,25,"img/c13_1.png", "img/c13_2.png",98,55, 401, 290],
    'a14': [2,26,26,27,"img/c14_1.png", "img/c14_2.png",101,54, 518, 285],
    'a15': [2,28,28,29,"img/c15_1.png", "img/c15_2.png",91,47, 638, 309],
    'a16': [2,30,30,31,"img/c16_1.png", "img/c16_2.png",95,58, 735, 293],
    'a17': [2,32,32,33,"img/c18_1.png", "img/c18_2.png",1,1,1,1],
    'a18': [2,34,34,35,"img/c18_1.png", "img/c18_2.png",91,50, 1220, 85],
    'a19': [2,36,36,37,"img/c19_1.png", "img/c19_2.png",101,42, 1210, 512],
    'a20': [1,0,38,"limpo","img/c20_1.png", "img/creta2.png",54,36, 215, 343],
    'a21': [1,0,39,"limpo","img/c21_1.png", "img/creta2.png",54,36, 215, 237],
    'a22': [1,0,40,"limpo","img/c22_1.png", "img/creta2.png",54,36, 452, 210],
    'a23' : [1,0,41,"limpo"],
    'a24' : [2,42,42,43],
    'a25' : [2,44,44,45],
    'a26' : [2,46,46,47],
    'a27' : [1,0,3,"luz"],
    }

#--------------------------------------------------------
# GUI
window = tk.Tk()                                            #inicia o tkinter/tkinter start
window.geometry("990x690+0+36")                             #geometria do tkinter/tkinter geometry
window.title("Sala de comando")                             #nome da tela/screen name
#iniciar.state("zoomed")
#iniciar.iconbitmap("img/trem_ico.ico")


imagem_fundo = Image.open("img/totalcnum.png")              #imagem fundo/background image
fundo_redimencionado =  imagem_fundo.resize((990, 520), Image.ANTIALIAS)#redimensionamento/resize
img_fundo = ImageTk.PhotoImage(fundo_redimencionado)        #ajustando imagem para mostrar ao usuario/ajusting image to show to the user

while z == 0:                                               #chama ao iniciar a configuração case/call the on start up the set up base
    inicial()
    z=1

#--------------------------------------------------------
# widgets
container = tk.Frame(window)                                #cria um conteinar/create an container 
container2 = tk.Frame(window)
fundo_de_troca = tk.Label(container,                        #label da imagem grande de fundo/label of the big picture of background
                       image=img_fundo,
                       bg="white",
                       bd=1,
                       relief="solid",
                       font="Verdana 42 bold")

btn_nr = -1
btns = []
contagem=0
for x in Estados_das_portas:                                #adiciona a um map as imagens do Estados_das_portas que podem ser adicionadas aos botões
                                                            #adds to a map images from Estados_das_portas that could be add to the button 
    try:
        e=Estados_das_portas
        
        image_aberta1 = Image.open(e[x][4])                 #abre imagem/open image
        imagem_redimecionada1 =  image_aberta1.resize((round(e[x][6]*0.62),round(e[x][7]*0.81)), Image.ANTIALIAS)#redimenciona/resize
        imagem_tk1 = ImageTk.PhotoImage(imagem_redimecionada1)#ajustando imagem para mostrar ao usuario/ajusting image to show to the user
        contagem=contagem+1
        variavel = "pyimage"+str(contagem)
        Estados_das_imagens[variavel] = imagem_tk1          #salva em um map de imagens/saves in a map of pictures
        
        image_aberta2 = Image.open(e[x][5])                 #abre imagem/open image
        imagem_redimecionada2 =  image_aberta2.resize((round(e[x][6]*0.62),round(e[x][7]*0.81)), Image.ANTIALIAS)#redimenciona/resize
        imagem_tk2 = ImageTk.PhotoImage(imagem_redimecionada2)#ajustando imagem para mostrar ao usuario/ajusting image to show to the user
        contagem=contagem+1
        variavel = "pyimage"+str(contagem)
        Estados_das_imagens[variavel] = imagem_tk2          #salva em um map de imagens/saves in a map of pictures
    except:                                                 #quando não tem a imagem deixa zerado/when it does not have an image leaves it zeroed
        contagem=contagem+1
        imagem_tk2 = 0
        variavel = "pyimage"+str(contagem)
        Estados_das_imagens[variavel] = imagem_tk2
        
        contagem=contagem+1
        imagem_tk2 = 0
        variavel = "pyimage"+str(contagem)
        Estados_das_imagens[variavel] = imagem_tk2
        
contagem1=0
contagem2=0
for x in Estados_das_portas:                                #vai criar um botão para o usuario para cada porta declarada em Estados_das_portas
                                                            #it create a button for the user from every state declareded in Estados_das_portas
        e=Estados_das_portas
        
        variavel = "pyimage"+str(2*contagem1+1)
        imagem_numero=Estados_das_imagens[variavel]
        if imagem_numero != 0:                              #se a possuir imagem ele cria/if it has an picture it create
            variavel = "pyimage"+str(2*contagem2+1)
            imagem_numero=Estados_das_imagens[variavel]
            btn_nr += 1
            btns.append(tk.Button(image=imagem_numero, command=lambda x=btn_nr: chama_botoes(x)))#salva em um vetor de botoes/ saves it in a vector of buttons
            btns[btn_nr].place(x=round(e[x][8]*0.62) , y=round(e[x][9]*0.81))#define posição dos botões/ define possition of th buttons
        else:
            btns.append(0)
        contagem2+=1
        contagem1+=1


espera = tk.Label(container,                                #espaço/space
                  text='',
                  padx=10,
                  pady=10,
                  bd=1,
                  font="Verdana 1 bold")
input_troca = tk.Entry(container, font = "Arial 25 bold")   #entrada de texto/text input    
trocar = tk.Button(container,                               #botão troca/ button "troca"
                text= 'Trocar',
                font = "Arial 20 bold",
                command= lambda x=input_troca.get(): chama_botoes('')
                )
reset = tk.Button(container,                                #botão reset/ button reset
               text= 'Reset',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_reset),
               fg="red")
luz = tk.Button(container,                                  #botão luz/button light
               text= 'Luz',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes("luz_button"),
               fg="blue")
a = tk.Button(container2,                                   #botão a/button a
               text= 'A',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_a),
               )
b = tk.Button(container2,                                   #botão b/button b
               text= 'B',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_b),
               )
c = tk.Button(container2,                                   #botão c/button c
               text= 'C',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_c),
               )
d = tk.Button(container2,                                   #botão d/button d
               text= 'D',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_d),
               )
e = tk.Button(container2,                                   #botão e/button e
               text= 'E',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_e),
               )
f = tk.Button(container2,                                   #botão f/button f
               text= 'F',
               font = "Arial 20 bold",
               command= lambda x=input_troca.get(): chama_botoes(Estado_f),
               )




texto_troca = tk.Label(container,                           #label texto troca/label text change
                       text = "Troca:",
                       padx=10,
                       pady=10,
                       font = "Arial 20 bold",)

#--------------------------------------------------------
# layout                                                    #modo de exibição ao usuario/ way of exhibition to the user 
fundo_de_troca.grid(row=0, columnspan=6)
espera.grid(row=1, columnspan=6)

texto_troca.grid(row=2, column = 0)
input_troca.grid(row=2, column = 1)
trocar.grid(row=2,column =2)
reset.grid(row=2,column =3)
luz.grid(row=2,column =4)
espera.grid(row=3, columnspan=6)
a.grid(row=0,column =0)
b.grid(row=0,column =1)
c.grid(row=0,column =2)
d.grid(row=0,column =3)
e.grid(row=0,column =4)
f.grid(row=0,column =5)

container.pack()                                            #mostra container/shows container
container2.pack()

window.mainloop()                                           #mantem a tela em loop/keep screen on loop

#estados == state
#troca == change
#luz == light

