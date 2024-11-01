const int sensorPin = A0;  // Pino do sensor de umidade
const int relePin = 7;     // Pino do relé da bomba

void setup() {
    Serial.begin(9600);     // Inicia a comunicação serial
    pinMode(relePin, OUTPUT); // Define o pino do relé como saída
}

void loop() {
    int umidade = analogRead(sensorPin); // Lê o valor do sensor
    Serial.println(umidade); // Envia o valor para o Python

    // Controla a bomba
    if (umidade < 500) {
        digitalWrite(relePin, HIGH); // Ativa a bomba
    } else {
        digitalWrite(relePin, LOW);  // Desativa a bomba
    }
    
    delay(5000); // Espera 5 segundos antes de ler novamente
}
