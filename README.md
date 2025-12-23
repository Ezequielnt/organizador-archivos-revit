# 🏗️ Organizador de Archivos Revit

Aplicación de escritorio desarrollada en Python para automatizar la clasificación de archivos de arquitectura (.rfa y .rvt).

## 🚀 Funcionalidades
- **Interfaz Gráfica (GUI):** Fácil de usar, sin línea de comandos.
- **Configurable:** Utiliza un archivo `reglas_revit.json` para que el usuario defina sus propias categorías y palabras clave.
- **Detección Inteligente:** Localiza automáticamente el Escritorio y Documentos, compatible con OneDrive.
- **Portátil:** Compilado en `.exe`, no requiere instalación de Python.

## 🛠️ Tecnologías
- Python 3.12
- Tkinter (UI)
- JSON (Configuración)
- Shutil/OS (Gestión de archivos)
- PyInstaller (Compilación)

## 📦 Instalación y Uso
1. Ve a la sección de [Releases](LINK_A_TU_REPO/releases) y descarga la última versión.
2. Descomprime el archivo ZIP.
3. Ejecuta `OrganizadorRevit.exe`.
4. Haz clic en "Ordenar Ahora".

## 📝 Personalización
Al ejecutar el programa por primera vez, se creará un archivo `reglas_revit.json`. Puedes editarlo para agregar nuevas categorías:

```json
"Techos": ["roof", "tejado", "cubierta"]
```

---
Desarrollado por [Tu Nombre]