import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Leer los puntos del archivo CSV
puntos = []
with open("puntos.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        puntos.append((float(row[0]), float(row[1])))

# Definir el número de celdas (bins) para la prueba de Chi-cuadrado
num_bins = 50
radio = $rdd - 2 * $rpp

# Crear una cuadrícula de celdas en el círculo
x_bins = np.linspace(-radio, radio, num_bins + 1)
y_bins = np.linspace(-radio, radio, num_bins + 1)

# Contar cuántos puntos caen en cada celda
hist, x_edges, y_edges = np.histogram2d(
    [p[0] for p in puntos], [p[1] for p in puntos], bins=[x_bins, y_bins]
)

# Agregar un valor pequeño a todas las celdas del histograma para evitar frecuencias esperadas de cero
hist += 1e-6

# Calcular el estadístico de Chi-cuadrado y el p-valor
chi2, p_value, _, _ = chi2_contingency(hist)

# Mostrar resultados
print(f"Estadístico de Chi-cuadrado: {chi2}")
print(f"p-valor: {p_value}")

# Visualizar la distribución de los puntos y la cuadrícula
plt.figure(figsize=(8, 8))
plt.hist2d(
    [p[0] for p in puntos], [p[1] for p in puntos], bins=[x_bins, y_bins], cmap="Blues"
)
plt.colorbar(label="Número de puntos")

# Dibujar el círculo
circle = plt.Circle((0, 0), radio, color="r", fill=False)
plt.gca().add_artist(circle)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Distribución de los puntos en el círculo")
plt.axis("equal")
plt.show()

# Verificar si la distribución es uniforme
if p_value > 0.05:
    print(
        "La distribución de los puntos es uniforme (no se rechaza la hipótesis nula)."
    )
else:
    print(
        "La distribución de los puntos no es uniforme (se rechaza la hipótesis nula)."
    )
