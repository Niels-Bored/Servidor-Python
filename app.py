from flask import Flask, request
from config import Config
from mysql import MySQL
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

# Obtener credentiales de base de datos
credentials = Config ()
db_server = credentials.get ("db_server")
db_name = credentials.get ("db_name")
db_user = credentials.get ("db_user")
db_password = credentials.get ("db_password")

# Conectar con mysql
database = MySQL (db_server, db_name, db_user, db_password)

def format_db_user (usuario):
    usuario_obj = {}
    usuario_obj["id"]       = usuario[0]
    usuario_obj["nombre"]   = usuario[1]
    usuario_obj["ap_pat"]   = usuario[2]
    usuario_obj["ap_mat"]   = usuario[3]
    usuario_obj["telefono"] = usuario[4]
    usuario_obj["correo"]   = usuario[5]
    usuario_obj["estado"]   = usuario[6]
    usuario_obj["calle"]    = usuario[7]
    usuario_obj["colonia"]  = usuario[8]
    usuario_obj["no_int"]   = usuario[9]
    usuario_obj["password"] = usuario[10].split("\n")[0]
    return usuario_obj

def format_db_state (estado):
    estado_obj = {}
    estado_obj["Id"]     = estado[0]
    estado_obj["Nombre"] = estado[1].split("\n")[0]
    return estado_obj

def format_db_pet (mascota):
    mascota_obj = {}
    mascota_obj["Id"]          = mascota[0]
    mascota_obj["Nombre"]      = mascota[1]
    mascota_obj["Raza"]        = mascota[2]
    mascota_obj["Color"]       = mascota[3]
    mascota_obj["Edad"]        = mascota[4]
    mascota_obj["Descripcion"] = mascota[5]
    mascota_obj["Imagen"]      = mascota[6]
    mascota_obj["Id_Usuario"]  = mascota[7].split("\n")[0]
    return mascota_obj

def format_db_lost_pet (mascota_perdida):
    mascota_obj = {}
    mascota_obj["Id"]                 = mascota_perdida[0]
    mascota_obj["Nombre"]             = mascota_perdida[1]
    mascota_obj["Raza"]               = mascota_perdida[2]
    mascota_obj["Color"]              = mascota_perdida[3]
    mascota_obj["edad"]               = mascota_perdida[4]
    mascota_obj["Descripcion"]        = mascota_perdida[5]
    mascota_obj["fecha_desaparicion"] = mascota_perdida[6]
    mascota_obj["fecha_publicacion"]  = mascota_perdida[7]
    mascota_obj["Imagen"]             = mascota_perdida[8]
    mascota_obj["Id_Usuario"]         = mascota_perdida[9].split("\n")[0]

    return mascota_obj

@app.get("/usuario/mascota/adopcion/<int:id>")
def get_mascotas_adopcion_usuario (id):   
    """ Regresar mascota por usuario """ 

    offset = int(request.args.get ("offset", 0)) 

    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        registros_mascotas = archivo.readlines()

    informacion_retorno = []
    registros_filtrados = []

    encontrado = False
    for registro in registros_mascotas:
        informacion_registro = registro.split("| ")
        if(str(id) in informacion_registro[7]):
            registros_filtrados.append (registro)
            encontrado = True

    registros_filtrados = registros_filtrados[offset:offset+5]

    for registro in registros_filtrados:
        informacion_registro = registro.split("| ")
        
        if(str(id) in informacion_registro[7]):
            informacion_retorno.append (format_db_pet (informacion_registro))    
        
    if (encontrado):
        
        return informacion_retorno
    else:
        return ({"error": f"user {id} not found"}, 403)

