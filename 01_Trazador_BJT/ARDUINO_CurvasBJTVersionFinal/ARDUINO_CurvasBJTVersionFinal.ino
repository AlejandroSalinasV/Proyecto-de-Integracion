/***************************************************

  PROGRAMA: 22062021

  Trazador de curvas para un transistor BJT utilizando potenciometros digitales 9XC103

  Este programa se ejecuta en conjunto con:

  ARDUINO: CurvasBJTVersionFinal.ino (entradas) 22062021-A
  PYTHON:  main.py, de carpeta "Completo AR 65 BJT"
  
  TARJETA UTILIZADA: Arduino UNO
  TRANSISTORES DE PRUEBA: BC547B 
  POTENCIOMETROS DIGITALES: 9XC103
                 
  22 / junio / 2021
  
*****************************************************/


// **************************************************************
//     SELECCION DE MUESTRAS CON ó SIN 'Filtrado Circular'
//      'true' <- CON Filtrado || circular de 32 muestras
//      'false' <- SIN Filtrado
// **************************************************************
 boolean Filtrado_Circular = true;
// **************************************************************

//*****Pines de lectura Analógicos **********************************
/*
 * A0 -> Pin conectado entre pot 2 y resistencia de 4.7 K
 * A1 -> Pin conectado a la base del transistor
 * A2 -> Pin conectado al colector del transitor
 * A3 -> Pin conectado entre el pot 1 y resistencia de 100 ohms
 */
int pin_canal[] = {A0, A1,A2, A3};
const int entradas_analogicas = sizeof(pin_canal)/sizeof(int);
int canales[entradas_analogicas]; //variable para guardar valores de lectura de canales [0,1023]

//********** arreglos donde guardaremos lecturas **********

double voltajes[entradas_analogicas]; //Voltaje: Vbb, Vbe, Vce, Vcc
double corrientes[2]; // coriente: ic & ib

/**
 * ---------------------------------------------------------------------------------------------------------
 *   Definicion de variables para el cálculo del FILTRO CIRCULAR (Promediador)
 *   Este filtro permite promediar cada lectura analogica de arduino mediante un filtro circular
 *   buffer_promediador[bufferSize]
 *   bufferSize = tamaño del buffer
 * ---------------------------------------------------------------------------------------------------------
 */
 const int bufferSize = 32;  // Numero de muestras a promediar
 int promedios_calculados[entradas_analogicas];
 int buffer_promediador[entradas_analogicas][bufferSize];
 int index[entradas_analogicas];
 int canalesBuffer[entradas_analogicas];
 
//******************************************************************************


/*
 * ---------------------------------------------------------------------------------------------------------
 * CONSIDERACIONES DE POTENCIOMETROS
 * POTENCIOMETRO 2 -> controla las variaciones del voltaje Vbb del trazador de curvas
 * POTENCIOMETRO 1 -> controla las variaciones del voltaje Vce del trazador de curvas
 * ---------------------------------------------------------------------------------------------------------
 */
//******Pines de control para potenciometros digital ****************
//orden de pines {pot1, pot2}
const int incPin[2] = {2,8}; // increment input 
const int udPin[2]  = {3,9}; //Up/Down input
const int csPin[2] = {4,10}; //Chip select input

/*
 * Pines para el manipular tensiones de potenciometro digital 2**
 * Se utiliza el concepto de tierra virtual, para generar variaciones
 * de voltaje de 0v-2.5v & de 2.5v - 5v. 
 * Rango dinamico medido: [0.0489V - 4.6041V]
 */
const int volt1 = 5; //pin conectado al extremo del resistor de 4.7k
const int volt2 = 6; // pin conectado en pot digital, en la terminal: Vh/Rh



//******************* Otras variables *****************************

float Resistor_base= 33030.00;// resistencia que se coloca en la base del transistor
float Resistor_colector = 100.60; // resistencia de colector, que se coloca en serie con el potenciometro 1
//float Resistor = 4650.00; //Resistencia en serie con pot2, proporciona Vth

int const Vth[] = {15,20,25,30,35}; // proporciona los voltajes de base Vbb para la obtencion de curvas ic, 
                                    // modificando el valor del pot 2. [rango 1-100]
                                    
int t = sizeof(Vth)/sizeof(int);//tamaño del arreglo Vth
const int muestras = 50; // cantidad de muestras para cada medición 
const double Vcc=5.0; // voltaje de referencia que se obtiene del arduino. 

/**
 * ---------------------------------------------------------------------------------------------------------
 * numero_curva -> Indica la curva de la cual se toman muestras. Las curvas con numero_curva = 0 hasta 3, 
 *                 se utilizan para graficar Id vs Vce. La curva con numero_curva = 4 se utiliza para 
 *                 graficar las demas curvas
 * ---------------------------------------------------------------------------------------------------------
 */
