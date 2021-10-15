/***************************************************

  PROGRAMA: 08062021

  Trazador de curvas para un transistor BJT/MOSFET utilizando DACs

  Este programa se ejecuta en conjunto con:

  ARDUINO: ARDUINO AR 65.ino (entradas) 08062021-A
  PYTHON:  Completo AR 65.py  (monitor) 08062021-P
  
  TARJETA UTILIZADA: Arduino UNO
  TRANSISTORES DE PRUEBA: BC547B y 2N7000
  CONVERTIDORES DIGITALES ANALOGICOS UTILIZADOS: PCF8591
                 
  8 / junio / 2021
  
*****************************************************/

/**
 * ---------------------------------------------------------------------------------------------------------
 * PCF_Vbb -> controla el voltaje Vbb del trazador de curvas
 * PCF_Vcc -> controla el voltaje Vcc del trazador de curvas
 * ---------------------------------------------------------------------------------------------------------
 */
#include "Wire.h"
#define PCF_Vbb 0x48 // I2C bus address
#define PCF_Vcc 0x49 // I2C bus address

// **************************************************************
//     SELECCION DE TRANSISTOR:
//      'true' <- BJT     BC547B
//      'false' <- MOSFET 2N7000
// **************************************************************
 boolean Transistor = true;
// **************************************************************

// **************************************************************
//     SELECCION DE MUESTRAS CON ó SIN 'Filtrado Circular'
//      'true' <- CON Filtrado || circular de 4 muestras
//      'false' <- SIN Filtrado
// **************************************************************
 boolean Filtrado_Circular = true;
// **************************************************************

/**
 * ---------------------------------------------------------------------------------------------------------
 * Declaracion de arreglos:
 * canales_medidos[4] -> son los voltajes analogicos medidos directamente del Arduino [0,1023]
 * voltajes[4] -> son los voltajes escalados del arreglo anterior [0,5]
 * corrientes[2] -> son las corrientes calculadas como la diferencia del arreglo de voltajes anterior
 * ---------------------------------------------------------------------------------------------------------
 */
const int numero_entradas_analogicas = 4;
int canales_medidos[numero_entradas_analogicas];
double voltajes[numero_entradas_analogicas];
double corrientes[2];

/**
 * ---------------------------------------------------------------------------------------------------------
 *   Definicion de variables para el cálculo del FILTRO CIRCULAR (Promediador)
 *   Este filtro permite promediar cada lectura analogica de arduino mediante un filtro circular
 *   buffer_promediador[bufferSize]
 *   bufferSize = tamaño del buffer
 * ---------------------------------------------------------------------------------------------------------
 */
 const int bufferSize = 32;  // Numero de muestras a promediar
 int promedios_calculados[numero_entradas_analogicas];
 int buffer_promediador[numero_entradas_analogicas][bufferSize];
 int index[numero_entradas_analogicas];
 int canales[numero_entradas_analogicas];

/**
 * ---------------------------------------------------------------------------------------------------------
 * Definicion de pines para los 4 canales del ADC
 * PinVbb -> Es el voltaje a la salida del PCF_Vbb
 * PinVcc -> Es el voltaje a la salida del PCF_Vcc
 * PinVbe -> Es el voltaje en base-emisor del transistor BJT
 * PinVce -> Es el voltaje en colector-emisor del transistor BJT
 * 
 * NOTA: Entre Vbb y Vbe hay una resistencia Rb de 100 Kohm (valor nominal)
 *       Entre Vcc y Vce hay una resistencia Rc de 470 ohm (valor nominal)
 * ---------------------------------------------------------------------------------------------------------     
 */
const int PinVbb = A0;  // Pin de entrada analogica canal 0
const int PinVbe = A1;  // Pin de entrada analogica canal 1
const int PinVcc = A2;  // Pin de entrada analogica canal 2
const int PinVce = A3;  // Pin de entrada analogica canal 3

