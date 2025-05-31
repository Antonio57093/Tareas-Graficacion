# md.py

```python
import os

# Carpeta con los .py
carpeta_origen = "."
# Carpeta donde guardar los .md
carpeta_destino = "markdowns"

# Crea la carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Convierte cada .py a .md
for archivo in os.listdir(carpeta_origen):
    if archivo.endswith(".py"):
        ruta_py = os.path.join(carpeta_origen, archivo)
        nombre_sin_extension = os.path.splitext(archivo)[0]
        ruta_md = os.path.join(carpeta_destino, f"{nombre_sin_extension}.md")
        
        with open(ruta_py, "r", encoding="utf-8") as f_py:
            contenido = f_py.read()
        
        contenido_md = f"# {archivo}\n\n```python\n{contenido}\n```"
        
        with open(ruta_md, "w", encoding="utf-8") as f_md:
            f_md.write(contenido_md)

print("✅ Archivos .py convertidos a .md y guardados en la carpeta 'markdowns'.")

```