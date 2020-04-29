
# Codice di Python da caricare tramite Python Console di Qgis.
# Crea un menu personalizzato con una funzione (LoadLidarFromShape_v4) utile a caricare e visulizzare da 1 a n file LIDAR 
# selezionati tramite shapefile di inquadramento e caricati da percorsi memorizzati su disco.
# Viene emulata al volo la tecnica del mosaico d'immagini senza creare file aggiuntivi.
# La funzione ActiveLidarTOC() facilita la selezione del lidar d'interesse quando si devono 
# eseguire operazioni sulla sengola sezione LIDAR
# La procedura vive sino alla chiusura del progetto, poi menu e funzioni vengono scaricate.
# Se modificata deve essere chiuso e riaperto il progetto
import ctypes
import sys


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


###### Titoli del progetto e del Menu######

myQGis_Title='LSulli QGIS'
myMenu_Title='LSulli_Menu'
myMsgBox_Title='Procedura: carica Lidar da Shapefile'



title = iface.mainWindow().windowTitle()
if title != myQGis_Title:
    new_title = myQGis_Title
iface.mainWindow().setWindowTitle(new_title)

###### Funzioni ######

def LoadLidarFromShape_v4():
    #inizializzo le variabili per il controllo degli shapefile di riferimento
    a = 0 # check per verifica shapefile inquadramento
    b = 0 
    my_msg=""

    # popolo il dizionario dei layer presenti nel progetto
    layers = iface.mapCanvas().layers() 

    # recupero il nome dello shapefile attivo (la funzione lavora attoivando lo shapefile di inquadramento)
    try:
        my_active_layer=iface.activeLayer()
        my_name_layer = my_active_layer.name()
    except:
        Mbox(myMsgBox_Title, 'Lo shapefile di inquadramento non è stato attivato o il nome indicato è sbagliato', 1)
        print ('Lo shapefile di inquadramento non è stato attivato o il nome indicato è sbagliato')
        return

    # nel mi caso sono disponibili due shapefile di inquadramento uno della Regione Toscana e uno del Ministero dell'Ambiente.
    # verifico che lo shapefile di inquadramento si stato caricato è sia attivo
    # assegno il corretto nome del campo degli attributi per recuperare il nome del Lidar e la path del file
    # assegno il CRS corretto ad ogni set di dati
    # assegno il fattore di scala (diverso per il set del ministero dell'ambiente)
    try:
        if my_name_layer == 'QU_Griglia_1x1_path':
            my_CRS_system = 4326
            my_ZFactorSet = 0.00001  # fattore di scala specifico per dataset del Ministero dell'Ambiente
            my_feature_fld = 'tavola'
            my_path_fld = 'path'
            a=1
        elif my_name_layer == 'RT_LIDAR_PATH':
            my_ZFactorSet = 1
            my_CRS_system = 3003
            my_feature_fld = 'DTMNAME'
            my_path_fld = 'path'
            a=1
        else:
            Mbox(myMsgBox_Title, 'Lo shapefile di inquadramento non è stato attivato o il nome indicato è sbagliato', 1)
            print ('Lo shapefile di inquadramento non è stato attivato o il nome indicato è sbagliato')
            a=0
    except:
        return
    while a==1:
        my_registry = QgsProject.instance()
        my_layer = my_registry.mapLayersByName(my_name_layer)[0]
        iface.setActiveLayer(my_layer)
        my_selection=my_layer.selectedFeatures()
        if len(my_selection) == 0:
            Mbox(myMsgBox_Title, 'Non è stato selezionato nessun oggetto nello shapefile '+my_name_layer, 1)
            print ('Non è stato selezionato nessun oggetto nello shapefile ', my_name_layer)
        for feature in my_selection:
            try:
                lyr = iface.addRasterLayer(feature[my_path_fld], feature[my_feature_fld])
                lyr.setCrs( QgsCoordinateReferenceSystem(my_CRS_system, QgsCoordinateReferenceSystem.EpsgCrsId))
                my_render_layer = iface.activeLayer()
                r = QgsHillshadeRenderer (my_render_layer.dataProvider(), 1, 315, 45)
                r.setZFactor (my_ZFactorSet)
                my_render_layer.setRenderer(r)
            except:
                print(feature [my_path_fld], r"non esiste o non e' stato dezippato")
        iface.setActiveLayer(my_layer)
        a=0
        Mbox(myMsgBox_Title, 'Procedura terminata', 1)