/**
 * ---------------------------------------------------------------------------------------------------------
 * Variables para el control del tiempo de muestreo
 * lastime -> guarda el ultimo instante de tiempo en el que enviaron datos por el puerto serie
 * sampleTime -> duracion entre cada muestra tomada
 * numMuestras -> numero de muestras tomadas por cada curva
 * 
 * Por lo tanto, la frecuencia de cada conjunto de muestras es de 2Hz (numMuestras x sampleTime)/1000
 * ---------------------------------------------------------------------------------------------------------
 */
unsigned long lastTime = 0;
unsigned long sampleTime = 100;
const double numMuestras = 50;

/**
 * ---------------------------------------------------------------------------------------------------------
 * Vcc -> valor medido de la fuente de voltaje que se utiliza como alimentacion del trazador de curvas
 * Vth -> valor observado experimentalmente de la curva Id vs Vbe en donde se observa que comienza a crecer 
 *        el voltaje Vbe con respecto a la corriente Ic (voltaje de umbral)
 * Resistencia usadas, valor nominal y valor medido:
 * Rd = 220 ohm  -> 224 ohm
 * Rg = 100 Kohm  -> 101.1 Kohm
 * ---------------------------------------------------------------------------------------------------------
 */
const double Vcc=5.0;
const double Vth=1.8;

/**
 * ---------------------------------------------------------------------------------------------------------
 * i_muestra -> Indica el numero de la muestra que se toma. Para cada conjunto de muestras, puede variar 
 *              entre [0,numMuestras]
 * numero_curva -> Indica la curva de la cual se toman muestras. Las curvas con numero_curva = 0 hasta 3, 
 *                 se utilizan para graficar Id vs Vce. La curva con numero_curva = 4 se utiliza para 
 *                 graficar las demas curvas
 * barrido_recta -> Realiza un barrido con un numero de muestras igual a numMuestras para cada curva medida
 * voltaje_obtencion_curva -> Valor de voltaje propuesto Vcc en formato hexadecimal para las curvas id vs Vce. 
 *                            Posteriormente, este mismo valor es Vbb para las demas curvas
 * ---------------------------------------------------------------------------------------------------------
 */
int i_muestra=0;
int numero_curva=0;
byte barrido_recta;
byte voltaje_obtencion_curva = 0x74;


/**
 * Inicializa tanto la comunicacion serial como la comunicacion I2C para comunicarse con los dos PCF8591
 * 
 */
void setup() {
  Wire.begin();
  // --- Inicializa velocidad de transmision serial ---
  Serial.begin(9600);

  // --- Sincronizacion de comunicacion serial ---
  Serial.println("inicio");
}


/**
 * Se miden cinco curvas para graficar Id vs Vce. Posteriormente se toma una ultima curva para graficar las demas curvas
 * 
 */
void loop() {
  // --- Toma muestras cada sampleTime ms ---
  if (millis()-lastTime > sampleTime) {
    
    lastTime = millis(); // Actualiza el tiempo de la ultima vez que se tomaron muestras

    if(numero_curva<5) // ¿Se toman muestras de las primeras 5 curvas para Id vs Vce?
    {
      int valor;
      if (Transistor)
      {
        // --- 5 Curvas para Ic vs Vce [BJT] ---    
        valor = map(numero_curva,0,5,50,250);
      } else {
        // --- 5 Curvas para Id vs Vds [MOSFET] ---    
        valor = map(numero_curva,0,5,100,140);
      }
      
      establecer_voltaje_Vbb(valor);
      barrer_voltaje_Vcc();
    }
    else if(numero_curva==5)
    {
      // --- 1 Curva para Ib vs Vbe , Ic vs Vbe , entre otras --- 
      // --- 1 Curva para Ig vs Vgs , Id vs Vgs ---
      establecer_voltaje_Vcc(250);
      barrer_voltaje_Vbb();
    }
    else
    {
      numero_curva = 0;
    }
  }
}

void barrer_voltaje_Vcc(){
  // --- Barre durante 50 muestras ---
  for (int i_muestra=0; i_muestra<250; i_muestra+=5){
    establecer_voltaje_Vcc(i_muestra);
    procesar_enviar_muestras();
  }
  numero_curva++; // Indica que se tomaran muestras de la siguiente curva
}

