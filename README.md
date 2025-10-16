# 📊 Análisis Predictivo de Clientes y Promociones

Aplicación web interactiva desarrollada con Streamlit para analizar el comportamiento de recompra de clientes basándose en promociones y características demográficas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Características

- **Análisis Exploratorio de Datos**: Visualización completa del dataset con estadísticas descriptivas
- **Modelo Predictivo**: Árbol de decisión para predecir la probabilidad de recompra
- **Visualizaciones Interactivas**: Gráficos dinámicos para análisis de factores clave
- **Matriz de Confusión**: Evaluación del rendimiento del modelo
- **Insights Estratégicos**: Recomendaciones basadas en los resultados del análisis

## 🚀 Demo

[Ver aplicación en vivo](https://recompra-informe.streamlit.app/)

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Ejecuta la aplicación:
```bash
streamlit run app.py
```

2. Abre tu navegador en `http://localhost:8501`

3. Sube tu archivo Excel con los datos de clientes

## 📊 Formato de Datos

El archivo Excel debe contener las siguientes columnas:

| Columna | Descripción | Tipo | Ejemplo |
|---------|-------------|------|---------|
| `Cliente_ID` | Identificador único del cliente | Numérico | 1001 |
| `Genero` | Género del cliente | Texto | F, M, Femenino, Masculino |
| `Edad` | Edad del cliente | Numérico | 35 |
| `Ingreso` | Ingreso del cliente | Numérico | 45000 |
| `Recibio_Promo` | Si recibió promoción | Texto | Si, No, Sí |
| `Monto_Promo` | Monto de la promoción | Numérico | 150 |
| `Recompra` | Si realizó recompra | Texto | Si, No, Sí |

### Ejemplo de datos:

```
Cliente_ID,Genero,Edad,Ingreso,Recibio_Promo,Monto_Promo,Recompra
1001,F,35,45000,Si,150,Si
1002,M,28,32000,No,0,No
1003,F,42,58000,Si,200,Si
```

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para la aplicación web
- **Pandas**: Manipulación y análisis de datos
- **Scikit-learn**: Modelo de machine learning (Decision Tree)
- **Matplotlib & Seaborn**: Visualizaciones
- **NumPy**: Operaciones numéricas

## 📈 Funcionalidades Principales

### 1. Exploración de Datos
- Vista previa del dataset
- Estadísticas descriptivas
- Métricas clave (total clientes, tasa de recompra, etc.)
- Distribuciones de variables

### 2. Modelo Predictivo
- Entrenamiento de árbol de decisión
- Matriz de confusión con heatmap
- Métricas de rendimiento (Accuracy, Precision, Recall)
- Importancia de variables

### 3. Insights y Recomendaciones
- Análisis de impacto de promociones
- Correlación entre monto y recompra
- Perfil demográfico óptimo
- Recomendaciones estratégicas

## 📁 Estructura del Proyecto

```
.
├── app.py                  # Aplicación principal de Streamlit
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
└── data/                  # Carpeta para datos de ejemplo (opcional)
    └── ejemplo_clientes.xlsx
```

## 👤 Autor

Bayaslian Santiago
- GitHub: [@Bayaslian_Santiago](https://github.com/BayaslianSantiago/)

## 🙏 Agradecimientos

- El Instituto Tecnologico Beltran y a los profesores por los recursos y su dedicación.
- Streamlit por su excelente framework
- La comunidad de Python y Data Science

---

⭐️ Si te gustó este proyecto, dale una estrella en GitHub!
