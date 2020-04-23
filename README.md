# LidarMenuQgis
Create a new temporany menu in Qgis for LIDAR upload and management

Codice di Python da caricare tramite Python Console di Qgis all'interno di un progetto.
Crea un menu personalizzato temporaneo con una funzione (LoadLidarFromShape_v4) utile a caricare e visulizzare da 1 a n file LIDAR 
selezionati tramite shapefile di inquadramento e caricati da percorsi memorizzati su disco.
Viene emulata al volo la tecnica del mosaico d'immagini senza creare file aggiuntivi.
La funzione ActiveLidarTOC() facilita la selezione del lidar d'interesse quando si devono eseguire operazioni sulla sengola sezione LIDAR
La procedura vive sino alla chiusura del progetto, poi menu e funzioni vengono scaricate.
Se viene modificata la procudera nella console di Python le funzionalità di menu si aggiornano al primo run.

---- 

Python code to be loaded via Qgis Python Console inside Project. Create a temporary custom menu with a function (LoadLidarFromShape_v4) useful for loading and displaying from 1 to n LIDAR files selected via frame shapefile and loaded from paths stored on disk. The mosaic image technique is emulated on the fly without creating additional files. The ActiveLidarTOC () function facilitates the selection of the lidar of interest when operations have to be performed on single LIDAR section. The procedure continues until the project is closed, then menus and functions are unistalled. If the procudera is changed in the Python console, the menu features update on the first run.