@app.get("/usuario/mascota/perdida/<int:id>")
def get_mascotas_perdidas_usuario (id):   
    """ Regresar mascota por usuario """ 

    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        registros_mascotas = archivo.readlines()

    offset = int(request.args.get ("offset", 0)) 

    informacion_retorno = []
    registros_filtrados = []

    encontrado = False
    for registro in registros_mascotas:
        informacion_registro = registro.split("| ")
        if(str(id) in informacion_registro[9]):
            registros_filtrados.append (registro)
            encontrado = True

    registros_filtrados = registros_filtrados[offset:offset+5]

    for registro in registros_filtrados:
        informacion_registro = registro.split("| ")
        
        if(str(id) in informacion_registro[9]):
            informacion_retorno.append (format_db_lost_pet (informacion_registro))    
        
    if (encontrado):
        
        return informacion_retorno
    else:
        return ({"error": f"user {id} not found"}, 403)


@app.get("/usuarios/")
def get_usuarios ():
    """ Obetener usuarios """
    # Obtener todos los usuarios

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de usuarios 
    usuarios_list = []
    
    # Consultar información de tabla
    with open("//192.168.43.177/Usuarios/Usuarios.txt", "r", encoding="utf-8") as archivo:
        usuarios = archivo.readlines()
    
    # Filtrar datos en base al offset
    usuarios = usuarios[offset:offset+20]
    
    # Recorrer cada usuario para convertirlo a un diccionario / objetos
    for usuario in usuarios: 
        # obtener y guardar usuario
        informacion = usuario.split("| ")
        usuarios_list.append (format_db_user (informacion))
    
    
    # Retornar arreglo de objetos de usuarios
    return usuarios_list