int numero_curva=0;

void setup() {
  
  // --- Inicializa velocidad de transmision serial ---
  Serial.begin(9600);

  // --- Sincronizacion de comunicacion serial ---
  delay(5);
  Serial.println("");
  Serial.println("inicio");
  delay(5);
  //********Nota: Los pines analogicos no es necesario declararlos****************
  //ya que estos pines solo actuan de entrada, input
  
  //***********Pines para variaciones de Vth*****************************
    pinMode(volt1, OUTPUT);
    pinMode(volt2, OUTPUT);

    
  //*********Pot digital Pines********************
  for (int i = 0; i<2; i++){
    pinMode(incPin[i], OUTPUT);
    pinMode(udPin[i],  OUTPUT);
    pinMode(csPin[i],  OUTPUT);
    digitalWrite(csPin[i], HIGH); // se encuentra en stand by current
  }     
  reset(true, true); // regresamos el pot 1 & 2 al valor minimo
  delay(10);   
  
}


/**
 * Se miden cinco curvas para graficar Ic vs Vce. 
 * Posteriormente se toma una ultima medición para graficar las demas curvas Ib vs Ic ....
 * 
 */
void loop() {      
    
    if(numero_curva<5) // Se toman muestras de las primeras 5 curvas para Ic vs Vce
    {           
      VariarVoltajeTh(Vth[numero_curva]); // variar voltajes en base del transistor
      barrer_voltaje_Vcc(); // obtención de variaciones de ic
      delay(20);
      numero_curva ++; 
    }
    else if(numero_curva==5)
    {     
      barrer_voltaje_Vbb(); // variaciones de voltaje de base del transistor
      delay(20);
      numero_curva++;
    }    
  
}

void barrer_voltaje_Vcc(){       
    int contador_local = 0;            
    reset(true,false); // reseteamos el pot 1, el cual esta en el colector del transistor
     
      while(contador_local< muestras){ // realizar las 50 mediciones  para las curvas de Ic 
        // --- Lectura y Escalamiento de canales e impresion ---       
        procesar_enviar_muestras();
        up(true, false);//aumenta contador del pot, Variaciones de voltaje de colector          
        delay(5);
        contador_local++;  
      }    
}


void barrer_voltaje_Vbb(){    
    int contador_local = 0;
    int fijo = 25; //Establecemos una resistencia de colector fija    
    
    reset(true,true); //reiniciamos pot's
    for (int i = 0; i < fijo; i++){ // ponemos una resistencia de colector fija
      up(true,false);      
    }
    
    while(contador_local < muestras ){
        // --- Lectura y Escalamiento de canales ---
        VariarVoltajeTh(contador_local * 2); // variar voltaje de la base. 
        delay(2);
        procesar_enviar_muestras();
        contador_local++;           
    }   
}


void procesar_enviar_muestras(){
  // --- Lecura de los canales ---
    lectura_canales(); // Lee los 4 voltajes del circuito
    
    // --- Escalamiento de canales ---
    escalar_canales(Vcc); // Escala los 4 voltajes leidos al voltaje de alimentacion Vcc
    
    // -- calculo de corrientes
    calcular_corrientes(); // Calcula las corrientes con los voltajes escalados
    
    // --- Transmision de cada valor al programa en Python ---
    enviar_datos_seriales(); // Envia los 4 voltajes escalador y las 2 corrientes calculadas
}



/**
 * Lee los 4 voltajes del circuito. [Vbb,Vbe,Vcc,Vce]
 * 
 */
void lectura_canales()
{
  if (Filtrado_Circular)
  {
     // --- CON FILTRADO CIRCULAR con buffer circular de 32 muestras ---
    for (int b=0; b<bufferSize; b++)
    {
      for (int i = 0; i <entradas_analogicas; i++ )      
        canales[i] = analogRead(pin_canal[i]);  // Vbb, Vbe, Vcc, Vce  
      // Filtrado circular en cada lectura. SIN mezclar muestras en tiempos diferentes
      agregar_lecturas_buffer(canales);
      promediador_lecturas_circular(canales);
    }
  } else {
    // --- SIN FILTRADO CIRCULAR ---
    for (int i = 0; i <entradas_analogicas; i++ )      
        canalesBuffer[i] = analogRead(pin_canal[i]);  // Vbb, Vbe, Vcc, Vce 
  }
}

/**
 * Escala los 4 canales de voltaje, que varian entre [0,1023] a un numero que representa el voltaje [0,5]
 * 
 */
