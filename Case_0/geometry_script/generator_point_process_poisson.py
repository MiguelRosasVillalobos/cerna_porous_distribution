import random
import math
import csv
import matplotlib.pyplot as plt

def generar_puntos_poisson(num_puntos, radio, distancia_minima):
    def calcular_distancia(punto1, punto2):
        return math.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)

    def en_circulo(punto, radio):
        return math.sqrt(punto[0]**2 + punto[1]**2) <= radio

    grid_size = distancia_minima / math.sqrt(2)
    grid_width = int(math.ceil((2 * radio) / grid_size))
    grid = [[None for _ in range(grid_width)] for _ in range(grid_width)]

    puntos = []
    lista_activa = []

    # Primer punto
    primer_punto = (random.uniform(-radio, radio), random.uniform(-radio, radio))
    while not en_circulo(primer_punto, radio):
        primer_punto = (random.uniform(-radio, radio), random.uniform(-radio, radio))

    puntos.append(primer_punto)
    lista_activa.append(primer_punto)
    grid_x = int((primer_punto[0] + radio) / grid_size)
    grid_y = int((primer_punto[1] + radio) / grid_size)
    grid[grid_x][grid_y] = primer_punto

    while lista_activa and len(puntos) < num_puntos:
        indice_activo = random.randint(0, len(lista_activa) - 1)
        punto_activo = lista_activa[indice_activo]
        nuevo_punto_valido = False

        for _ in range(30):  # Intentar hasta 30 veces
            angulo = random.uniform(0, 2 * math.pi)
            distancia = random.uniform(distancia_minima, 2 * distancia_minima)
            nuevo_punto = (
                punto_activo[0] + distancia * math.cos(angulo),
                punto_activo[1] + distancia * math.sin(angulo)
            )

            if en_circulo(nuevo_punto, radio):
                grid_x = int((nuevo_punto[0] + radio) / grid_size)
                grid_y = int((nuevo_punto[1] + radio) / grid_size)

                if 0 <= grid_x < grid_width and 0 <= grid_y < grid_width and grid[grid_x][grid_y] is None:
                    valido = True
                    for i in range(max(0, grid_x - 2), min(grid_width, grid_x + 3)):
                        for j in range(max(0, grid_y - 2), min(grid_width, grid_y + 3)):
                            vecino = grid[i][j]
                            if vecino is not None and calcular_distancia(nuevo_punto, vecino) < distancia_minima:
                                valido = False
                                break
                        if not valido:
                            break

                    if valido:
                        puntos.append(nuevo_punto)
                        lista_activa.append(nuevo_punto)
                        grid[grid_x][grid_y] = nuevo_punto
                        nuevo_punto_valido = True
                        break

        if not nuevo_punto_valido:
            lista_activa.pop(indice_activo)

    # Intentar llenar puntos faltantes con método aleatorio
    while len(puntos) < num_puntos:
        x = random.uniform(-radio, radio)
        y = random.uniform(-radio, radio)
        if en_circulo((x, y), radio):
            agregar_punto = True
            for punto_existente in puntos:
                if calcular_distancia((x, y), punto_existente) < distancia_minima:
                    agregar_punto = False
                    break
            if agregar_punto:
                puntos.append((x, y))

    return puntos

num_puntos = $npp
radio = $rdd - 2*$rpp
distancia_minima = 2*$rpp

puntos_generados = generar_puntos_poisson(num_puntos, radio, distancia_minima)

# Extraer coordenadas x, y de los puntos generados y de la circunferencia
x_coords = [p[0] for p in puntos_generados]
y_coords = [p[1] for p in puntos_generados]

# Guardar puntos en un archivo CSV
with open("./puntos.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    for punto in puntos_generados:
        writer.writerow([punto[0], punto[1]])

# Guardar conteos en un archivo de texto
with open("./conteo_puntos.txt", mode="w") as file:
    file.write(f"Puntos generados: {len(puntos_generados)}\n")
