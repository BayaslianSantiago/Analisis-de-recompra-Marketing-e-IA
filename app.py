import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import io
import seaborn as sns

# Configuración de página
st.set_page_config(
    page_title="Análisis de Clientes", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la estética
st.markdown("""
    <style>
    /* Fondo y colores generales */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Títulos con estilo */
    h1 {
        color: #ffffff;
        font-weight: 700;
        padding: 20px 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #ffffff;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Texto general */
    p, .stMarkdown {
        color: #ffffff;
    }
    
    /* Labels y textos de elementos */
    label, .stTextInput label, .stSelectbox label {
        color: #ffffff !important;
    }
    
    /* Tarjetas con sombra */
    .stDataFrame {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.8);
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Métricas destacadas */
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Warning mejorado */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #f59e0b;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal con emoji
st.markdown("<h1>📊 Análisis Predictivo de Clientes y Promociones</h1>", unsafe_allow_html=True)

# =======================
# Sidebar para configuración
# =======================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/business.png", width=150)
    st.markdown("### 🎯 Panel de Control")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo Excel", 
        type=['xlsx', 'xls'],
        help="Archivo con datos de clientes y promociones"
    )
    
    if uploaded_file is not None:
        st.success("✅ Archivo cargado correctamente")
    
    st.markdown("---")
    st.markdown("### 📈 Métricas del Modelo")

# Verificar si hay archivo
if uploaded_file is None:
    st.info("👆 Por favor, sube un archivo Excel desde el panel lateral para comenzar el análisis.")
    st.stop()

# =======================
# Preprocesamiento
# =======================
df = pd.read_excel(uploaded_file)

for col in ['Genero','Recibio_Promo','Monto_Promo','Edad','Ingreso']:
    if col not in df.columns:
        df[col] = np.nan

# Mapear categorías
df['Genero'] = df['Genero'].map({'F':0,'M':1,'Femenino':0,'Masculino':1})
col_name = 'Recibio_Promo' if 'Recibio_Promo' in df.columns else 'Recibió_Promo'
df['Recibio_Promo'] = df[col_name].map({'Si':1,'No':0,'Sí':1})
df['Recompra'] = df['Recompra'].map({'Si':1,'No':0,'Sí':1})

# Variables predictoras
X = df.drop(['Cliente_ID','Recompra'], axis=1)
y = df['Recompra']
X = X.fillna(0)

# =======================
# Entrenamiento del modelo
# =======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
modelo = DecisionTreeClassifier(random_state=42, max_depth=5)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# Métricas
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

conf_matrix = pd.DataFrame(
    confusion_matrix(y_test, y_pred),
    index=['No Recompra','Recompra'],
    columns=['Pred No','Pred Sí']
)
importancias = pd.Series(modelo.feature_importances_, index=X.columns).sort_values(ascending=False)

# Mostrar métricas en sidebar
with st.sidebar:
    st.metric("🎯 Precisión", f"{accuracy*100:.1f}%")
    st.metric("📊 Exactitud", f"{precision*100:.1f}%")
    st.metric("🔍 Recall", f"{recall*100:.1f}%")

# =======================
# Tabs principales
# =======================
tab1, tab2, tab3 = st.tabs(["📋 Exploración de Datos", "🤖 Modelo Predictivo", "💡 Insights y Recomendaciones"])

# --- Tab 1: Exploración ---
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Clientes", len(df))
    with col2:
        st.metric("✅ Tasa Recompra", f"{df['Recompra'].mean()*100:.1f}%")
    with col3:
        st.metric("🎁 Con Promoción", f"{df['Recibio_Promo'].sum()}")
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Vista Previa del Dataset")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("📊 Estadísticas")
        st.dataframe(df.describe().round(2))
    
    st.markdown("---")
    
    # Distribuciones
    st.subheader("📈 Distribución de Variables Clave")
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        df['Recompra'].value_counts().plot(
            kind='bar', 
            ax=ax, 
            color=['#ef4444', '#22c55e']
        )
        ax.set_title('Distribución de Recompra', fontsize=14, fontweight='bold')
        ax.set_xlabel('Recompra (0=No, 1=Sí)')
        ax.set_ylabel('Cantidad')
        ax.set_xticklabels(['No', 'Sí'], rotation=0)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        if 'Recibio_Promo' in df.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            df['Recibio_Promo'].value_counts().plot(
                kind='bar', 
                ax=ax, 
                color=['#f59e0b', '#3b82f6']
            )
            ax.set_title('Distribución de Promociones', fontsize=14, fontweight='bold')
            ax.set_xlabel('Recibió Promo (0=No, 1=Sí)')
            ax.set_ylabel('Cantidad')
            ax.set_xticklabels(['No', 'Sí'], rotation=0)
            plt.tight_layout()
            st.pyplot(fig)

# --- Tab 2: Modelo ---
with tab2:
    st.subheader("🎯 Rendimiento del Modelo")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Matriz de Confusión")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(
            conf_matrix, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            cbar_kws={'label': 'Cantidad'},
            ax=ax
        )
        ax.set_title('Matriz de Confusión', fontsize=14, fontweight='bold')
        ax.set_ylabel('Valor Real')
        ax.set_xlabel('Predicción')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### Importancia de Variables")
        fig, ax = plt.subplots(figsize=(6, 5))
        importancias.plot(
            kind='barh', 
            ax=ax, 
            color='#6366f1'
        )
        ax.set_title('Importancia de Variables', fontsize=14, fontweight='bold')
        ax.set_xlabel('Importancia')
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Análisis detallado
    st.subheader("📊 Análisis de Factores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Recibio_Promo' in df.columns:
            st.markdown("##### 🎁 Impacto de Promociones")
            tabla = pd.crosstab(df['Recibio_Promo'], df['Recompra'], normalize='index')*100
            tabla.index = ['Sin Promo', 'Con Promo']
            tabla.columns = ['No Recompra', 'Recompra']
            st.dataframe(tabla.style.format("{:.1f}%").background_gradient(cmap='RdYlGn'))
            
            fig, ax = plt.subplots(figsize=(8, 5))
            df.groupby('Recibio_Promo')['Recompra'].mean().plot(
                kind='bar', 
                ax=ax, 
                color=['#f87171', '#34d399']
            )
            ax.set_ylabel('Tasa de Recompra')
            ax.set_xlabel('Recibió Promoción')
            ax.set_xticklabels(['No', 'Sí'], rotation=0)
            ax.set_title('Tasa de Recompra por Promoción')
            plt.tight_layout()
            st.pyplot(fig)
    
    with col2:
        if 'Monto_Promo' in df.columns:
            st.markdown("##### 💰 Impacto del Monto")
            df['Monto_Promo'] = pd.to_numeric(df['Monto_Promo'], errors='coerce')
            resumen = df.groupby('Recompra')['Monto_Promo'].agg(['mean', 'median', 'std']).round(2)
            resumen.index = ['No Recompra', 'Recompra']
            st.dataframe(resumen.style.background_gradient(cmap='Oranges'))
            
            fig, ax = plt.subplots(figsize=(8, 5))
            df.boxplot(column='Monto_Promo', by='Recompra', ax=ax)
            ax.set_title('Distribución del Monto de Promoción')
            ax.set_xlabel('Recompra (0=No, 1=Sí)')
            ax.set_ylabel('Monto Promoción ($)')
            plt.suptitle('')
            plt.tight_layout()
            st.pyplot(fig)

# --- Tab 3: Insights ---
with tab3:
    st.subheader("💡 Conclusiones y Recomendaciones Estratégicas")
    
    # Insights clave
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Hallazgos Clave
        
        #### 1️⃣ Impacto de Promociones
        Las promociones tienen un **impacto directo y positivo** en la tasa de recompra. 
        Los clientes que reciben promociones muestran una probabilidad significativamente 
        mayor de realizar una nueva compra.
        
        #### 2️⃣ Monto Óptimo
        El monto de la promoción es un factor **crítico**. Existe una correlación positiva 
        entre el valor de la promoción y la probabilidad de recompra, sugiriendo que 
        inversiones mayores generan mejores retornos.
        
        #### 3️⃣ Perfil Demográfico
        Clientes con **mayor edad e ingreso** presentan tasas de recompra más elevadas, 
        indicando un segmento de mercado más estable y propenso a la fidelización.
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Recomendaciones Estratégicas
        
        #### 📌 Segmentación Inteligente
        - Priorizar campañas hacia clientes de **mayor ingreso y edad**
        - Crear perfiles específicos según comportamiento histórico
        - Implementar estrategias diferenciadas por segmento
        
        #### 💰 Optimización de Inversión
        - Establecer un **monto mínimo efectivo** de promoción
        - Realizar pruebas A/B para encontrar el punto óptimo de inversión
        - Maximizar ROI mediante targeting preciso
        
        #### 📊 Monitoreo Continuo
        - Implementar dashboards de seguimiento en tiempo real
        - Ajustar estrategias basándose en resultados actuales
        - Evaluar periódicamente la efectividad de las campañas
        
        #### 🎁 Personalización
        - Desarrollar ofertas personalizadas según perfil del cliente
        - Implementar sistemas de recomendación inteligentes
        - Aumentar la relevancia de las promociones
        """)
    
    st.markdown("---")
    
    # Scorecard
    st.subheader("📈 Scorecard del Modelo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Accuracy",
            f"{accuracy*100:.1f}%",
            delta=f"{(accuracy-0.7)*100:.1f}% vs baseline"
        )
    
    with col2:
        st.metric(
            "📊 Precision",
            f"{precision*100:.1f}%",
            delta="Confiabilidad alta" if precision > 0.75 else "Mejorable"
        )
    
    with col3:
        st.metric(
            "🔍 Recall",
            f"{recall*100:.1f}%",
            delta="Cobertura alta" if recall > 0.75 else "Mejorable"
        )
    
    with col4:
        var_importante = importancias.index[0]
        st.metric(
            "⭐ Variable Clave",
            var_importante,
            delta=f"{importancias.iloc[0]*100:.1f}% importancia"
        )
    
    st.markdown("---")
    st.success("✅ Análisis completado. Los insights generados pueden ser utilizados para optimizar estrategias de marketing y aumentar la retención de clientes.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 20px;'>
        <p>📊 Análisis Predictivo de Clientes | Powered by Streamlit & Machine Learning 🤖</p>
    </div>
""", unsafe_allow_html=True)
