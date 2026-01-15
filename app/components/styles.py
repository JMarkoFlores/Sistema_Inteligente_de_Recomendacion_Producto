"""
Estilos CSS profesionales para la aplicación
"""
from config.settings import THEME_COLORS, GRADIENTS

def get_custom_css():
    """Retorna CSS personalizado profesional"""
    return f"""
    <style>
    /* ============================================ */
    /* VARIABLES Y RESET */
    /* ============================================ */
    :root {{
        --primary: {THEME_COLORS['primary']};
        --secondary: {THEME_COLORS['secondary']};
        --success: {THEME_COLORS['success']};
        --warning: {THEME_COLORS['warning']};
        --danger: {THEME_COLORS['danger']};
        --info: {THEME_COLORS['info']};
        --dark: {THEME_COLORS['dark']};
        --light: {THEME_COLORS['light']};
    }}
    
    /* ============================================ */
    /* LAYOUT GENERAL */
    /* ============================================ */
    .main {{
        padding: 1rem 2rem;
        background: linear-gradient(to bottom, #f9fafb 0%, #ffffff 100%);
    }}
    
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }}
    
    /* ============================================ */
    /* TARJETAS Y CONTENEDORES */
    /* ============================================ */
    .card {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }}
    
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }}
    
    .product-card {{
        background: {GRADIENTS['primary']};
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        min-height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: none;
    }}
    
    .product-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }}
    
    .product-card h4 {{
        color: white;
        font-size: 1.2rem;
        margin: 0 0 0.5rem 0;
        font-weight: 700;
        line-height: 1.3;
    }}
    
    .product-card .category {{
        opacity: 0.9;
        font-size: 0.95rem;
        margin: 0.5rem 0;
    }}
    
    .product-card .rating {{
        font-size: 1.3rem;
        margin: 0.5rem 0;
    }}
    
    .product-card .price {{
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFD700;
        margin: 0.5rem 0 0 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    /* ============================================ */
    /* MÉTRICAS */
    /* ============================================ */
    div[data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
    }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 1rem;
        font-weight: 600;
        color: var(--dark);
    }}
    
    div[data-testid="metric-container"] {{
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }}
    
    /* ============================================ */
    /* BOTONES */
    /* ============================================ */
    .stButton > button {{
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
    }}
    
    .stButton > button[kind="primary"] {{
        background: {GRADIENTS['primary']};
        color: white;
    }}
    
    .stButton > button[kind="secondary"] {{
        background: white;
        color: var(--primary);
        border: 2px solid var(--primary);
    }}
    
    /* ============================================ */
    /* INPUTS Y FORMS */
    /* ============================================ */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {{
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}
    
    /* ============================================ */
    /* TABS */
    /* ============================================ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 3rem;
        background: transparent;
        border-radius: 10px;
        color: var(--dark);
        font-weight: 600;
        padding: 0 2rem;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: var(--light);
        color: var(--primary);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {GRADIENTS['primary']};
        color: white !important;
    }}
    
    /* ============================================ */
    /* SIDEBAR */
    /* ============================================ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: white;
    }}
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {{
        color: white !important;
        font-weight: 600;
    }}
    
    /* ============================================ */
    /* ALERTAS */
    /* ============================================ */
    .stAlert {{
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    
    /* ============================================ */
    /* DATAFRAME Y TABLAS */
    /* ============================================ */
    .dataframe {{
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }}
    
    /* ============================================ */
    /* EXPANDER */
    /* ============================================ */
    .streamlit-expanderHeader {{
        background: white;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .streamlit-expanderHeader:hover {{
        border-color: var(--primary);
        background: var(--light);
    }}
    
    /* ============================================ */
    /* ANIMACIONES */
    /* ============================================ */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .card, .product-card, div[data-testid="metric-container"] {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    /* ============================================ */
    /* SCROLLBAR PERSONALIZADA */
    /* ============================================ */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {GRADIENTS['primary']};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--secondary);
    }}
    
    /* ============================================ */
    /* RESPONSIVE */
    /* ============================================ */
    @media (max-width: 768px) {{
        .product-card {{
            min-height: 220px;
        }}
        
        div[data-testid="column"] {{
            padding: 0 0.5rem !important;
        }}
    }}
    </style>
    """