@app.get("/usuario/<int:id>")
def get_usuario (id):
    """ Obetener usuario id """
    
    # Consultar información de Tabla
    with open("//192.168.43.177/Usuarios/Usuarios.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            informacion = linea.split("| ")
            if(str(id) in informacion[0]):
                usuario = informacion
                encontrado = True
                break
            else:
                encontrado = False    

    if encontrado:
        usuario_obj = format_db_user (usuario)
        
        # Retornar arreglo de objetos de usuarios
        return usuario_obj

    else:
        return ({"error": "user not found"}, 403)

@app.post("/usuario/")
def post_usuario ():   
    """ Actualizar un usuario """ 
    
    # Obtener datos del requests
    id = request.json.get("id", "") 
    nombre = request.json.get("nombre", "") 
    ap_pat = request.json.get("ap_pat", "") 
    ap_mat = request.json.get("ap_mat", "")
    telefono = request.json.get("telefono", "") 
    correo = request.json.get("correo", "") 
    estado = request.json.get("estado", "")
    calle = request.json.get("calle", "") 
    colonia = request.json.get("colonia", "") 
    no_int = request.json.get("no_int", 0) 
    password = request.json.get("password", "") 
    
    if not id or not nombre or not ap_pat or not ap_mat or not telefono or not correo or not estado or not calle or not colonia or not no_int or not password:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Usuarios/Usuarios.txt", "r", encoding="utf-8") as archivo:
        registros_usuarios = archivo.readlines()

    informacion_txt = ""
        
    encontrado = False
    for registro in registros_usuarios:
        
        informacion_registro = registro.split("| ")
        informacion = registro.split("| ")
        
        if(str(id) in informacion_registro[0]):
            informacion_insertar = [str(id), nombre, ap_pat, ap_mat, telefono, correo, str(estado),calle, colonia, str(no_int), password+"\n"]
            encontrado = True
        else:
            informacion_insertar = [informacion[0], informacion[1], informacion[2], informacion[3], informacion[4], informacion[5], informacion[6], informacion[7], informacion[8], informacion[9], informacion[10]]

        informacion_txt += '| '.join(informacion_insertar)

    if (encontrado):
        with open("//192.168.43.177/Usuarios/Usuarios.txt", "w", encoding="utf-8") as archivo:
            archivo.write(informacion_txt)
        return {"ok": True}
    else:
        return ({"error": f"user {id} not found"}, 403)

@app.post("/usuario/login/")
def login_usuario ():   
    """ Autenticar un usuario """ 
    
    # Obtener datos del requests
    nombre = request.json.get("nombre", "") 
    password = request.json.get("password", "") 
    
    if not nombre or not password:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Usuarios/Usuarios.txt", "r", encoding="utf-8") as archivo:
        registros_usuarios = archivo.readlines()


    id = ""
        
    encontrado = False
    for registro in registros_usuarios:
        
        informacion_registro = registro.split("| ")
        
        if(nombre == informacion_registro[5] and password == informacion_registro[10].split("\n")[0]):
            id = informacion_registro[0]
            encontrado = True

    if (encontrado):
        
        return {"ok": True, "id":id}
    else:
        return ({"error": f"invalid credentials"}, 403)


@app.put("/usuario/")
def put_usuario (): 

    # Obtener datos del requests
    nombre = request.json.get("nombre", "") 
    ap_pat = request.json.get("ap_pat", "") 
    ap_mat = request.json.get("ap_mat", "")
    telefono = request.json.get("telefono", "") 
    correo = request.json.get("correo", "") 
    estado = request.json.get("estado", "")
    calle = request.json.get("calle", "") 
    colonia = request.json.get("colonia", "") 
    no_int = request.json.get("no_int", 0) 
    password = request.json.get("password", "") 
        
    if not nombre or not ap_pat or not ap_mat or not telefono or not correo or not estado or not calle or not colonia or not no_int or not password:
        return ({"error": "invalid or missing pramaters"}, 403)

    res = requests.get (f"https://verifier.meetchopra.com/verify/{correo}?token=92928b756e623357b3bd80e8dc90deae2930ffd26e598b84867f3b788106dce911a819a49e3e3fe6834c36e844035116")
    res.raise_for_status()
    json_response = res.json()

    if not json_response["status"]:
        return ({"error": "invalid email"}, 403)

    with open("//192.168.43.177/Usuarios/Usuarios.txt", "r", encoding="utf-8") as archivo:
        usuarios = archivo.readlines()

    ultimo_usuario = usuarios[-1].split("| ")

    id = int(ultimo_usuario[0])

    id+=1

    informacion = [str(id), nombre, ap_pat, ap_mat, telefono, correo, str(estado), calle, colonia, str(no_int), password]
    informacion_txt = '| '.join(informacion)

    informacion_txt=informacion_txt+"\n"
    print(informacion_txt)

    with open("//192.168.43.177/Usuarios/Usuarios.txt", "a", encoding="utf-8") as archivo:
        archivo.write(informacion_txt)
    
    return {"ok": True}
    
@app.delete("/usuario/")
def delete_usuario ():    
    # Obtener datos del requests
    id = request.json.get("id", "")     
        
    if not id:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Usuarios/Usuarios.txt", "r", encoding="utf-8") as archivo:
        registros_usuarios = archivo.readlines()
    
    encontrado = False
    for registro in registros_usuarios:
        
        index=registros_usuarios.index(registro)

        informacion_registro = registro.split("| ")
        
        if(str(id) in informacion_registro[0]):
            del registros_usuarios[index]
            encontrado = True
            break
        else:
            encontrado = False

    informacion_txt = ""
    for registro in registros_usuarios:
        informacion = registro.split("| ")
        informacion_insertar = [informacion[0], informacion[1], informacion[2], informacion[3], informacion[4], informacion[5], informacion[6], informacion[7], informacion[8], informacion[9], informacion[10]]
        informacion_txt += '| '.join(informacion_insertar)
        #informacion_txt+="\n"

    if (encontrado):
        with open("//192.168.43.177/Usuarios/Usuarios.txt", "w", encoding="utf-8") as archivo:
            archivo.write(informacion_txt)
        return {"ok": True}
    else:
        return ({"error": f"user {id} not found"}, 403)
###############Estados############################
@app.get("/usuario/estado/<int:id>")
def get_estado (id):
    """ Obetener estado por id """
    
    # Consultar información de Tabla
    with open("//192.168.43.177/Usuarios/Estados.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            informacion = linea.split("| ")
            if(str(id) in informacion[0]):
                estado = informacion
                encontrado = True
                break
            else:
                encontrado = False    

    if encontrado:
        estado_obj = format_db_state (estado)
        
        # Retornar arreglo de objetos de usuarios
        return estado_obj

    else:
        return ({"error": "user not found"}, 403)
###############Mascotas en Adopción###############


@app.get("/mascotas/adopcion/")
def get_adopciones ():
    """ Obetener mascotas en adopción """
    # Obtener todas las mascotas en adopción

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de mascotas 
    mascotas_list = []
    
    # Consultar información de base de datos
    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        mascotas = archivo.readlines()
    
    # Filtrar datos en base al offset
    mascotas = mascotas[offset:offset+5]
    
    # Recorrer cada mascota para convertirlo a un diccionario / objetos
    for mascota in mascotas: 
        
        # obtener y guardar mascota
        informacion = mascota.split("| ")
        mascotas_list.append (format_db_pet (informacion))
    
    # Retornar arreglo de objetos de mascotas
    return mascotas_list

@app.get("/mascota/adopcion/<int:id>")
def get_adopcion (id):
    """ Obtener mascota en adopción por id """
    
    # Consultar información de Tabla
    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            informacion = linea.split("| ")
            if(str(id) in informacion[0]):
                mascota = informacion
                encontrado = True
                break
            else:
                encontrado = False 

    if encontrado:
        mascota_obj = format_db_pet (mascota)
        
        # Retornar arreglo de objetos de mascota
        return mascota_obj

    else:
        return ({"error": "pet not found"}, 403)

@app.get("/mascota/adopcion/<string:nombre>")
def get_adopcion_nombre (nombre):
    """ Obtener mascota en adopción por nombre """
    
    # Consultar información de Tabla
    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            informacion = linea.split("| ")
            if(nombre in informacion[1]):
                mascota = informacion
                encontrado = True
                break
            else:
                encontrado = False 

    if encontrado:
        mascota_obj = format_db_pet (mascota)
        
        # Retornar arreglo de objetos de mascota
        return mascota_obj

    else:
        return ({"error": "pet not found"}, 403)

@app.post("/mascota/adopcion")
def post_adopcion ():   
    """ Actualizar una mascota """ 
    
    # Obtener datos del requests
    id = request.json.get("id", "") 
    nombre = request.json.get("nombre", "") 
    raza = request.json.get("raza", "") 
    color = request.json.get("color", "")
    edad = request.json.get("edad", "") 
    descripcion = request.json.get("descripcion", "") 
    imagen = request.json.get("imagen", "") 
    id_u = request.json.get("id_usuario", "")
    
    if not id or not nombre or not raza or not color or not edad or not descripcion or not id_u:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        registros_mascotas = archivo.readlines()

    informacion_txt = ""
        
    encontrado = False
    for registro in registros_mascotas:
        
        informacion_registro = registro.split("| ")
        informacion = registro.split("| ")
        
        if(str(id) in informacion_registro[0]):
            informacion_insertar = [str(id), nombre, raza, color, edad, descripcion, imagen,id_u+"\n"]
            encontrado = True
        else:
            informacion_insertar = [informacion[0], informacion[1], informacion[2], informacion[3], informacion[4], informacion[5], informacion[6],informacion[7]]

        informacion_txt += '| '.join(informacion_insertar)

    if (encontrado):
        with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "w", encoding="utf-8") as archivo:
            archivo.write(informacion_txt)
        return {"ok": True}
    else:
        return ({"error": f"user {id} not found"}, 403)   

@app.put("/mascota/adopcion")
def put_adopcion (): 

    # Obtener datos del requests
    nombre = request.json.get("nombre", "") 
    raza = request.json.get("raza", "") 
    color = request.json.get("color", "")
    edad = request.json.get("edad", "") 
    descripcion = request.json.get("descripcion", "") 
    imagen = request.json.get("imagen", "") 
    id_u = request.json.get("id_usuario", "")
        
    if not nombre or not raza or not color or not edad or not descripcion or not id_u:
        return ({"error": "invalid or missing pramaters"}, 403)
    
     # Insertar mascota en tabla
    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        mascotas = archivo.readlines()

    ultima_mascota = mascotas[-1].split("| ")

    id = int(ultima_mascota[0])

    id+=1

    informacion = [str(id), nombre, raza, color, edad, descripcion, imagen, id_u]
    informacion_txt = '| '.join(informacion)

    informacion_txt=informacion_txt+"\n"
    print(informacion_txt)

    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "a", encoding="utf-8") as archivo:
        archivo.write(informacion_txt)
    
    return {"ok": True}
    
