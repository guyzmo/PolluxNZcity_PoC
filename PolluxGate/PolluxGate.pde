/*
 * Arduino ENC28J60 Ethernet shield Polluxnzcity gateway
 * copyleft 2011 ckab, caused by guyzmo at hackable-devices dot org
 */

#include <EtherShield.h>

#define VW_MAX_MESSAGE_LEN 115
#include <VirtualWire.h>

// LES ADRESSES MAC ET IP DOIVENT ETRE UNIQUES DANS VOTRE RESEAU LOCAL

static uint8_t mymac[6] = {0xDE,0xAD,0xBE,0xEF,0xFE,0xED}; // ex : {0x12,0x34,0x56,0x78,0x90,0xab}
static uint8_t myip[4] = {192,168,42,42}; // ex : {192,168,0,35}

// ADRESSE IP DE VOTRE PASSERELLE (*-box)

static uint8_t gwip[4] = {192,168,42,1}; // ex : {192,168,0,1}


/**************************************************************************/
/**************************************************************************/

// Parametres de connexion serveur

//#define USE_DNS  

static uint8_t websrvip[4] = {192,168,42,1};
#define PORT 80                   // HTTP
#define HOSTNAME "demo.polluxnzcity.org"
#define WEBSERVER_VHOST "demo.polluxnzcity.org"

// etat de la connexion
static uint8_t resend=0; // donnees a envoyer
static int8_t dns_state=0; // obtention de la resolution DNS

// valeurs a transmettre
static char timestamp[15]; // date et heure
static char value[11];     // valeur mesuree
static char deviceid[37];  // identifiant equipement

// tampons de transmission
#define BUFFER_SIZE 400 // longeur maximale des requetes http
static uint8_t buf[BUFFER_SIZE+1];  //variable contenant la requete
static char tampon[108]; // variable contenant le message RF


// Chargement du pilote pour le shield reseau
EtherShield es=EtherShield();

#define RX_LED 4

// declaration des fonctions
void browserresult_callback(uint8_t,uint16_t);
int dns_resolution(int dat_p, int plen);

void setup(){
  Serial.begin(9600);
  Serial.print("setup:");

// initialisation communication radio
  vw_setup(1200); // vitesse en Bits par seconde
  vw_rx_start();    // demarrage recepteur
  vw_set_rx_pin(8); // modification du pin de reception (le pin par defaut etant le 11)

// initialisation communication reseau
  es.ES_enc28j60Init(mymac); // attribution de l'adresse MAC
  es.ES_init_ip_arp_udp_tcp(mymac,myip, PORT); // gestion de l'ARP et attribution adresse IP
  es.ES_client_set_gwip(gwip);  // configuration de la passerelle
  dns_state=2;

// initialisation LED
  pinMode(RX_LED, OUTPUT);

  Serial.println(" done");
  // blink led
  digitalWrite(RX_LED, HIGH); delay(50);
  digitalWrite(RX_LED, LOW);  delay(50);
  digitalWrite(RX_LED, HIGH); delay(50);
  digitalWrite(RX_LED, LOW);  delay(50);
  digitalWrite(RX_LED, HIGH); delay(50);
  digitalWrite(RX_LED, LOW);
}


// fonction executee en boucle

