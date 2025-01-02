from datetime import date,datetime
from typing import NamedTuple
import csv
from collections import defaultdict, Counter

Carrera = NamedTuple("Carrera", 
            [("nombre", str),
             ("escuderia", str),
             ("fecha_carrera", date) ,
             ("temperatura_min", int),
             ("vel_max", float),
             ("duracion",float),
             ("posicion_final", int),
             ("ciudad", str),
             ("top_6_vueltas", list[float]),
             ("tiempo_boxes",float),
             ("nivel_liquido", bool)
            ])

def parseo_top(top):
    res=[]
    for e in top.split("/"):

        e=e.strip("[")
        e=e.strip("]")
        e=e.strip()

        if e.strip() == "-":
            res.append(0)
        else:
            res.append(float(e))
    return res
    

def lee_carreras(ruta_fichero:str)->list[Carrera]:
    res=[]
    with open(ruta_fichero, encoding="UTF-8")as f:
        datos=csv.reader(f, delimiter=";")
        next(datos)
        for nombre,escuderia,fecha,temp,vel,duracion,posicion,ciudad,\
            top,tiempo_boxes,nivel_liquido in datos:
            fecha = datetime.strptime(fecha, "%d-%m-%y").date()
            temp = int(temp)
            vel = float(vel)
            duracion = float(duracion)
            posicion = int(posicion)
            top = parseo_top(top)
            tiempo_boxes = float(tiempo_boxes)
            nivel_liquido = nivel_liquido=="1"
            res.append(Carrera(nombre,escuderia,fecha,temp,vel,duracion,posicion,ciudad,\
            top,tiempo_boxes,nivel_liquido))
    return res


def media_tiempo_boxes(carreras:list[Carrera], ciudad:str,\
                        fecha:date | None =None)->float:
    
    res=[]
    for e in carreras:
        if fecha != None:
            if (e.ciudad==ciudad) and (e.fecha_carrera==fecha):
                res.append(e.tiempo_boxes)
        else:
            if (e.ciudad==ciudad):
                res.append(e.tiempo_boxes)

    if len(res)==0:
        return None

    return sum(res)/len(res)


def pilotos_menor_tiempo_medio_vueltas_top(carreras:list[Carrera],\
                                            n)->list[tuple[str,date]]:
    
    res1=[(e.nombre,e.fecha_carrera,sum(e.top_6_vueltas)/len(e.top_6_vueltas)) for e in carreras if 0 not in e.top_6_vueltas]

    res1.sort(key=lambda x:x[2])

    res=[(d1,d2) for d1,d2,d3 in res1][:n]
    return res


def ratio_tiempo_boxes_total(carreras:list[Carrera])->list[tuple[str,date, float]]:
    t_total=0
    res=[]

    for e in carreras:
        t_total+=e.tiempo_boxes

    for i in carreras:
        ratio=(i.tiempo_boxes/t_total)
        res.append((i.nombre,i.fecha_carrera,round(ratio, 3)))
    return sorted(res, key=lambda x:x[2])


def funcion_aux(carrera:Carrera):
    res=0
    if carrera.posicion_final==1:
        res=50
    elif carrera.posicion_final==2:
        res=25
    elif carrera.posicion_final==3:
        res=10
    return res

def puntos_piloto_anyos(carreras: list[Carrera]) -> dict[str, list[int]]:
    
    diccionario1=defaultdict(int)
    todo=defaultdict(dict)

    for e in carreras:
        clave=(e.nombre, e.fecha_carrera.year)
        diccionario1[clave]+=funcion_aux(e)
    
    for (nombre,anyo),puntos in diccionario1.items():
        diccionario2={anyo : puntos}
        todo[nombre].update(diccionario2)
    
    newDic=defaultdict(list)

    for piloto, puntitos in todo.items():
        for i,i2 in sorted(puntitos.items()):
            newDic[piloto].append(i2)
    
    return newDic

"""def calcular_puntos(carrera: Carrera) -> int:
    if carrera.posicion_final == 1:
        return 50
    elif carrera.posicion_final == 2:
        return 25
    elif carrera.posicion_final == 3:
        return 10
    else:
        return 0


def puntos_piloto_anyos(carreras: list[Carrera]) -> dict[str, list[int]]:

    puntos_por_piloto = defaultdict(list)
    acumulador = defaultdict(int)

    for carrera in carreras:
        puntos = calcular_puntos(carrera)
        anyo = carrera.fecha_carrera.year
        clave = (carrera.nombre, anyo)
        acumulador[clave] += puntos

    piloto_a_puntos = defaultdict(dict)
    for (piloto, anyo), puntos in acumulador.items():
        piloto_a_puntos[piloto].update({anyo: puntos})

    for piloto, puntos_por_anyo in piloto_a_puntos.items():
        puntos_ordenados = [puntos_por_anyo[anyo] for anyo in sorted(puntos_por_anyo)]
        puntos_por_piloto[piloto] = puntos_ordenados

    return dict(puntos_por_piloto)"""


def mejor_escuderia_anyo(carreras:list[Carrera], anyo:int)->str:
    res=Counter(e.escuderia for e in carreras if e.posicion_final ==1 if e.fecha_carrera.year==anyo)
    return res.most_common(1)[0][0]
