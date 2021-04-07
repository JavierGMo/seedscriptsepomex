# Obtener datos limpios de SEPOMEX
## Requisitos:
- python 3.x


Nota: Este script se corrio en windows 10 y ubuntu. Este script trabaja bajo parametros muy especificos y tiene resultados muy especificos, pero se puede modificar para obtener la data que requieras o requieran.

Este script funciona con base en los datos de SEPOMEX, para este script se utilizo el txt, este txt solo debe de tener algunas modificaciones, las cuales son borrar cosas que no nos sirven y que solo estorbaria y producirian errores en el script, dichas lineas que se deben de quitar son las siguientes:

El Catálogo Nacional de Códigos Postales, es elaborado por Correos de México y se proporciona en forma gratuita para uso particular, no estando permitida su comercialización, total o parcial, ni su distribución a terceros bajo ningún concepto.
d_codigo|d_asenta|d_tipo_asenta|D_mnpio|d_estado|d_ciudad|d_CP|c_estado|c_oficina|c_CP|c_tipo_asenta|c_mnpio|id_asenta_cpcons|d_zona|c_cve_ciudad

El txt no debe de tener espacios en blanco por arriba de lo que se borro, mover las lienas a la posicion 1

En este repo dejare el txt limpio de sepomex para que este se pueda leer. Se puede borrar, pero debe tener el nombre de sepomex.txt para que el script lo lea, sino habra errores y dejar como ya se ha mencionado arriba.
Este script nos devuelve dos archivos que son un JSON y un SQL. El JSON contiene informacion que es de interes, no es tan importante solo era para pruebas, el segundo archivo es el mas importante, que es el SQL el cual contiene consultas para crear tablas de nuestro interes e insertar datos de nuestro interes.
Para este script es necesario borrar los archivos resultado.json y scriptdbsepomex.sql, en caso de que no se borre se escribira en el archivo que ya viene el repo y surgiran errores si se quiere importar a mysql.

Si solo requiere usar las tablas y la data de estas puede borrar el create database y el use.