@app.delete("/mascota/adopcion/<int:id>")
def delete_adopcion (id):    
    # Obtener datos del requests
    if not id:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "r", encoding="utf-8") as archivo:
        registros_mascotas = archivo.readlines()
    
    encontrado = False
    for registro in registros_mascotas:
        
        index=registros_mascotas.index(registro)

        informacion_registro = registro.split("| ")
        
        if(str(id) in informacion_registro[0]):
            del registros_mascotas[index]
            encontrado = True
            break
        else:
            encontrado = False

    informacion_txt = ""
    for registro in registros_mascotas:
        informacion = registro.split("| ")
        informacion_insertar = [informacion[0], informacion[1], informacion[2], informacion[3], informacion[4], informacion[5], informacion[6], informacion[7]]
        informacion_txt += '| '.join(informacion_insertar)
        #informacion_txt+="\n"

    if (encontrado):
        with open("//192.168.43.177/Datos/Mascotas_Adopcion.txt", "w", encoding="utf-8") as archivo:
            archivo.write(informacion_txt)
        return {"ok": True}
    else:
        return ({"error": f"user {id} not found"}, 403)

###############Mascotas Perdidas###############

@app.get("/mascotas/perdida/")
def get_perdidas ():
    """ Obetener mascotas perdidas """
    # Obtener todas las mascotas perdidas

    # Obtener offset
    offset = int(request.args.get ("offset", 0)) 
    
    # Inicializar lista vacía de mascotas 
    mascotas_list = []
    
    # Consultar información de base de datos
    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        mascotas = archivo.readlines()
    
    # Filtrar datos en base al offset
    mascotas = mascotas[offset:offset+5]
    
    # Recorrer cada mascota para convertirlo a un diccionario / objetos
    for mascota in mascotas: 
        
        # obtener y guardar mascota
        informacion = mascota.split("| ")
        mascotas_list.append (format_db_lost_pet (informacion))
    
    # Retornar arreglo de objetos de mascotas
    return mascotas_list