void loop(){
    uint16_t dat_p;
    int plen = 0;
    uint8_t buf_rf[VW_MAX_MESSAGE_LEN];
    uint8_t buf_rflen=VW_MAX_MESSAGE_LEN;
    buf_rf[75]=0;
    boolean send_data=0;
    char airq[5], lux[5], noise[5], hum[5], press[6], temp[5];


    while(1){
        buf_rflen = VW_MAX_MESSAGE_LEN; 
        plen = es.ES_enc28j60PacketReceive(BUFFER_SIZE, buf);
        dat_p=es.ES_packetloop_icmp_tcp(buf,plen);
        if( plen > 0 ) {
            Serial.println("received packet");
        }

        if (es.ES_client_waiting_gw() );

        // Reception radio
        if (vw_get_message(buf_rf, &buf_rflen)){ // Non-blocking
            digitalWrite(RX_LED, HIGH);
            Serial.print("got vw message : ");
            Serial.println((char*)buf_rf);
            send_data=1;
            digitalWrite(RX_LED, LOW);
        }

        Serial.println("enculé, con, taing");

        // Si nous avons une adresse IP pour le serveur (dns_state = 2) et que nous avons recu des donnees
        // -> envoi !


        if(send_data==1){

            // note the use of PSTR - this puts the string into code space and is compulsory in this call
            // second parameter is a variable string to append to HTTPPATH, this string is NOT a PSTR

            Serial.println("\nAttempt to send");

            Serial.print("Device : ");
            snprintf(deviceid,36,"%s",(char*)buf_rf);
            Serial.println(deviceid);

            //Serial.print("Value : ");
            //snprintf(value,26,"%s",(char*)buf_rf+36);
            //Serial.println(value);

            Serial.print("AirQ: ");
            snprintf(airq,5,"%s",(char*)buf_rf+35);
            Serial.print(airq);

            Serial.print(", Lux: ");
            snprintf(lux,5,"%s",(char*)buf_rf+40);
            Serial.print(lux);

            Serial.print(", Noi: ");
            snprintf(noise,5,"%s",(char*)buf_rf+44);
            Serial.print(noise);

            Serial.print(", Hum: ");
            snprintf(hum,5,"%s",(char*)buf_rf+47);
            Serial.print(hum);

            Serial.print(", Pressure: ");
            snprintf(press,6,"%s",(char*)buf_rf+51);
            Serial.print(press);

            Serial.print(", Temp: ");
            snprintf(temp,5,"%s",(char*)buf_rf+57);
            Serial.println(temp);
            
           // snprintf(tampon, 90, "/%036s?timestamp=%14s%cvalue=%10s", deviceid, timestamp,0x26, value);
            snprintf(tampon, 108, "%s/values?a=%s&l=%s&n=%s&h=%s&p=%s&t=%s", 
                                  deviceid, airq, lux, noise, hum, press, temp);
            tampon[89]=0;
            Serial.print("RESTful path : /push/pollux/");
            Serial.println(tampon);
            es.ES_client_browse_url(PSTR("/push/pollux/"), tampon , PSTR(HOSTNAME),&browserresult_callback);
            Serial.println("Post done");
            send_data=0;
        }
    }
}

int dns_resolution(int dat_p, int plen) {
    long lastDnsRequest = 0L;

    // We have a packet
    // Check if IP data
    if (dat_p == 0) {
        if (es.ES_client_waiting_gw() ){
            // No ARP received for gateway
            return 0;
        }
        // It has IP data
        if (dns_state==0){
            dns_state=1;
            lastDnsRequest = millis();
            es.ES_dnslkup_request(buf,(uint8_t*)WEBSERVER_VHOST);
            return 0;
        }
        if (dns_state==1 && es.ES_udp_client_check_for_dns_answer( buf, plen ) ){
            dns_state=2;
            Serial.println('got dns');
            es.ES_client_set_wwwip(es.ES_dnslkup_getip());
        }
        if (dns_state!=2){
            // retry every minute if dns-lookup failed:
            if (millis() > (lastDnsRequest + 60000L) ){
                dns_state=0;
                lastDnsRequest = millis();
            }
            // don't try to use web client before
            // we have a result of dns-lookup
            return 0;
        }
    } else {
        if (dns_state==1 && es.ES_udp_client_check_for_dns_answer( buf, plen ) ){
            dns_state=2;
            es.ES_client_set_wwwip(es.ES_dnslkup_getip());
        }
    }
    return 1;
}

// reception de donnees et affichage sur port serie

void browserresult_callback(uint8_t statuscode,uint16_t datapos){
  Serial.print("callback...");
  if (datapos != 0)
  {
    uint16_t pos = datapos;
    while (buf[pos])    // loop until end of buffer (or we break out having found what we wanted)
    {
      while (buf[pos]) if (buf[pos++] == '\n') break;   // find the first line feed
      if (buf[pos] == 0) break; // run out of buffer
      if (buf[pos++] == '\r') break; // if it is followed by a carriage return then it is a blank line (\r\n\r\n)
    }
    if (buf[pos])  // we didn't run out of buffer
    {
      pos++;  //skip over the '\n' remaining
      Serial.println((char*)&buf[pos]);
    }
  }
}




