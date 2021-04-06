
    CREATE TABLE IF NOT EXISTS estado (
        id int(10) NOT NULL AUTO_INCREMENT,
        nombre varchar(60) NOT NULL,
        PRIMARY KEY (id)
    );

    CREATE TABLE IF NOT EXISTS codigopostal (
        id int NOT NULL AUTO_INCREMENT,
        cp varchar(20) NOT NULL,
        PRIMARY KEY (id)
    );

    CREATE TABLE IF NOT EXISTS municipio (
        id int(10) NOT NULL AUTO_INCREMENT,
        nombre varchar(60) NOT NULL,
        idestado int(10) NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(idestado) REFERENCES estado(id) ON DELETE CASCADE ON UPDATE CASCADE
    );

    CREATE TABLE IF NOT EXISTS colonia (
        id int(10) NOT NULL AUTO_INCREMENT,
        nombre varchar(60) NOT NULL,
        idmunicipio int(10) NOT NULL,
        idcp int(10)NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(idmunicipio) REFERENCES municipio(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(idcp) REFERENCES codigopostal(id) ON DELETE CASCADE ON UPDATE CASCADE
    );

    