void escalar_canales(double Vcc_ref)
{
  voltajes[0] = scaling(canalesBuffer[0], 0, 1023, 0, Vcc_ref);  // Vbb
  voltajes[1] = scaling(canalesBuffer[1], 0, 1023, 0, Vcc_ref);  // Vbe
  voltajes[2] = scaling(canalesBuffer[2], 0, 1023, 0, Vcc_ref);  // Vcc
  voltajes[3] = scaling(canalesBuffer[3], 0, 1023, 0, Vcc_ref);  // Vce
}

/**
 * Calcula las corrientes con los valores de voltaje escalados [Ig,Id]
 * NOTA: Las corrientes Ig e Id no estan escaladas al valor medido de las resistencias Rg y Rd. 
 *       Solo son una diferencia de voltajes. Ig = Vbb - Vbe
 *                                            Id = Vcc - Vce
 * 
 */
void calcular_corrientes()
{
  corrientes[0] = (voltajes[0]-voltajes[1])/Resistor_base;  // Corriente ib
  corrientes[0] = corrientes[0] * 1000000.00 ; // corriente ib en Microampers
  
  corrientes[1] = (voltajes[3]-voltajes[2])/Resistor_colector;  // Corriente ic
  corrientes[1] = corrientes[1] * 1000.00; // corriente ic en microampers
}

/**
 * Envia todos los datos por el puerto serial
 * En orden, se envian: [Vbb,Vbe,Ib,Vcc,Vce,Ic]
 * 
 */
void enviar_datos_seriales()
{
  /* DEPURACION Y ANALISIS DE DATOS
  Serial.print(voltajes[0],4);    // VBB
  Serial.print("\t"); 
  Serial.print(voltajes[1],4);    // Vbe
   Serial.print("\t");
  Serial.print(corrientes[0],4);  // Ib
   Serial.print("\t");
  Serial.print(voltajes[2],4);    // VCC
   Serial.print("\t");
  Serial.print(voltajes[3],4);    // Vce
   Serial.print("\t");
  Serial.print(corrientes[1],4);  // Ic
   Serial.print("\n");
   */
  Serial.println(voltajes[0],4);    // VBB
  Serial.println(voltajes[1],4);    // Vbe
  Serial.println(corrientes[0],4);  // Ib
  Serial.println(voltajes[2],4);    // VCC
  Serial.println(voltajes[3],4);    // Vce
  Serial.println(corrientes[1],4);  // Ic
   
}

/**
 * Escala valores que se sabe que varian entre un intervalo definido [in_min,in_max] a otro intervalo [out_min,out_max]
 * @param x -> es el valor a escalar
 * @param in_min -> es el valor minimo que puede tomar x
 * @param in_max -> es el valor maximo que puede tomar x
 * @param out_min -> es el valor minimo al cual se escala x
 * @param out_max -> es el valor maximo al cual se escala x
 * 
 */
float scaling(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min;
}

// *******************************************************************
//
//  FILTRO CIRCULA (promediador) con buffer de 32 muetars 
//
// *******************************************************************
// --- Inicializacion del buffer ---
void agregar_lecturas_buffer(int canales[])
{
  for(int i=0; i<entradas_analogicas; i++)
  {
    buffer_promediador[i][index[i]] = canales[i];
    index[i] += 1;
    if (index[i] >= bufferSize) 
      index[i] = 0;
  }
}

// --- Filtro circular: promediador ---
void promediador_lecturas_circular(int canales[])
{
  for(int i=0; i<entradas_analogicas; i++)
  {
    long sum = 0;
    for (int k=0; k<bufferSize; k++)
    {
      sum += buffer_promediador[i][k];
    }
    canalesBuffer[i] = (int)(sum/bufferSize);
  }
}

//*************CONTROL DEL POTENCIOMETRO DIGITAL*************************
/*
 * AUMENTA EL VALOR DEL POTENCIOMETRO, HACIENDO QUE TENGA EL VALOR SIGUIENTE
 */
void up(bool pot1, bool pot2){//SIGUIENTE VALOR RESISTIVO
  
  if (pot1 == true){ // Aumentamos el valor de resistencia en el pot 1      
      digitalWrite(udPin[0], HIGH);
      digitalWrite(incPin[0], HIGH); // generar pulso de bajada, to down
      digitalWrite(csPin[0], LOW);  
    
      //Generamos pulso de bajada
      digitalWrite(incPin[0], LOW);
      delayMicroseconds(3);
      digitalWrite(incPin[0], HIGH); // regresamos el flanco 
      delayMicroseconds(3);
      
      digitalWrite(csPin[0], HIGH); //regresamos a stand by current 
      
  }

    if (pot2 == true){  // Aumentamos el valor de resistencia en el pot 2        
      digitalWrite(udPin[1], HIGH);
      digitalWrite(incPin[1], HIGH); // generar pulso de bajada, to down
      digitalWrite(csPin[1], LOW);  
    
      //Generamos pulso de bajada
      digitalWrite(incPin[1], LOW);
      delayMicroseconds(3);
      digitalWrite(incPin[1], HIGH); // regresamos el flanco 
      delayMicroseconds(3);
      
      digitalWrite(csPin[1], HIGH); //regresamos a stand by current 
       
  }   
}
 /********************************************************************************************
 * DISMINUYE EL VALOR DEL POTENCIOMETRO, HACIENDO QUE TENGA EL VALOR ANTERIOR
 ********************************************************************************************/

