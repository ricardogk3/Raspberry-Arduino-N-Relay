import time                                                 #tempo, chama para prover atrasos/time, calling for time to provide delays in program
from smbus import SMBus                                     #usado para i2c/used for i2c


addr = 0x8                                                  #endereço de envio i2c/ bus address i2c
bus = SMBus(1)                                              #indica /dev/ic2-1/ indicates /dev/ic2-1


def enviadados(estados):                                    #função que envia dados para o arduino/function that send data to arduino
    bus.write_byte(addr, 3)                                 #primeiro dado sendo um 3 para indicar o inicio do envio de dados/ first data being a 3 to indicate the start of sending data
    print(estados)
    for a in estados:                                       #laço de repetição/looping
        bus.write_byte(addr, a)                             #envia bit por bit da estados/send bit by bit from "estados"

#estados das portas/states of gates     
estadozero = [0]*48
estadoreset = [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
estado = [0]*48

#organização dos estados das portas:                                    organization of port states:
                                    #quantidade de saidas                           amount of doors
                                    #porta que tá                                   last door
                                    #porta 1                                        door 1
                                    #porta 2                                        door 2
Porta = {
    'a1' : [2,0,0,1],
    'a2' : [1,0,2],
    'luz' : [1,0,3],
    'a3' : [2,4,4,5],
    'a4' : [2,6,6,7],
    'a5' : [2,8,8,9],
    'a6' : [2,10,10,11],
    'a7' : [2,12,12,13],
    'a8' : [2,14,14,15],
    'a9' : [2,16,16,17],
    'a10' : [2,18,18,19],
    'a11' : [2,20,20,21],
    'a12' : [2,22,22,23],
    'a13' : [2,24,24,25],
    'a14' : [2,26,26,27],
    'a15' : [2,28,28,29],
    'a17' : [2,32,32,33],
    'a18' : [2,34,34,35],
    'a19' : [2,36,36,37],
    'a20' : [1,0,38],
    'a21' : [1,0,39],
    'a22' : [1,0,40],
    'a23' : [1,0,41],
    'a24' : [2,42,42,43],
    'a25' : [2,44,44,45],
    'a26' : [2,46,46,47]
    
}

#configura a primeira configuração/set up the first position
enviadados(estadozero)                                      #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino
time.sleep(2.0)                                             #tempo de delay/time of delay
enviadados(estadoreset)                                     #chama a função para enviar os estados reset ao arduino/call functio to send the states reset to arduino
time.sleep(2.0)                                             #tempo de delay/time of delay
estado[3] = 1                                               #atribui a porta 3(luz) ligado/assigns door 3 as on
enviadados(estado)                                          #chama a função para enviar os estados ao arduino/call functio to send the states to arduino

        
while 1:                                                    #executa um loop eterno/execute loop forever
    try:                                                    #tenta rodar, caso contrario espera 10 segundos e tenta novamente/try to run it, in case it didnt run it will wait for 10 seconds
        trocar = input("Escolha a posição a trocar:").lower()#lê dados de entrada para rodar/ reads data in to run it
        if trocar == 'luz':                                 #se for luz/ if it is light
            if Porta['luz'][1] == 0:                        #se a luz estiver desligada/if the light it is off
                Porta['luz'][1] = 1                         #liga a luz/turn the light on
                estado[3] = 0                               #atribui a porta 3(luz) ligado/assigns door 3 as on
                enviadados(estado)                          #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino
                
            else:                                           #se a luz estiver ligada/if the light it is on
                Porta['luz'][1] = 0                         #desliga a luz/turn the light off
                estado[3] = 1                               #atribui a porta 3(luz) desligado/assigns door 3 as off  
                enviadados(estado)                          #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino                          
                
        elif trocar == 'reset':                             #chama para o estado original/ call it for the original state
            enviadados(estadoreset)                         #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
            time.sleep(2.0)                                 #tempo de delay/time of delay
            estado[3] = 1                                   #atribui a porta 3(luz) ligado/assigns door 3 as on
            enviadados(estado)                              #chama a função para enviar os estados zerados ao arduino/call functio to send the states zeroed to arduino
            
        elif trocar == 'a':                                 #estado pre programado/ preprogrammed state
            veta = [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            veta[3] = estado[3]                             #atribui a porta 3(luz) ligado ou desligado/assigns door 3 as on or off
            enviadados(veta)                                #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
            time.sleep(2.0)                                 #tempo de delay/time of delay
            enviadados(estado)                              #chama a função para enviar os estados ao arduino/call functio to send the states to arduino

        elif trocar.isnumeric():                            #se numérico/if it is numeric
            if int(trocar) > 0 and int(trocar) < 20 and int(trocar) != 2 or int(trocar) > 23 and int(trocar) < 27:
                                                            #define intervalo de 1 a 19, diferente de 2, maior que 23 e menor que 27/defines interval from 1 to 19, different of 2, bigger then 23 ans smaller then 27                                                
                trocar = 'a' + trocar                       #salva com a para "a" leitura do map/ save with "a" for read the map
                if Porta[trocar][1] == Porta[trocar][2]:    #se a porta estiver em um sentido troca para o outro/ if the door it is in one way change to the other
                    Porta[trocar][1] = Porta[trocar][3]     #salva o novo estado/saves the new state
                    estado[Porta[trocar][3]] = 1            #indica a porta a trocar/indicates the door to change
                    enviadados(estado))                     #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                    time.sleep(2.0)                         #tempo de delay/time of delay
                    estado[Porta[trocar][3]] = 0            #volta porta ao original/turn the door back to the original
                    enviadados(estado))                     #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                else:
                    Porta[trocar][1] = Porta[trocar][2]
                    estado[Porta[trocar][2]] = 1            #indica a porta a trocar/indicates the door to change
                    enviadados(estado))                     #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                    time.sleep(2.0)                         #tempo de delay/time of delay
                    estado[Porta[trocar][2]] = 0            #volta porta ao original/turn the door back to the original
                    enviadados(estado))                     #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                
            elif int(trocar) >= 20 and int(trocar) <= 23:   #se for maior ou igual a 20 e menor ou igual a 23/if it is equall or bigger then 20 or equal or smaller then 23
                num = int(trocar)                           #transforma em inteiro/ transform in interger
                trocar = 'a' + trocar                       #salva com a para "a" leitura do map/ save with "a" for read the map
                estado[Porta[trocar][2]] = 1                #indica a porta a trocar/indicates the door to change
                enviadados(estado))                         #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                time.sleep(2.0)                             #tempo de delay/time of delay
                estado[Porta[trocar][2]] = 0                #volta porta ao original/turn the door back to the original
                enviadados(estado))                         #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                
            elif int(trocar) == 2:                          #se igual a dois/if it is equal 2
                num = int(trocar)                           #transforma em inteiro/ transform in interger
                trocar = 'a' + trocar                       #salva com a para "a" leitura do map/ save with "a" for read the map
                estado[2] = 1                               #indica a porta a trocar/indicates the door to change
                enviadados(estado)                          #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                time.sleep(2.0)                             #tempo de delay/time of delay
                estado[2] = 0                               #volta porta ao original/turn the door back to the original
                enviadados(estado)                          #chama a função para enviar os estados ao arduino/call functio to send the states to arduino
                
    except:                                                 #espera 10 segundos na falha/wait for 10 seconds on case of fail
        time.sleep(10.0)                                    #tempo de delay/time of delay

 


        
