/***************************************************
 ************LECTURA DE DATOS***********************

  Adaptado de: https://www.youtube.com/watch?v=8YEvU2Zi_LU

 **************MEDIDOR DE FRECUENCIA******************
 Frequency timer
 Author: Nick Gammon
 Date: 10th February 2012
 https://forum.arduino.cc/t/medir-frecuencias/263804/7
 Input: Pin D2
  
*****************************************************/

//----------VARIABLES DE CONTROL--------------------
volatile boolean first;
volatile boolean triggered;
volatile unsigned long overflowCount;
volatile unsigned long startTime;
volatile unsigned long finishTime;
unsigned long elapsedTime;
float freq;
float periodo; // periodo de la señal senoidal
int index = -1; 
float sum_fq = 0; 
boolean Medicion = true; // si Medicion = true -> toma el periodo del 555
                         // si Medicion = false -> toma el periodo del
                         // es necesario cambiar el pin D2, dependiendo la medición a realizar 
//----------------------------------------------------


// --- Definicion del pin para el canal del ADC ---
const int PinCanal0 = A0;  // Pin de entrada analogica canal 0


// -----------------------------------------------------------
//  Declaracion de Variables de lectura:
//  canales -> valor analógico leido en el canal
//  voltaje -> voltaje escalado de los valores analógicos   
//            escalamiento(analogicos: 0,1023 -> voltajes: 0,5)
// -----------------------------------------------------------
int   canal;//array
float voltajes[16]; //array
float voltaje;
int indice = 0; 

String estados[16] = {"0000", "0001", "0010", "0011",
                      "0100", "0101", "0110", "0111",
                      "1000", "1001", "1010", "1011",
                      "1100", "1101", "1110", "1111",};

// --- Variables para control tiempo de muestreo ---
unsigned long lastTime = 0;
float sampleTime; //referencia a las muestras por segundo, en milisegundos 

void setup() {
  // --- Inicializa velocidad de transmision serial ---
  Serial.begin(9600);
  delay(70);
  // --- Sincronizacion de comunicacion serial ---
  
//*****************************************************
// -----------PARAMETROS PARA FREQUENCY COUNTER--------
//*****************************************************
    // reset Timer 1
  TCCR1A = 0;
  TCCR1B = 0;
  // Timer 1 - interrupt on overflow
  TIMSK1 = bit (TOIE1);   // enable Timer1 Interrupt
  // zero it
  TCNT1 = 0;  
  overflowCount = 0;  
  // start Timer 1
  TCCR1B =  bit (CS10);  //  no prescaling

  // set up for interrupts
  prepareForInterrupts ();    
  Frecuencia();
  sampleTime = periodo *1000 / 16.0;
}
bool habilitar_impresion = false;
void loop() {
  
  // --- Toma muestras cada periodo_senoidal/16 ---
  if (millis()-lastTime > int(sampleTime)) {
    lastTime = millis();    
    // --- Lecura de los canales ---
    canal = analogRead(PinCanal0);    
    // --- Escalamiento de canales ---
    voltaje = scaling(canal, 0, 1023, 0, 5);    
    // --- Transmision de cada valor al programa en Python ---
    if (voltaje < 0.10) // comienza la impresión desde el estado 0. 
      habilitar_impresion= true;
    
    if (habilitar_impresion == true){      
      voltajes[indice] = voltaje;      
      indice ++;
    }

   if (indice == 16){
      Serial.println("inicio");
      int i = 0;
      int p=0;    
      while(true){
        Serial.println(voltajes[i]);
        Serial.println(sum_fq);
        Serial.println(p*sampleTime*0.001);
        //Serial.println(estados[i]);
        p++;
        i ++;
        if(i == 16)
          i=0;
      }
    }

  }

}

/***********************************************
 --------FUNCIONES PARA FRECUENCIA--------------
 ********************************************/
// here on rising edge
void isr (){
  unsigned int counter = TCNT1;  // quickly save it
  
  // wait until we noticed last one
  if (triggered)
    return;

  if (first)
    {
    startTime = (overflowCount << 16) + counter;
    first = false;
    return;  
    }
    
  finishTime = (overflowCount << 16) + counter;
  triggered = true;
  detachInterrupt(0);   
}  // end of isr

// timer overflows (every 65536 counts)
ISR (TIMER1_OVF_vect){
  overflowCount++;
}  // end of TIMER1_OVF_vect

void prepareForInterrupts(){
  // get ready for next time
  EIFR = bit (INTF0);  // clear flag for interrupt 0
  first = true;
  triggered = false;  // re-arm for next time
  attachInterrupt(0, isr, RISING);     
}  // end of prepareForInterrupts

void DetectarFrecuencia(){
  if (!triggered)
    return;
     
  elapsedTime = finishTime - startTime;
  freq = F_CPU / float (elapsedTime);  // each tick is 62.5 nS at 16 MHz
  prepareForInterrupts (); 
  index ++;
   
}

void Frecuencia(){
  float fq[6];   
  int index_pasado;
/*
 * MEDICION == TRUE 
 * PARA REALIZAR LA MEDIFICION DE FRECUENCIA DEL CLK 
 * QUE ALIMENTA LA SEÑAL DE RELOJ DEL 4015, ES DECIR,
 * FRECUENCIA DEL 555
 */
  while (Medicion == true){  
    index_pasado = index;   
    DetectarFrecuencia();
    
    if (index!= index_pasado){
      fq[index] = freq;
      sum_fq += freq;     
    }
    if (index == 5){
      sum_fq= sum_fq / 6.0; // divido entre la cantidad de muestras
      sum_fq = sum_fq/16.0; // la frecuencia de cada cambio de estado es 1/16 
      periodo = 1.0/ sum_fq;   
      break;
    }
  }

/*
 * Medicion == false 
 * Para realizar la medicion de la frecuencia de la señal
 * senoidal generada por 4015
 */
  
    while (Medicion == false){  
    index_pasado = index;   
    DetectarFrecuencia();    
    if (index!= index_pasado){      
      sum_fq = freq;     
    }
    if (index == 0){ 
      periodo = 1.0/ sum_fq;           
      break;
    }
  }
  
  return;
}
/***********************************************
 --------FUNCION DE ESCALAMIENTO----------------
 ********************************************/
float scaling(float x, float in_min, float in_max, float out_min, float out_max){
  return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}
