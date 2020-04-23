# LidarMenuQgis
Create a new temporany menu in Qgis for LIDAR upload and management

Codice di Python da caricare tramite Python Console di Qgis.
Crea un menu personalizzato temporaneo con una funzione (LoadLidarFromShape_v4) utile a caricare e visulizzare da 1 a n file LIDAR 
selezionati tramite shapefile di inquadramento e caricati da percorsi memorizzati su disco.
Viene emulata al volo la tecnica del mosaico d'immagini senza creare file aggiuntivi.
La funzione ActiveLidarTOC() facilita la selezione del lidar d'interesse quando si devono eseguire operazioni sulla sengola sezione LIDAR
La procedura vive sino alla chiusura del progetto, poi menu e funzioni vengono scaricate.
Se viene modificata la procudera nella console di Python le funzionalità di menu si aggiornano al primo run.