def ActiveLidarTOC():

    #inizializzo le variabili per il controllo degli shapefile di riferimento
    a = 1 # check per verifica shapefile inquadramento
    # popolo il dizionario dei layer presenti nel progetto
    layers = iface.mapCanvas().layers() 

    # recupero il nome dello shapefile attivo
    my_active_layer=iface.activeLayer()
    my_name_layer = my_active_layer.name()
        
    # verifico che lo shapefile di inquadramento si stato caricato è sia attivo
    # assegno il corretto nome del campo degli attributi per recuperare il nome del Lidar
    if my_name_layer == 'QU_Griglia_1x1_path':
        my_feature_fld = 'tavola'
    elif my_name_layer == 'RT_LIDAR_PATH':
        my_feature_fld = 'DTMNAME'
    else:
        print ('Lo shapefile di inquadramento non è stato attivato o il nome indicato è sbagliato')
        a=0 # condizione di interruzione procedura
        
    if a == 1:
        my_registry = QgsProject.instance()
        my_layer = my_registry.mapLayersByName(my_name_layer)[0]
        my_selection=my_layer.selectedFeatures()
        
        for feature in my_selection:
            if len (my_registry.mapLayersByName(feature[my_feature_fld])) != 0:
                my_setactivelayer=my_registry.mapLayersByName(feature[my_feature_fld])[0]
        # viene attivato il foglio LIDAR indicato nel riquadro seleionato dello shapefile
                for ly in layers:
                    if ly.name() == my_setactivelayer.name():
                        iface.setActiveLayer(my_setactivelayer)
                        print ('Selezionato lidar: ', my_setactivelayer.name())
            else:
                print('Non esiste nel progetto nessun Lidar del nome indicato')
    else:
        print ('La procedura è stata interrotta')

def calc_area():
    my_active_layer=iface.activeLayer()
    my_name_layer = my_active_layer.name()
    my_registry = QgsProject.instance()
    my_layer = my_registry.mapLayersByName(my_name_layer)[0]
    my_layer.startEditing()
    myarea = 0
    for feature in my_layer.getSelectedFeatures():
        geom=feature.geometry()
        myarea=geom.area()
        feature.setAttribute(feature.fieldNameIndex('area'), myarea)
        my_layer.updateFeature(feature)
    print (myarea)


######################Creazione menu##########################

#Controlla se esiste già il Menu personalizzato e nel caso rimuove tutte le voci
for x in iface.mainWindow().findChildren(QMenu): 
    a= x.menuAction() #recupera l'oggetto menuAction() presente in tutti gli oggetti della classe QMenu
    if a.text()== myMenu_Title: #recupera la stringa testo dell'oggetto menuAction()
        iface.mainWindow().menuBar().removeAction (a)
        
#Crea il menù personalizzato e aggiunge le funzionalità
MyMenu = QMenu(myMenu_Title, iface.mainWindow().menuBar())
CalcArea_action = QAction('Calcola area poligono selezionato')
CalcArea_action.triggered.connect(calc_area)
LoadLidar_action = QAction('Carica Lidar da Shapefile')
LoadLidar_action.triggered.connect(LoadLidarFromShape_v4)
ActiveLidar_action = QAction('Attiva Lidar nella TOC')
ActiveLidar_action.triggered.connect(ActiveLidarTOC)
    
iface.mainWindow().menuBar().insertMenu(CalcArea_action, MyMenu)
MyMenu.addAction(CalcArea_action)
MyMenu.addSeparator()
MyMenu.addAction(LoadLidar_action)
MyMenu.addSeparator()
MyMenu.addAction(ActiveLidar_action)
#
