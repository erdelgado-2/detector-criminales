# Detector de mascotas

Este es un simple proyecto de computer vision demostrando como se podrían detectar mascotas y generar alertas a los dueños.
El proyecto esta diseñado de forma que pueda correr en tiempo real.

Utiliza un modelo fine-tuneado de YOLO 11 con 63 imagenes para detectar al perro, OpenCV para transformar pixeles a centimetros, y codigo adicional para manejar los estados, permitiendo ejecutar funciones ante eventos determinados y agregando robustez ante errores del detector.

## Features
Puede ejecutarse en tiempo real 
BLA BLA

![video](./raw_videos/perro.mp4)

## Estructura del proyecto

main.ipynb
Cuaderno con la función principal que procesa streams de videos.

model 
Carpeta con el modelo entrenado

drawing
Funciones para dibujar los frames

creature_detector
Funciones para medir la distancia del perro respecto a una linea imaginaria

pespective_transformer
Funciones para realizar transformaciones de perspectiva, permitiendo calcular distancias reales

state_keeper
Funciones para mantener un estado interno, permiten ejecutar funciones ante ciertos eventos.

raw_videos
Carpeta con videos de ejemplo

output_videos
Carpeta con videos de ejemplo procesados
