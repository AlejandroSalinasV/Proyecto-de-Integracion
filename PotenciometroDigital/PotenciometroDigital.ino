/*
 * PROGRAMA PARA LA CARACTERIZACION DE UN POT DIGITAL X9C103.
 * EN ESTE PROGRAMA SOLO SE RECURRE A LOS DIFERENTES VALORES
 * DEL POT DIGITAL DE UNA MANERA CONSECUTIVA
 * 
 * ALEJANDRO SALINAS V. 
 */
// pines de control del pot digital
int incPin = 2; // increment input 
int udPin = 3; // Up/Down input
int csPin = 4; // Chip select input 

// otra configuracion de pines 
//int incPin = 8; // increment input 
//int udPin =  9; // Up/Down input
//int csPin =  10; // Chip select input 

int contador = 0;
void setup() {
  Serial.begin(9600);
  pinMode(incPin, OUTPUT);
  pinMode(udPin, OUTPUT);
  pinMode(csPin, OUTPUT);
  digitalWrite(csPin, HIGH); // se encuentra en stand by current   
  reset();
}

void loop() {  
  
  if (Serial.available() > 0) {
    char  Dato = Serial.read();
    Serial.println(Dato);
    if(Dato == 'U'){ 
      up();
      contador ++;
      Serial.println("Incrementamos [" + String(contador) + "]" );
    } // if U

    if(Dato == 'D'){ 
      down();
      Serial.println("Disminuinos");  
      contador --;   
    } // if D

    
 }// if serial

// Barrido automatico. 
  for(int i = 0; i < 100; i++){
     delay(5000);
      up();
      contador ++;
      Serial.println("Incrementamos [" + String(contador) + "]" );
     
  }

}// llave loop

void up(){
  //Incremento wiper up
  digitalWrite(udPin, HIGH);
  digitalWrite(incPin, HIGH); // generar pulso de bajada, to down
  digitalWrite(csPin, LOW);  

  
  digitalWrite(incPin, LOW); // Generamos pulso de bajada (flanco to down)
  delayMicroseconds(3);
  digitalWrite(incPin, HIGH); // regresamos el flanco, store. 
  delayMicroseconds(3);
  
  digitalWrite(csPin, HIGH); // Store wiper position 7 & standby  current 
  
}

void down(){
  //Decremento wiper down
  digitalWrite(udPin, LOW);
  digitalWrite(incPin, HIGH); // generar pulso de bajada, to down
  digitalWrite(csPin, LOW);  

  
  digitalWrite(incPin, LOW); // Generamos pulso de bajada (flanco to down)
  delayMicroseconds(3);
  digitalWrite(incPin, HIGH); // regresamos el flanco, store. 
  delayMicroseconds(3);
  
  digitalWrite(csPin, HIGH); // Store wiper position 7 & standby  current 
}

// Reiniciamos el valor del pot mandandolo a la resistencia más baja
void reset(){
  int i = 0;
  for(i; i<100; i++)
    down(); 
}