@app.get("/mascota/perdida/<int:id>")
def get_perdida (id):
    """ Obtener mascota perdida por id """
    
    # Consultar información de Tabla
    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            informacion = linea.split("| ")
            if(str(id) in informacion[0]):
                mascota = informacion
                encontrado = True
                break
            else:
                encontrado = False 

    if encontrado:
        mascota_obj = format_db_lost_pet (mascota)
        
        # Retornar arreglo de objetos de mascota
        return mascota_obj

    else:
        return ({"error": "pet not found"}, 403)

@app.get("/mascota/perdida/<string:nombre>")
def get_perdida_nombre (nombre):
    """ Obtener mascota perdida por nombre """
    
    # Consultar información de Tabla
    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            informacion = linea.split("| ")
            if(nombre in informacion[1]):
                mascota = informacion
                encontrado = True
                break
            else:
                encontrado = False 

    if encontrado:
        mascota_obj = format_db_lost_pet (mascota)
        
        # Retornar arreglo de objetos de mascota
        return mascota_obj

    else:
        return ({"error": "pet not found"}, 403)

@app.post("/mascota/perdida")
def post_perdida ():   
    """ Actualizar una mascota """ 
    
    # Obtener datos del requests
    id = request.json.get("id", "") 
    nombre = request.json.get("nombre", "") 
    raza = request.json.get("raza", "") 
    color = request.json.get("color", "")
    edad = request.json.get("edad", "")
    descripcion = request.json.get("descripcion", "") 
    fecha_desaparicion = request.json.get("fecha_desaparicion", "") 
    fecha_publicacion = request.json.get("fecha_publicacion", "")
    imagen = request.json.get("imagen", "") 
    id_u = request.json.get("id_usuario", "")
    
    if not id or not nombre or not raza or not color or not edad or not descripcion or not fecha_desaparicion or not fecha_publicacion or not id_u:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        registros_mascotas = archivo.readlines()

    informacion_txt = ""
        
    encontrado = False
    for registro in registros_mascotas:
        
        informacion_registro = registro.split("| ")
        informacion = registro.split("| ")
        
        if(str(id) in informacion_registro[0]):
            informacion_insertar = [str(id), nombre, raza, color, edad, descripcion, fecha_desaparicion, fecha_publicacion, imagen,id_u+"\n"]
            encontrado = True
        else:
            informacion_insertar = [informacion[0], informacion[1], informacion[2], informacion[3], informacion[4], informacion[5], informacion[6], informacion[7], informacion[8],informacion[9]]

        informacion_txt += '| '.join(informacion_insertar)

    if (encontrado):
        with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "w", encoding="utf-8") as archivo:
            archivo.write(informacion_txt)
        return {"ok": True}
    else:
        return ({"error": f"user {id} not found"}, 403)
