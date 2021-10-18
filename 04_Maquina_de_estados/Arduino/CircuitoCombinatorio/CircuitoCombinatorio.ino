/*
 *12-08-2021
 *PROGRAMA PARA OBTENER LOS ESTADOS COMBINATORIOS DE UN CIRCUITO DIGITAL
 *SE REALIZARA EL MUESTREO PARA UN CIRCUITO DE 4 ENTRADAS Y UNA SALIDA
 
 */

int entrada []= {2,3,4,5};
int salida = 13;
int retardo = 10;
bool medicion = true;

String estados[16] = {"0000", "0001", "0010", "0011",
                      "0100", "0101", "0110", "0111",
                      "1000", "1001", "1010", "1011",
                      "1100", "1101", "1110", "1111",};
                      
void setup() {
  for(int i = 0; i<4;i++){
    pinMode(entrada[i], OUTPUT);  
  }
  pinMode(salida,INPUT);
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("inicio");
  for (int j = 0; j < 4; j++){
    digitalWrite(entrada[j],LOW);
  
  }
}

void loop() {
  while (medicion){
    for (int i = 0; i < 16; i++){ 
     for (int j = 0; j < 4; j++){
       if ( ( (i >> j) & 1 )  == 1 )
           digitalWrite(entrada[j], HIGH);
       else 
        digitalWrite(entrada[j], LOW);
     }
     if (digitalRead(salida) == HIGH) {
        Serial.println("1");
      }
      else{
        Serial.println("0");
      }
     //Serial.println(estados[i]);
     Serial.println(i);
     delay(retardo);
    }
    medicion = false;
  }
   
  if (medicion == false){
    for (int j = 0; j < 4; j++){
      digitalWrite(entrada[j],LOW);
  
  }
  }
}
