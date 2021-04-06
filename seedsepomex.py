import json
import threading

# Aqui solo se lee, limpia la data y se retorna
def lecturaSEPOMEX(ruta):
    if ruta == None or ruta == '':
        raise 'La ruta no puede nula'
    dataEntidades = []
    #Lectura del archivo de sepomex
    with open(ruta, 'r') as archivo:
        # Cada elemento del txt se limpia de salto de linea y se hace listas pequeñas con la data ya limpia
        dataEntidades = [x.strip('\n').split('|') for x in archivo.readlines()]

    # Lista de lista con la data
    return dataEntidades

# Hacemos un diccionario para rescatar la data que nos importa
# En este caso: estado, municipio, colonia y cp
def mapeoDeLoNecesario(listaDataEntidades):
    if listaDataEntidades == None or listaDataEntidades == []:
        raise 'La lista no tiene que ser nula'
    # diccionario para data
    dataNecesaria = {
        'data' : []
    }
    listaTemporal = []
    # Obtenemos toda la data necesaria
    # Este cotejamiento se hizo en base a la descripcion de campos de sepomex
    for i in listaDataEntidades:
        if i[10] == '09':
            listaTemporal.append({
                'cp' : i[0],
                'estado' : i[4],
                'colonia' : i[1],
                'municipio' : i[3],
                'ciudad' : i[5],
                'claveestado' : i[7],
                'clavemunicipio' : i[11],
                'idcolonia' : i[12],
                'claveciudad' : i[14]
            })
    dataNecesaria['data'] = listaTemporal
    return dataNecesaria

#query con llaves foraneas para las relaciones
def queryInsertConForeignKey(dataLista, nombreTabla, campos):
    totalEnLista = len(dataLista)-1
    totalCampos = len(campos)-1
    cont = 0
    query = 'INSERT INTO {} ('.format(nombreTabla)
    print("\n\nEmpezando el query \n\n")


# Funcion para hacer los querys de insertar a las tablas, esta funciona para hacer un query de forma general
def queryInsert(dataLista, nombreTabla, campos):
    totalEnLista = len(dataLista)-1
    totalCampos = len(campos)-1
    cont = 0
    query = 'INSERT INTO {} ('.format(nombreTabla)
    print("\n\nEmpezando el query \n\n")
    #Ciclo para sacar mapear los campos de la tabla
    for campo in campos:
        if cont != totalCampos:
            query += '{}, '.format(campo)
        else:
            query += '{}) VALUES '.format(campo)
        cont += 1
    cont = 0
    #Ciclo para mapear los campos en el query a sql
    for i in dataLista:
        if cont != totalEnLista:
            query += '(0, {}),'.format(i)
        else:
            query += '(0, {});'.format(i)
        cont += 1
    print("\n\n++++++Query : {} +++++++".format(query))
    return query

#Esta obtiene una lista con los datos ya sea de estados, municipios y colonias
def dataParaLosCampos(listaData, llaveDelDiccionario, llaveParaAgregarALista):
    mapaConteo = {}
    listaConLaData = []
    print("\n\nProceso para: {}\n\n".format(llaveParaAgregarALista))
    for entidad in listaData:
        if entidad[llaveDelDiccionario] not in mapaConteo:
            mapaConteo[entidad[llaveDelDiccionario]] = 1
            listaConLaData.append(entidad[llaveParaAgregarALista])
    #print(mapaConteo)
    #print(listaConLaData)
    return listaConLaData
#Esta funcion obtiene todos los datos sin repetir para poder hacer los querys
def insertarDatosTablas(dataMapaEntidades):
    print("Haciendo el diccionario de entidades")
    listaEstados = dataParaLosCampos(dataMapaEntidades, "claveestado", "estado")
    print(listaEstados)
    listaMunicipios = dataParaLosCampos(dataMapaEntidades, "clavemunicipio", "municipio")
    print(listaMunicipios)
    listaColonias = dataParaLosCampos(dataMapaEntidades, "idcolonia", "colonia")
    listaCPs = dataParaLosCampos(dataMapaEntidades, "cp", "cp")
    
    #Querys
    #queryEstados = queryInsert(listaEstados, 'estado', ['id, nombre'])
    #queryMunicipios = queryInsert(listaEstado, 'estado', ['id, nombre, idestado'])
#Funcion para escribir en el sql
def escribirSQL(dataMapeo):
    queryCreateTables = """
    CREATE TABLE IF NOT EXISTS estado (
        id int(10) NOT NULL AUTO_INCREMENT,
        nombre varchar(60) NOT NULL,
        PRIMARY KEY (id)
    );\n
    CREATE TABLE IF NOT EXISTS codigopostal (
        id int NOT NULL AUTO_INCREMENT,
        cp varchar(20) NOT NULL,
        PRIMARY KEY (id)
    );\n
    CREATE TABLE IF NOT EXISTS municipio (
        id int(10) NOT NULL AUTO_INCREMENT,
        nombre varchar(60) NOT NULL,
        idestado int(10) NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(idestado) REFERENCES estado(id) ON DELETE CASCADE ON UPDATE CASCADE
    );\n
    CREATE TABLE IF NOT EXISTS colonia (
        id int(10) NOT NULL AUTO_INCREMENT,
        nombre varchar(60) NOT NULL,
        idmunicipio int(10) NOT NULL,
        idcp int(10)NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(idmunicipio) REFERENCES municipio(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(idcp) REFERENCES codigopostal(id) ON DELETE CASCADE ON UPDATE CASCADE
    );\n
    """
    with open('scripbssepomex.sql', 'a+') as archivosql:
        archivosql.write(queryCreateTables)
        insertarDatosTablas(dataMapeo)
    print("Escritura en SQL lista \n")

#Escribimos en un JSON
def escribirJSON(dataMapeo):
    #Creamos el json con la data que necesitamos (Se puede modificar al gusto)
    with open('resultado.json', 'w') as archivoResultado:
        json.dump(dataMapeo, archivoResultado, indent=4)
    print("Escritura en JSON lista \n")


# Escribimos un archivo json para ver resultados y un archivo sql para una importacion rapida
def escrituraArchivoDB(dataMapeo):
    listaConLaData = dataMapeo['data']

    #Creamos hilos para no detener el proceso de las escrituras
    hiloSQL = threading.Thread(
        target=escribirSQL,
        args=(listaConLaData,),
        daemon=True
    )
    hiloSQL.start()
    hiloJSON = threading.Thread(
        target=escribirJSON,
        args=(dataMapeo,),
        daemon=True
    )
    hiloJSON.start()

    hiloPrincipal = threading.main_thread()
    for hilo in threading.enumerate():
        if hilo is hiloPrincipal:
            continue
        hilo.join()

    
if __name__ == '__main__':
    # Escribir la ruta de su archivo
    dataLimpia = lecturaSEPOMEX('./sepomex.txt')

    #print(dataLimpia)
    dataDelMapeo = mapeoDeLoNecesario(dataLimpia)
    #print(dataDelMapeo)
    escrituraArchivoDB(dataDelMapeo)