@app.put("/mascota/perdida")
def put_perdida (): 

    # Obtener datos del requests
    nombre = request.json.get("nombre", "") 
    raza = request.json.get("raza", "") 
    color = request.json.get("color", "")
    edad = request.json.get("edad", "") 
    descripcion = request.json.get("descripcion", "")
    fecha_desaparicion = request.json.get("fecha_desaparicion", "") 
    fecha_publicacion = request.json.get("fecha_publicacion", "")
    imagen = request.json.get("imagen", "") 
    id_u = request.json.get("id_usuario", "")
        
    if not nombre or not raza or not color or not edad or not descripcion or not fecha_desaparicion or not fecha_publicacion or not id_u:
        return ({"error": "invalid or missing pramaters"}, 403)

     # Insertar mascota en tabla
    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        mascotas = archivo.readlines()

    ultima_mascota = mascotas[-1].split("| ")

    id = int(ultima_mascota[0])

    id+=1

    informacion = [str(id), nombre, raza, color, edad, descripcion, fecha_desaparicion, fecha_publicacion, imagen,id_u]
    informacion_txt = '| '.join(informacion)

    informacion_txt=informacion_txt+"\n"
    print(informacion_txt)

    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "a", encoding="utf-8") as archivo:
        archivo.write(informacion_txt)
    
    return {"ok": True}
    
@app.delete("/mascota/perdida/<int:id>")
def delete_perdida (id):    
    # Obtener datos del requests
        
    if not id:
        return ({"error": "invalid or missing pramaters"}, 403)

    with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "r", encoding="utf-8") as archivo:
        registros_mascotas = archivo.readlines()
    
    encontrado = False
    for registro in registros_mascotas:
        
        index=registros_mascotas.index(registro)

        informacion_registro = registro.split("| ")
        
        if(str(id) in informacion_registro[0]):
            del registros_mascotas[index]
            encontrado = True
            break
        else:
            encontrado = False

    informacion_txt = ""
    for registro in registros_mascotas:
        informacion = registro.split("| ")
        informacion_insertar = [informacion[0], informacion[1], informacion[2], informacion[3], informacion[4], informacion[5], informacion[6], informacion[7], informacion[8], informacion[9]]
        informacion_txt += '| '.join(informacion_insertar)
        #informacion_txt+="\n"

    if (encontrado):
        with open("//192.168.43.177/Datos/Mascotas_Perdidas.txt", "w", encoding="utf-8") as archivo:
            archivo.write(informacion_txt)
        return {"ok": True}
    else:
        return ({"error": f"pet {id} not found"}, 403)

if __name__ == "__main__":
    app.run (port="3000", host="0.0.0.0", debug=True)