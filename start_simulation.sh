#Miguel Rosas

# Verifica si se proporciona la cantidad_simulaciones como argumento
if [ $# -eq 0 ]; then
	echo "Uso: $0 cantidad_simulaciones"
	exit 1
fi

# Obtiene la cantidad_simulaciones desde el primer argumento
cantidad_simulaciones=$1

# Leer valores desde el archivo parametros.txt
rd=$(grep -oP 'rd\s*=\s*\K[\d.+-]+' parametros.txt)
a=$(grep -oP 'a\s*=\s*\K[\d.+-]+' parametros.txt)
rp=$(grep -oP 'rp\s*=\s*\K[\d.+-]+' parametros.txt)
np=$(grep -oP 'np\s*=\s*\K[\d.+-]+' parametros.txt)

touch puntos.csv

# Bucle para crear y mover carpetas, editar y genrar mallado
for ((i = 1; i <= $cantidad_simulaciones; i++)); do
	# Genera el nombre de la carpeta
	carpeta_caso_i="Case_$i"

	# Crea la carpeta del caso
	mkdir "$carpeta_caso_i"

	# Copia carpetas del caso dentro de las carpetasgeneradas
	cp "Case_0/verificador.py" ./
	cp -r "Case_0/geometry_script/" "$carpeta_caso_i/"
	cd "$carpeta_caso_i/"

	# Reemplazar valores en sus respectivos archivos
	sed -i "s/\$npp/$np/g" ./geometry_script/generator_point_process.py
	sed -i "s/\$rpp/$rp/g" ./geometry_script/generator_point_process.py
	sed -i "s/\$rpp/$rp/g" ../verificador.py
	sed -i "s/\$rdd/$rd/g" ./geometry_script/generator_point_process.py
	sed -i "s/\$rdd/$rd/g" ../verificador.py

	cd "./geometry_script/"
	#Generar mallado gmsh
	python3 generator_point_process.py
	mv conteo_puntos.txt ../
	mv puntos.csv ../
	cd ../
	awk '{print}' puntos.csv >>../puntos.csv
	cd ../
done

echo "Proceso completado."
