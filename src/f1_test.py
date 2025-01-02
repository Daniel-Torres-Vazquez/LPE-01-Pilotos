from f1 import *

def lectura_test():
    datos=lee_carreras("./data/f1.csv")
    print(len(datos), datos[0])

def media_t_test(datos):
    print(media_tiempo_boxes(datos, "Barcelona"))

def pilotos_menor_tiempo_medio_vueltas_top_test(datos, n):
    print(pilotos_menor_tiempo_medio_vueltas_top(datos, n))

def ratios_test(datos):
    print("##################################################")
    print("4. Test ratio_tiempo_boxes_total")
    ratios= ratio_tiempo_boxes_total(datos)
    print(f"Los ratios del tiempo en boxes son:")
    for nombre, fecha, ratio in ratios:
        print(f"{nombre},{fecha},{round(ratio, 3)}")

def puntos_piloto_anyos_test(datos):
    print(puntos_piloto_anyos(datos))

def mejor_escuderia_anyo_test(datos):
    print(mejor_escuderia_anyo(datos,2022))

if __name__ == "__main__":

    datos=lee_carreras("./data/f1.csv")

    #lectura_test()
    #media_t_test(datos)
    #pilotos_menor_tiempo_medio_vueltas_top_test(datos, 4)
    ratios_test(datos)
    #puntos_piloto_anyos_test(datos)
    #mejor_escuderia_anyo_test(datos)