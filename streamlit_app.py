import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cmath
from io import BytesIO
import requests
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Analisador de Circuito RLC - MISTO", layout="wide")

# Configuração de estilo CSS para alinhamento perfeito
st.markdown("""
<style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
        gap: 1rem;
    }
    .header-container {
        margin-bottom: 2rem;
    }
    .title-container {
        padding-right: 1rem;
    }
    .image-container {
        display: flex;
        justify-content: flex-end;
    }
</style>
""", unsafe_allow_html=True)

# Carregar imagem do circuito
img_url = "https://i.imgur.com/Jh8awva.png"  # Substitua pelo seu link direto
try:
    circuit_image = Image.open(requests.get(img_url, stream=True).raw)
except:
    circuit_image = None

# Container principal do cabeçalho
header_container = st.container()
with header_container:
    # Layout com colunas (5:1 ratio)
    col_title, col_img = st.columns([5, 1])
    
    with col_title:
        st.markdown('<div class="title-container">', unsafe_allow_html=True)
        st.title("🔍 Analisador de Circuito RLC MISTO")
        st.markdown("""
        **Aplicativo web para análise de circuitos RLC MISTO**  
        *Desenvolvido para Trabalho Acadêmico*
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_img:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        if circuit_image:
            st.image(circuit_image, width=180, use_column_width=False)
        else:
            st.image(img_url, width=180, use_column_width=False)
        st.markdown('</div>', unsafe_allow_html=True)

# Funções auxiliares
def format_fasor(z):
    return f"{abs(z):.2f} ∠ {np.degrees(cmath.phase(z)):.2f}°"

def format_retangular(z):
    return f"{z.real:.2f} + {z.imag:.2f}j"

def plot_fasores(fasores, labels, title):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='polar')
    max_mag = max([abs(f) for f in fasores])
    
    for i, (fasor, label) in enumerate(zip(fasores, labels)):
        mag = abs(fasor) / max_mag * 0.8
        angle = cmath.phase(fasor)
        ax.arrow(angle, 0, 0, mag, alpha=0.7, width=0.015,
                 edgecolor='black', facecolor=plt.cm.tab10(i), lw=2,
                 label=f"{label} ({format_fasor(fasor)})")
        ax.text(angle, mag/2, label, ha='center', va='bottom')
    
    ax.set_rmax(1.0)
    ax.set_title(title, pad=20)
    ax.legend(bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)
    
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    st.image(buf)

# Entrada de dados na sidebar
with st.sidebar:
    st.header("🔧 Parâmetros do Circuito")
    f = st.number_input("Frequência (Hz)", min_value=1.0, value=1000.0, step=100.0)
    omega = 2 * np.pi * f
    
    st.subheader("Componentes")
    col1, col2 = st.columns(2)
    with col1:
        C = st.number_input("Capacitância (µF)", min_value=0.01, value=1.0) * 1e-6
        R1 = st.number_input("Resistência R1 (Ω)", min_value=1.0, value=1000.0)
        R2 = st.number_input("Resistência R2 (Ω)", min_value=1.0, value=2000.0)
    with col2:
        L = st.number_input("Indutância (µH)", min_value=1.0, value=1000.0) * 1e-6
        R3 = st.number_input("Resistência R3 (Ω)", min_value=1.0, value=3000.0)
    
    st.subheader("Tensão de Referência")
    v_format = st.radio("Formato", ["Polar", "Retangular"], index=0)
    
    if v_format == "Polar":
        v_mag = st.number_input("Tensão (V)", min_value=1.0, value=10.0)
        v_phase = st.number_input("Fase (θ)", value=0.0)
        V_ref = cmath.rect(v_mag, np.radians(v_phase))
    else:
        v_real = st.number_input("Parte real (V)", value=10.0)
        v_imag = st.number_input("Parte imaginária (j)", value=0.0)
        V_ref = complex(v_real, v_imag)

# Cálculos
Z_C = 1 / (1j * omega * C)
Z_R1 = R1
Z_R2 = R2
Z_ramo1 = Z_C + Z_R1 + Z_R2
Z_L = 1j * omega * L
Z_ramo2 = R3 + Z_L
Z_total = 1 / (1/Z_ramo1 + 1/Z_ramo2)

I_total = V_ref / Z_total
I_ramo1 = V_ref / Z_ramo1
I_ramo2 = V_ref / Z_ramo2

V_C = I_ramo1 * Z_C
V_R1 = I_ramo1 * R1
V_R2 = I_ramo1 * R2
V_R3 = I_ramo2 * R3
V_L = I_ramo2 * Z_L

# Exibição dos resultados
st.header("📈 Resultados da Análise")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Impedâncias")
    st.metric("Z Ramo 1 (C+R1+R2)", format_fasor(Z_ramo1))
    st.metric("Z Ramo 2 (R3+L)", format_fasor(Z_ramo2))
    st.metric("Z Total", format_fasor(Z_total))

with col2:
    st.subheader("Correntes")
    st.metric("I Total", format_fasor(I_total))
    st.metric("I Ramo 1", format_fasor(I_ramo1))
    st.metric("I Ramo 2", format_fasor(I_ramo2))

st.subheader("Tensões nos Componentes")
cols = st.columns(5)
with cols[0]: st.metric("V_C", format_fasor(V_C))
with cols[1]: st.metric("V_R1", format_fasor(V_R1))
with cols[2]: st.metric("V_R2", format_fasor(V_R2))
with cols[3]: st.metric("V_R3", format_fasor(V_R3))
with cols[4]: st.metric("V_L", format_fasor(V_L))

# Gráficos
st.header("📊 Diagramas Fasoriais")
plot_fasores([V_ref, V_C, V_R1, V_R2, V_R3, V_L], 
             ["V_ref", "V_C", "V_R1", "V_R2", "V_R3", "V_L"],
             "Diagrama Fasorial de Tensões")

plot_fasores([I_total, I_ramo1, I_ramo2],
             ["I_total", "I_ramo1", "I_ramo2"],
             "Diagrama Fasorial de Correntes")

# Rodapé
st.markdown("---")
st.caption("João Guilherme | Flávio H. | Mikhaelly M. | Gustavo H. \\\n Circuitos II - Engenharia Elétrica | 2025-1")