void barrer_voltaje_Vbb(){
  if (Transistor)
  {
    // --- Transistor BJT: Valores de VBB desde 0 hasta 5V aprox. ---
    for (int i_muestra=0; i_muestra<250; i_muestra+=5){
      establecer_voltaje_Vbb(i_muestra);
      procesar_enviar_muestras();
    }
  } else {
    // --- Transostor MOSFET: valores de VGG mayores a Vth ---
    for (int i_muestra=0; i_muestra<150; i_muestra+=3){
      establecer_voltaje_Vbb(i_muestra);
      procesar_enviar_muestras();
    }
  }

  numero_curva++; // Indica que se tomaran muestras de la siguiente curva
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

void establecer_voltaje_Vbb(int valor){
  Wire.beginTransmission(PCF_Vbb); // wake up PCF_Vbb
  Wire.write(0x40); // control byte - turn on DAC (binary 1000000)
  Wire.write(valor);
  Wire.endTransmission(); // end tranmission
}

/**
 * Ac un valor de voltaje a Vcc en el PCF8591 correspondiente
 * @param valor -> Es un numero en formato hexadecimal [0,255] que representa un voltaje [0,5V]
 * 
 */
void establecer_voltaje_Vcc(int valor){
  Wire.beginTransmission(PCF_Vcc); // wake up PCF_Vcc
  Wire.write(0x40); // control byte - turn on DAC (binary 1000000)
  Wire.write(valor);
  Wire.endTransmission(); // end tranmission
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
      canales_medidos[0] = analogRead(PinVbb); // Vbb
      canales_medidos[1] = analogRead(PinVbe); // Vbe
      canales_medidos[2] = analogRead(PinVcc); // Vcc
      canales_medidos[3] = analogRead(PinVce); // Vce
  
      // Filtrado circular en cada lectura. SIN mezclar muestras en tiempos diferentes
      agregar_lecturas_buffer(canales_medidos);
      promediador_lecturas_circular(canales_medidos);
    }
  } else {
    // --- SIN FILTRADO CIRCULAR ---
    canales_medidos[0] = analogRead(PinVbb); // Vbb
    canales_medidos[1] = analogRead(PinVbe); // Vbe
    canales_medidos[2] = analogRead(PinVcc); // Vcc
    canales_medidos[3] = analogRead(PinVce); // Vce

    for(int j=0; j<4; j++)
    {
      canales[j] = canales_medidos[j];
    }
  }
}

/**
 * Escala los 4 canales de voltaje, que varian entre [0,1023] a un numero que representa el voltaje [0,5]
 * 
 */
void escalar_canales(double Vcc_ref)
{
  voltajes[0] = scaling(canales[0], 0, 1023, 0, Vcc_ref);  // Vbb
  voltajes[1] = scaling(canales[1], 0, 1023, 0, Vcc_ref);  // Vbe
  voltajes[2] = scaling(canales[2], 0, 1023, 0, Vcc_ref);  // Vcc
  voltajes[3] = scaling(canales[3], 0, 1023, 0, Vcc_ref);  // Vce
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
  corrientes[0] = (voltajes[0]-voltajes[1])/0.1;  // Rb = 0.1 MOhms, Ib en uA
  corrientes[1] = (voltajes[2]-voltajes[3])/0.1;  // Rc = 0.1 KOhms, Ic en mA
}

/**
 * Envia todos los datos por el puerto serial
 * En orden, se envian: [Vbb,Vbe,Ig,Vcc,Vce,Id]
 * 
 */
void enviar_datos_seriales()
{
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
void agregar_lecturas_buffer(int canales_medidos[])
{
  for(int i=0; i<numero_entradas_analogicas; i++)
  {
    buffer_promediador[i][index[i]] = canales_medidos[i];
    index[i] += 1;
    if (index[i] >= bufferSize) index[i] = 0;
  }
}

// --- Filtro circular: promediador ---
void promediador_lecturas_circular(int canales_medidos[])
{
  for(int i=0; i<numero_entradas_analogicas; i++)
  {
    long sum = 0;
    for (int k=0; k<bufferSize; k++)
    {
      sum += buffer_promediador[i][k];
    }
    canales[i] = (int)(sum/bufferSize);
  }
}