void down(bool pot1, bool pot2){ //ANTERIOR VALOR RESISTIVO
  
  if (pot1 == true){// Disminuismos el valor de resistencia en el pot 1   
      //inicializamos la cuenta ascendente
      digitalWrite(udPin[0], LOW);
      digitalWrite(incPin[0], HIGH); // generar pulso de bajada, to down
      digitalWrite(csPin[0], LOW);  
    
      //Generamos pulso de bajada
      digitalWrite(incPin[0], LOW);
      delayMicroseconds(3);
      digitalWrite(incPin[0], HIGH); // regresamos el flanco 
      delayMicroseconds(3);
      
      digitalWrite(csPin[0], HIGH); //regresamos a stand by current
        
  }
  
  if (pot2 == true){ // Disminuismos el valor de resistencia en el pot 2 
      //inicializamos la cuenta ascendente
      digitalWrite(udPin[1], LOW);
      digitalWrite(incPin[1], HIGH); // generar pulso de bajada, to down
      digitalWrite(csPin[1], LOW);  
    
      //Generamos pulso de bajada
      digitalWrite(incPin[1], LOW);
      delayMicroseconds(3);
      digitalWrite(incPin[1], HIGH); // regresamos el flanco 
      delayMicroseconds(3);
      
      digitalWrite(csPin[1], HIGH); //regresamos a stand by current
        
  }
}
 /********************************************************************************************
 * La funcion reset() vuelve nuestro potenciometro al valor mas bajo resistivo
 * el valor oscila aproximadamente entre 40 ohms 
 ********************************************************************************************/
void reset(bool pot1, bool pot2){ // REGRESA EL POT AL VALOR MINIMO
  if (pot1 == true)  { // reseteamos al valor mas bajo el pot 1
    for(int i = 0; i<100; i++)
      down(true, false);
    
  }
  if (pot2 == true){// reseteamos al valor mas bajo el pot 2
    for(int i = 0; i<50; i++)
      down(false, true );    
  }
}

 /********************************************************************************************
 * Variacion de voltaje en la base, con la funcion VariarVoltajeTh().
 * Se pueden generar 100 variaciones en la base del transistor debido a que se tienen 
 * 100 steps resistivos. 
 * 
 * Con el diseño proporcionado se pueden hacer variciones de aprox 0 a 5 V 
 * Rango dinamico medido: [0.0489V - 4.6041V]
 ********************************************************************************************/

void VariarVoltajeTh(int variacion){ // variacion 1 -> 100, [1-100]
  //GENERAREMOS LOS DIFERENTES DE BASE DEL TRANSISTOR
 
  reset(false, true);//pot1=false, pot2=true

  if (variacion < 51 ){
    voltaje_down(); // establecemos margen de 0 a 2.5 V pines digitales resistencias
    for (int i = 0; i < (variacion)-1; i++)
      up(false, true); //pot1=false, pot2=true
  } else {
      voltaje_up(); // establecemos margen de 2.5 a 5.0 V pines digitales resistencias
      for (int i = 0; i < 50; i++)
        up(false, true); //pot1=false, pot2=true // resistencia a valor maximo 
      for (int i = 0; i < (variacion)-51; i++)
        down(false, true); //pot1=false, pot2=true
    }
    
    delay(1); //Estabilizar señal
}
/*********************************************************************************************
 * voltaje_down() función que permite establecer las variaciones de 
 * 0 a 2.5 V, utilizada en  funcion VariarVoltajeTh
 ********************************************************************************************/
void voltaje_down()
{
  //Para variaciones de 0 a 2.5 volts
  digitalWrite(volt1, HIGH);
  digitalWrite(volt2, LOW);  
}
/*********************************************************************************************
 * voltaje_down() función que permite establecer las variaciones de 
 * 2.5 a 5 V, utilizada en  funcion VariarVoltajeTh
 ********************************************************************************************/
void voltaje_up()
{
  //Para variaciones de 2.5 a 5 volts
  digitalWrite(volt1, LOW);
  digitalWrite(volt2, HIGH);  
}
