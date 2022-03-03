//bibliotecas/librarys
#include <Wire.h>                                         //biblioteca Wire para o I2C/ Wire library for I2C
#include <Vector.h>
#include <MultiShiftRegister.h>                           //biblioteca para um multiplas saidas mutáveis 74HC595N/ library for a multi shift register 74HC595N

//pinos de coneção/conection pin
const int latchPin = 8;
const int clockPin = 12;
const int dataPin = 11;

int numberOfRegisters = 6;                                //definição da quantidade de chips a serem usados, pino de trava, clock e dados/ definition of amount of chips used, latch pin, clock pin and data pin
MultiShiftRegister msr (numberOfRegisters , latchPin, clockPin, dataPin); 

int controle = 0;
int estado[48];

void setup() {                                            //configurações inicials/ inicial setups
  pinMode(latchPin, OUTPUT);                              //configura pinos como saidas//setup pins as output
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  
  Wire.begin(0x8);                                        // Configura o barramento I2C como escavo no endereço 8/ Join I2C bus as slave with address 8
                  
  Wire.onReceive(receiveEvent);                           // Quando recebe dados chama a função receiveEvent/Call receiveEvent when data received
}
 
void receiveEvent(int howMany) {                          // Função que executa quando qualquer dado for recebido/Function that executes whenever data is received from master
   
  while (Wire.available()) {                              // permanece ativo enquanto receber dados/remains active while it recives data
    double c = Wire.read();                               // lê o dado recebido/reads data input
    if(c == 3){                                           //primeiro dado/ first data
      controle = 0;
      }
    else if(controle < 48 && c!=3){                       // guarda valor em um vetor/ keeps value on a vector
      estado[controle]=c;
      controle = controle+1;  
      }
    
    if(controle == 48){                                   //quando o vetor estiver completo manda os dados para os 74HC595N/when the vector is full send then to the 74HC595N's
      for(int i = 0; i < 48; i++)
        {
          if(estado[i]== 0){                              //separa os 0 dos 1/separates 0 and 1
            msr.set_shift(i);
            }
          else{
            msr.clear_shift(i);
          }
        }
      } 
  }
}

void loop() {                                             //repete eternamente//repeats forever
  delay(100);
}


/*
  Arduino escravo para um Raspberry Pi mestre
  Arduino Slave for Raspberry Pi Master
  Conectados via I2C
  Connects via I2C

  I2C
  https://dronebotworkshop.com/i2c-arduino-raspberry-pi/

  MultiShiftRegister
  https://www.youtube.com/watch?v=cAT07gy4DII&list=PLyhTKvTGKcZewn_eqmkh8nqm4eIgToSXq&index=2
  https://www.youtube.com/watch?v=RjzmKYg66nM&list=PLyhTKvTGKcZewn_eqmkh8nqm4eIgToSXq&index=3
*/
