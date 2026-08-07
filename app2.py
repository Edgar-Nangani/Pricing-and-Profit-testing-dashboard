import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import root
import plotly.graph_objects as go
import plotly.express as px
import time
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Unit-Linked Endowment Microinsurance Pricing Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS - Dark Sidebar with White Text
# =============================================================================
st.markdown("""
<style>
    /* Main background - light */
    .stApp {
        background: linear-gradient(145deg, #f0f4f8 0%, #e8edf3 50%, #dfe6ef 100%);
    }
    
    /* Sidebar - Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a2d4a 50%, #0a1628 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    /* ALL sidebar text - white */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        opacity: 1 !important;
        filter: none !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stSlider .stMarkdown,
    [data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] div {
        color: #ffffff !important;
        opacity: 1 !important;
        filter: none !important;
    }
    
    /* Sidebar select box */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Sidebar number input - White background with dark purple text */
    [data-testid="stSidebar"] .stNumberInput > div > div {
        background-color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput input {
        color: #4a1a6b !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput div[data-baseweb="input"] input {
        color: #4a1a6b !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar slider */
    [data-testid="stSidebar"] .stSlider > div > div > div {
        background-color: #3b82f6 !important;
    }
    
    /* Sidebar headers */
    .sidebar-header {
        color: #ffffff !important;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
        opacity: 1 !important;
        filter: none !important;
        letter-spacing: 0.3px;
    }
    
    /* Sidebar expander - White text */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff !important;
        opacity: 1 !important;
        filter: none !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        color: #ffffff !important;
        opacity: 1 !important;
        filter: none !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent label {
        color: #ffffff !important;
        opacity: 1 !important;
        filter: none !important;
    }
    
    /* Sidebar slider value display */
    [data-testid="stSidebar"] .stSlider .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Sidebar button */
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
    }
    
    /* Circular Progress Cards */
    .circular-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1.2rem 0.5rem;
        border-radius: 50%;
        width: 100%;
        aspect-ratio: 1/1;
        background: rgba(255, 255, 255, 0.9);
        border: 3px solid rgba(37, 99, 235, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        position: relative;
        text-align: center;
        transition: all 0.3s ease;
    }
    .circular-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(37, 99, 235, 0.12);
    }
    
    .circular-card .label {
        color: #64748b;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }
    .circular-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.2;
    }
    .circular-card .sub {
        color: #94a3b8;
        font-size: 0.6rem;
        margin-top: 0.1rem;
    }
    
    /* SVG Circular Progress */
    .progress-ring {
        transform: rotate(-90deg);
        width: 140px;
        height: 140px;
    }
    .progress-ring .bg {
        fill: none;
        stroke: rgba(0, 0, 0, 0.06);
        stroke-width: 10;
    }
    .progress-ring .progress {
        fill: none;
        stroke-width: 10;
        stroke-linecap: round;
        transition: stroke-dasharray 0.8s ease-in-out;
    }
    
    /* Headers - Black */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 0;
        margin-bottom: 0.5rem;
    }
    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #000000;
        letter-spacing: -0.5px;
        text-align: center;
    }
    .sub-title {
        color: #475569;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* Card styles */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons - main */
    .stButton button {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0, 0, 0, 0.06);
    }
    .dataframe thead tr th {
        background: rgba(37, 99, 235, 0.08) !important;
        color: #1e293b !important;
    }
    .dataframe tbody tr td {
        color: #334155 !important;
    }
    .dataframe tbody tr:hover {
        background: rgba(37, 99, 235, 0.03) !important;
    }
    
    /* Expander - main */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        color: #1e293b !important;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.8);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.02);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        border-radius: 10px;
    }
    
    /* Term badge */
    .term-badge {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 1. LOADED PROBABILITIES (AGES 20-70)
# =============================================================================

# Female loaded mortality (qd_f) – ages 20..70
qd_f = [
    0.000456, 0.000756345, 0.001057281, 0.001226782, 0.001083785,  # 20-24
    0.000494260, 0.000711604, 0.000881086, 0.001014746, 0.001076240,  # 25-29
    0.001101610, 0.001139182, 0.001201145, 0.001299769, 0.001410929,  # 30-34
    0.001510365, 0.001646837, 0.001747305, 0.001885006, 0.001986674,  # 35-39
    0.002101219, 0.002204153, 0.002295408, 0.002350167, 0.002417695,  # 40-44
    0.002473268, 0.002529238, 0.002623087, 0.002705128, 0.002800370,  # 45-49
    0.002971943, 0.002993432, 0.002457677, 0.004178185, 0.003647339,  # 50-54
    0.004249473, 0.004756069, 0.005360003, 0.006051136, 0.007067799,  # 55-59
    0.007933863, 0.008806327, 0.009419782, 0.021436580, 0.012395553,  # 60-64
    0.008386057, 0.005074186, 0.017666059, 0.013830334, 0.018894045,  # 65-69
    0.021762029                                                       # 70
]

# Male loaded mortality (qd_m) – ages 20..70
qd_m = [
    0.002868, 0.002670, 0.002484, 0.002313, 0.002100,  # 20-24
    0.002089, 0.001920, 0.001836, 0.001781, 0.001758,  # 25-29
    0.001768, 0.001816, 0.001901, 0.002028, 0.002198,  # 30-34
    0.002407, 0.002648, 0.002917, 0.003206, 0.003511,  # 35-39
    0.003826, 0.004144, 0.004460, 0.004767, 0.005061,  # 40-44
    0.005335, 0.005585, 0.005800, 0.005980, 0.006115,  # 45-49
    0.006200, 0.006366, 0.006496, 0.006675, 0.014012,  # 50-54
    0.007247, 0.015040, 0.008447, 0.009287, 0.010671,  # 55-59
    0.012497, 0.014787, 0.017603, 0.021009, 0.025024,  # 60-64
    0.029912, 0.035481, 0.042015, 0.049572, 0.058215,  # 65-69
    0.065375                                                       # 70
]

# Female loaded disability (qdi_f) – ages 20..70
qdi_f = [
    0.000767, 0.000767, 0.000767, 0.000767, 0.000767,  # 20-24
    0.000767, 0.000767, 0.000767, 0.000767, 0.000780,  # 25-29
    0.000793, 0.000819, 0.000845, 0.000897, 0.000949,  # 30-34
    0.001014, 0.001079, 0.001144, 0.001222, 0.001287,  # 35-39
    0.001365, 0.001456, 0.001573, 0.001703, 0.001859,  # 40-44
    0.002028, 0.002210, 0.002405, 0.002600, 0.002795,  # 45-49
    0.002990, 0.003185, 0.003614, 0.003874, 0.004290,  # 50-54
    0.004706, 0.005122, 0.005538, 0.005954, 0.006370,  # 55-59
    0.006786, 0.007202, 0.007618, 0.008034, 0.008450,  # 60-64
    0.008866, 0.009282, 0.009698, 0.010114, 0.010530,  # 65-69
    0.010946                                             # 70
]

# Male loaded disability (qdi_m) – ages 20..70
qdi_m = [
    0.000611, 0.000611, 0.000611, 0.000611, 0.000611,  # 20-24
    0.000611, 0.000611, 0.000611, 0.000611, 0.000611,  # 25-29
    0.000611, 0.000624, 0.000650, 0.000689, 0.000728,  # 30-34
    0.000767, 0.000819, 0.000871, 0.000923, 0.000975,  # 35-39
    0.001027, 0.001092, 0.001170, 0.001261, 0.001378,  # 40-44
    0.001495, 0.001638, 0.001768, 0.001911, 0.002041,  # 45-49
    0.002184, 0.002314, 0.002470, 0.002600, 0.002730,  # 50-54
    0.002860, 0.002990, 0.003120, 0.003250, 0.003380,  # 55-59
    0.003510, 0.003640, 0.003770, 0.003900, 0.004030,  # 60-64
    0.004160, 0.004290, 0.004420, 0.004550, 0.004680,  # 65-69
    0.004810                                             # 70
]

ages_list = list(range(20, 71))

def get_rates(age, gender='female'):
    idx = ages_list.index(age)
    if gender == 'female':
        return qd_f[idx], qdi_f[idx]
    else:
        return qd_m[idx], qdi_m[idx]

# =============================================================================
# 2. CORE MODEL FUNCTIONS
# =============================================================================

def compute_decrements_excel(qd, qdi, qw):
    n = len(qd)
    aqd = np.zeros(n)
    aqdi = np.zeros(n)
    aqw = np.zeros(n)
    ap = np.zeros(n)
    
    for t in range(n):
        qd_t = qd[t]
        qdi_t = qdi[t]
        qw_t = qw[t]
        
        aqd[t] = qd_t * (1 - 0.5 * (qdi_t + qw_t) + (1/3) * (qdi_t * qw_t))
        aqdi[t] = qdi_t * (1 - 0.5 * (qw_t + qd_t) + (1/3) * (qw_t * qd_t))
        aqw[t] = qw_t * (1 - 0.5 * (qd_t + qdi_t) + (1/3) * (qd_t * qdi_t))
        ap[t] = 1 - (aqd[t] + aqdi[t] + aqw[t])
    
    inforce = np.zeros(n)
    inforce[0] = 1.0
    for t in range(1, n):
        inforce[t] = inforce[t-1] * ap[t-1]
    
    return aqd, aqdi, aqw, ap, inforce

def calculate_unit_fund(premium, term, unit_int=0.155, mgt_charge=0.025,
                        alloc_first=0.95, alloc_other=0.85, bid_offer=0.05):
    fund_end = np.zeros(term)
    alloc = np.zeros(term)
    spread = np.zeros(term)
    cost_alloc = np.zeros(term)
    fund_after = np.zeros(term)
    fund_before = np.zeros(term)
    mgt_fees = np.zeros(term)
    
    for t in range(term):
        if t == 0:
            alloc[t] = alloc_first * float(premium)
        else:
            alloc[t] = alloc_other * float(premium)
        
        spread[t] = bid_offer * alloc[t]
        cost_alloc[t] = alloc[t] - spread[t]
        
        if t == 0:
            fund_after[t] = cost_alloc[t]
        else:
            fund_after[t] = fund_end[t-1] + cost_alloc[t]
        
        fund_before[t] = fund_after[t] * (1 + unit_int)
        mgt_fees[t] = mgt_charge * fund_before[t]
        fund_end[t] = fund_before[t] - mgt_fees[t]
    
    return {
        'fund_end': fund_end,
        'alloc': alloc,
        'spread': spread,
        'mgt_fees': mgt_fees
    }

@st.cache_data(show_spinner=False)
def price_policy(age=30, gender='female', term=5, sa=1500000,
                 init_exp=0.15, init_comm=0.10,
                 inflation=0.032, ren_exp=0.05, ren_comm=0.075):
    
    SA = sa
    disab_ratio = 1.10
    surrender_ratio = 0.70
    i = 0.155
    v = 1 / (1 + i)
    
    qd = np.zeros(term)
    qdi = np.zeros(term)
    qw = np.zeros(term)
    
    for t in range(term):
        qd[t], qdi[t] = get_rates(age + t, gender)
    
    if term > 2:
        qw[1:term-1] = 0.10
    
    aqd, aqdi, aqw, ap, inforce = compute_decrements_excel(qd, qdi, qw)
    
    def epv_benefits(premium):
        fund = calculate_unit_fund(float(np.ravel(premium)[0]), term)
        fund_end = fund['fund_end']
        
        epv_death = np.sum(SA * aqd * (v ** (np.arange(term) + 1)))
        dis_benefits = disab_ratio * fund_end
        epv_dis = np.sum(dis_benefits * aqdi * (v ** (np.arange(term) + 1)))
        
        surr_benefits = np.zeros(term)
        for t in range(term):
            if t >= 3:
                surr_benefits[t] = surrender_ratio * fund_end[t]
        epv_surr = np.sum(surr_benefits * aqw * (v ** (np.arange(term) + 1)))
        
        prob_surv = inforce[term-1]
        epv_surv = SA * prob_surv * (v ** term)
        
        return epv_death + epv_dis + epv_surr + epv_surv
    
    def epv_expenses(premium):
        epv = init_exp * premium * inforce[0] * (v ** 0)
        for t in range(1, term):
            exp_amt = ren_exp * premium * ((1 + inflation) ** t)
            epv += exp_amt * inforce[t] * (v ** t)
        return epv
    
    def epv_commissions(premium):
        epv = init_comm * premium * inforce[0] * (v ** 0)
        for t in range(1, term):
            comm_amt = ren_comm * premium
            epv += comm_amt * inforce[t] * (v ** t)
        return epv
    
    def epv_premium(premium):
        return np.sum([premium * inforce[t] * (v ** t) for t in range(term)])
    
    def equation(premium):
        return epv_premium(premium) - (epv_benefits(premium) + epv_expenses(premium) + epv_commissions(premium))
    
    sol = root(equation, 150000, method='hybr', tol=1e-12)
    premium = sol.x[0]
    
    fund = calculate_unit_fund(float(premium), term)
    fund_end = fund['fund_end']
    
    epv_death_details = SA * aqd * (v ** (np.arange(term) + 1))
    epv_dis_details = (disab_ratio * fund_end) * aqdi * (v ** (np.arange(term) + 1))
    
    surr_benefits = np.zeros(term)
    for t in range(term):
        if t >= 3:
            surr_benefits[t] = surrender_ratio * fund_end[t]
    epv_surr_details = surr_benefits * aqw * (v ** (np.arange(term) + 1))
    
    epv_surv = SA * inforce[term-1] * (v ** term)
    
    epv_death_total = np.sum(epv_death_details)
    epv_dis_total = np.sum(epv_dis_details)
    epv_surr_total = np.sum(epv_surr_details)
    epv_benefits_total = epv_death_total + epv_dis_total + epv_surr_total + epv_surv
    
    final_epv_expenses = epv_expenses(premium)
    final_epv_commissions = epv_commissions(premium)
    final_epv_premium = epv_premium(premium)
    
    return {
        'premium': premium,
        'aqd': aqd, 'aqdi': aqdi, 'aqw': aqw, 'ap': ap, 'inforce': inforce,
        'fund_end': fund_end,
        'epv_death_details': epv_death_details,
        'epv_dis_details': epv_dis_details,
        'epv_surr_details': epv_surr_details,
        'epv_surv': epv_surv,
        'epv_death': epv_death_total,
        'epv_dis': epv_dis_total,
        'epv_surr': epv_surr_total,
        'epv_surv_value': epv_surv,
        'epv_benefits': epv_benefits_total,
        'epv_expenses': final_epv_expenses,
        'epv_commissions': final_epv_commissions,
        'epv_premium': final_epv_premium
    }

@st.cache_data(show_spinner=False)
def profit_test(pricing_result, mgt_charge=0.025, rdr=0.185, unit_int=0.155):
    SA = 1500000
    alloc_first = 0.95
    alloc_other = 0.85
    bid_offer = 0.05
    non_unit_int = 0.155
    disab_ratio = 1.10
    surrender_penalty_rate = 0.30
    extra_maturity_cost_rate = 0.05
    init_exp = 0.15
    ren_exp = 0.05
    init_comm = 0.10
    ren_comm = 0.075
    inflation = 0.032
    
    premium = pricing_result['premium']
    aqd = pricing_result['aqd']
    aqdi = pricing_result['aqdi']
    aqw = pricing_result['aqw']
    ap = pricing_result['ap']
    inforce = pricing_result['inforce']
    term = len(aqd)
    z = 1 / (1 + rdr)
    
    fund = calculate_unit_fund(float(premium), term, unit_int, mgt_charge,
                               alloc_first, alloc_other, bid_offer)
    fund_end = fund['fund_end']
    alloc = fund['alloc']
    spread = fund['spread']
    mgt_fees = fund['mgt_fees']
    
    unalloc = np.zeros(term)
    expenses = np.zeros(term)
    commissions = np.zeros(term)
    interest = np.zeros(term)
    extra_death = np.zeros(term)
    extra_disab = np.zeros(term)
    surrender_penalty = np.zeros(term)
    extra_maturity_cost = np.zeros(term)
    profit = np.zeros(term)
    
    for t in range(term):
        unalloc[t] = premium - alloc[t]
        
        if t == 0:
            expenses[t] = init_exp * premium
        else:
            expenses[t] = ren_exp * premium * ((1 + inflation) ** t)
        
        if t == 0:
            commissions[t] = init_comm * premium
        else:
            commissions[t] = ren_comm * premium
        
        net_cash = unalloc[t] + spread[t] - expenses[t] - commissions[t]
        interest[t] = net_cash * non_unit_int
        
        extra_death[t] = max(SA - fund_end[t], 0) * aqd[t]
        extra_disab[t] = (disab_ratio - 1) * fund_end[t] * aqdi[t]
        surrender_penalty[t] = surrender_penalty_rate * fund_end[t] * aqw[t]
        
        if t == term - 1:
            extra_maturity_cost[t] = extra_maturity_cost_rate * fund_end[t] * ap[t]
        else:
            extra_maturity_cost[t] = 0.0
        
        profit[t] = (unalloc[t] + spread[t] - expenses[t] - commissions[t] + interest[t]
                     - extra_death[t] - extra_disab[t] + mgt_fees[t] 
                     + surrender_penalty[t] - extra_maturity_cost[t])
    
    npv_profit = 0.0
    npv_premium = 0.0
    for t in range(term):
        year = t + 1
        profit_discount = z ** year
        premium_discount = z ** (year - 1)
        npv_profit += profit[t] * inforce[t] * profit_discount
        npv_premium += premium * inforce[t] * premium_discount
    
    return {
        'profit_margin': npv_profit / npv_premium,
        'npv_profit': npv_profit,
        'npv_premium': npv_premium,
        'profit': profit,
        'fund_end': fund_end,
        'alloc': alloc,
        'spread': spread,
        'mgt_fees': mgt_fees,
        'unalloc': unalloc,
        'expenses': expenses,
        'commissions': commissions,
        'interest': interest,
        'extra_death': extra_death,
        'extra_disab': extra_disab,
        'surrender_penalty': surrender_penalty,
        'extra_maturity_cost': extra_maturity_cost
    }

def compute_term_results(age, gender_lower, term, sa, init_exp, init_comm,
                          inflation, ren_exp, ren_comm, mgt_charge, rdr, unit_int):
    if age + term - 1 > 70:
        return None
    pricing = price_policy(age=age, gender=gender_lower, term=term, sa=sa,
                            init_exp=init_exp, init_comm=init_comm,
                            inflation=inflation, ren_exp=ren_exp, ren_comm=ren_comm)
    profit = profit_test(pricing, mgt_charge=mgt_charge, rdr=rdr, unit_int=unit_int)
    return {'pricing': pricing, 'profit': profit}


def create_stat_card(label, value, sub_text="", color="#2563eb"):
    return f"""
    <div style="background: rgba(255,255,255,0.92); border-radius: 16px; padding: 1.1rem 1rem;
                border: 1px solid rgba(0,0,0,0.06); border-left: 4px solid {color};
                box-shadow: 0 4px 16px rgba(0,0,0,0.05); height: 100%;">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.3rem;">
            <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.5px; text-transform:uppercase; color:#64748b;">{label}</span>
        </div>
        <div style="font-size:1.6rem; font-weight:700; color:#1e293b; line-height:1.2;">{value}</div>
        <div style="font-size:0.72rem; color:#94a3b8; margin-top:0.15rem;">{sub_text}</div>
    </div>
    """


def create_circular_progress(value, max_val, label, color, sub_text=""):
    percentage = min(value / max_val * 100, 100)
    circumference = 2 * 3.14159 * 50
    offset = circumference - (percentage / 100) * circumference
    
    if isinstance(value, float):
        if abs(value) >= 1000:
            formatted_value = f"{value:,.2f}"
        else:
            formatted_value = f"{value:.2f}"
    else:
        formatted_value = f"{value:.2f}"
    
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:0.5rem;">
        <div style="position:relative; width:150px; height:150px;">
            <svg class="progress-ring" viewBox="0 0 120 120" style="width:150px; height:150px; transform:rotate(-90deg);">
                <circle class="bg" cx="60" cy="60" r="50" stroke="rgba(0,0,0,0.06)" stroke-width="10" fill="none"/>
                <circle class="progress" cx="60" cy="60" r="50" 
                        stroke="{color}" stroke-width="10" fill="none"
                        stroke-dasharray="{circumference}" 
                        stroke-dashoffset="{offset}"/>
            </svg>
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); text-align:center;">
                <div style="font-size:1.2rem; font-weight:700; color:#1e293b;">{formatted_value}</div>
                <div style="font-size:0.6rem; color:#94a3b8;">{sub_text}</div>
            </div>
        </div>
        <div style="font-size:0.7rem; color:#64748b; font-weight:600; letter-spacing:0.5px; text-transform:uppercase; margin-top:0.5rem;">{label}</div>
    </div>
    """

# =============================================================================
# 4. ANALYSIS FUNCTION
# =============================================================================

def run_analysis(age_start=20, age_end=60, genders=['Female', 'Male']):
    """Run premium and profit margin analysis across ages for both genders"""
    results = []
    terms = [5, 10]
    
    for gender in genders:
        gender_lower = gender.lower()
        for term in terms:
            for age in range(age_start, age_end + 1):
                if age + term - 1 > 70:
                    continue
                try:
                    pricing = price_policy(age=age, gender=gender_lower, term=term)
                    profit = profit_test(pricing)
                    results.append({
                        'Gender': gender,
                        'Age': age,
                        'Term': f'{term}-Year',
                        'Premium': pricing['premium'],
                        'Profit_Margin': profit['profit_margin'] * 100
                    })
                except Exception:
                    continue
    
    return pd.DataFrame(results)

# =============================================================================
# 5. STREAMLIT APP
# =============================================================================

def main():
    st.markdown("""
    <div class="header-container">
        <span class="header-title">Unit-Linked Endowment Microinsurance</span>
    </div>
    <p class="sub-title">Pricing & Profit Testing Model for Food Market Vendors in Uganda</p>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Policyholder Information</div>', unsafe_allow_html=True)
        age = st.slider("Age (years)", min_value=20, max_value=60, value=30, step=1)
        gender = st.selectbox("Gender", ["Female", "Male"])
        term_options = [5, 10]
        term = st.selectbox("Policy Term (years)", term_options, index=0)
        st.markdown('<div class="sidebar-header" style="margin-top:1.5rem;">Policy Details</div>', unsafe_allow_html=True)
        sa = st.number_input("Sum Assured (UGX)", min_value=500000, max_value=5000000, value=1500000, step=100000, format="%d")
        st.markdown('<div class="sidebar-header" style="margin-top:1.5rem;">Assumptions</div>', unsafe_allow_html=True)
        with st.expander("Expenses & Commissions", expanded=False):
            init_exp = st.slider("Initial Expenses (% of premium)", min_value=5.0, max_value=30.0, value=15.0, step=0.5) / 100
            init_comm = st.slider("Initial Commission (% of premium)", min_value=5.0, max_value=30.0, value=10.0, step=0.5) / 100
            ren_exp = st.slider("Renewal Expenses (% of premium)", min_value=2.0, max_value=15.0, value=5.0, step=0.5) / 100
            ren_comm = st.slider("Renewal Commission (% of premium)", min_value=2.0, max_value=15.0, value=7.5, step=0.5) / 100
        with st.expander("Financial Assumptions", expanded=False):
            mgt_charge = st.slider("Management Charge (% p.a.)", min_value=0.5, max_value=3.0, value=2.5, step=0.1) / 100
            rdr = st.slider("Risk Discount Rate (% p.a.)", min_value=10.0, max_value=25.0, value=18.5, step=0.5) / 100
            unit_int = st.slider("Unit Fund Interest Rate (% p.a.)", min_value=10.0, max_value=20.0, value=15.5, step=0.5) / 100
            inflation = st.slider("Inflation Rate (% p.a.)", min_value=0.0, max_value=10.0, value=3.2, step=0.1) / 100
        calculate = st.button("Calculate Premium", use_container_width=True)
    
    if calculate:
        with st.spinner("Calculating..."):
            gender_lower = gender.lower()
            result = compute_term_results(age, gender_lower, term, sa, init_exp, init_comm,
                                          inflation, ren_exp, ren_comm, mgt_charge, rdr, unit_int)
            if result is None:
                st.error(f"Age {age} + {term}-year term exceeds the mortality table's upper bound (age 70). Please lower the age or choose the 5-year term.")
                st.stop()
            pricing = result['pricing']
            profit = result['profit']
            
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align:center; margin-bottom:1.5rem;">
                <span class="term-badge">{term}-Year Term Results</span>
            </div>
            """, unsafe_allow_html=True)
            
            margin_color = "#22c55e" if profit['profit_margin'] > 0 else "#ef4444"
            row1 = st.columns(2)
            with row1[0]:
                st.markdown(create_stat_card("Annual Premium (UGX)", f"{pricing['premium']:,.0f}", "Payable yearly", "#2563eb"), unsafe_allow_html=True)
            with row1[1]:
                st.markdown(create_circular_progress(profit['profit_margin'] * 100, max(abs(profit['profit_margin']) * 100 * 1.3, 10), "Profit Margin (%)", margin_color, "Profitable" if profit['profit_margin'] > 0 else "Not Profitable"), unsafe_allow_html=True)
            
            row2 = st.columns(2)
            with row2[0]:
                st.markdown(create_stat_card("NPV of Profit (UGX)", f"{profit['npv_profit']:,.0f}", f"@ {rdr*100:.1f}% RDR", "#7c3aed"), unsafe_allow_html=True)
            with row2[1]:
                st.markdown(create_stat_card("NPV of Premium (UGX)", f"{profit['npv_premium']:,.0f}", f"@ {rdr*100:.1f}% RDR", "#eab308"), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # =============================================================
            # COMPARISON SECTION
            # =============================================================
            with st.expander("Compare 5-Year vs 10-Year Term", expanded=False):
                other_term = 10 if term == 5 else 5
                other_result = compute_term_results(age, gender_lower, other_term, sa, init_exp, init_comm,
                                                    inflation, ren_exp, ren_comm, mgt_charge, rdr, unit_int)
                
                if other_result is None:
                    st.warning(f"The {other_term}-year term isn't available at age {age} (would run past age 70 on the mortality table).")
                else:
                    term_a, term_b = (term, other_term) if term == 5 else (other_term, term)
                    res_a = result if term_a == term else other_result
                    res_b = result if term_b == term else other_result
                    
                    comp_data = {
                        "Metric": ["Annual Premium (UGX)", "Profit Margin (%)", "NPV of Profit (UGX)", "NPV of Premium (UGX)"],
                        f"{term_a}-Year Term": [f"{res_a['pricing']['premium']:,.2f}", f"{res_a['profit']['profit_margin']*100:.2f}", f"{res_a['profit']['npv_profit']:,.2f}", f"{res_a['profit']['npv_premium']:,.2f}"],
                        f"{term_b}-Year Term": [f"{res_b['pricing']['premium']:,.2f}", f"{res_b['profit']['profit_margin']*100:.2f}", f"{res_b['profit']['npv_profit']:,.2f}", f"{res_b['profit']['npv_premium']:,.2f}"]
                    }
                    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)
                    
                    fig_cmp = go.Figure()
                    fig_cmp.add_trace(go.Bar(x=["Premium (UGX)", "Profit Margin (%, x10,000)"], y=[res_a['pricing']['premium'], res_a['profit']['profit_margin']*100*10000], name=f"{term_a}-Year", marker_color="#2563eb"))
                    fig_cmp.add_trace(go.Bar(x=["Premium (UGX)", "Profit Margin (%, x10,000)"], y=[res_b['pricing']['premium'], res_b['profit']['profit_margin']*100*10000], name=f"{term_b}-Year", marker_color="#7c3aed"))
                    st.caption("Profit margin is scaled ×10,000 on this chart purely so both bars share one axis — read exact values from the table above.")
                    fig_cmp.update_layout(
                        barmode='group', template='plotly_white',
                        plot_bgcolor='rgba(255,255,255,0.8)', paper_bgcolor='rgba(255,255,255,0)',
                        font=dict(color='#1e293b'), height=380,
                        title="Comparison of Premium and Profit Margin by Term"
                    )
                    st.plotly_chart(fig_cmp, use_container_width=True)
                
                # =============================================================
                # PREMIUM AND PROFIT MARGIN COMPARISON ACROSS AGES - 4 GRAPHS
                # =============================================================
                st.markdown("---")
                st.markdown('<h3 style="color: #000000;">Premium and Profit Margin Comparison Across Ages</h3>', unsafe_allow_html=True)
                st.markdown('<p style="color: #475569;">The charts below show how premiums and profit margins vary by age for both genders and policy terms.</p>', unsafe_allow_html=True)
                
                with st.spinner("Running analysis..."):
                    df_analysis = run_analysis(20, 60, ['Female', 'Male'])
                    
                    if not df_analysis.empty:
                        # GRAPH 1: Female Premiums by Term
                        st.markdown("#### Female Premiums by Term")
                        df_female = df_analysis[df_analysis['Gender'] == 'Female']
                        if not df_female.empty:
                            fig_female_prem = go.Figure()
                            for term_label in ['5-Year', '10-Year']:
                                df_term = df_female[df_female['Term'] == term_label]
                                if not df_term.empty:
                                    fig_female_prem.add_trace(go.Scatter(
                                        x=df_term['Age'], y=df_term['Premium'],
                                        mode='lines+markers', name=term_label,
                                        line=dict(width=2), marker=dict(size=8)
                                    ))
                            fig_female_prem.update_layout(
                                title="Female Premiums by Age and Term",
                                xaxis_title="Age (years)",
                                yaxis_title="Annual Premium (UGX)",
                                hovermode='x unified',
                                template='plotly_white',
                                plot_bgcolor='rgba(255,255,255,0.8)',
                                paper_bgcolor='rgba(255,255,255,0)',
                                font=dict(color='#1e293b'),
                                title_font=dict(color='#1e293b', size=16),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                            )
                            st.plotly_chart(fig_female_prem, use_container_width=True)
                        else:
                            st.info("No female data available.")
                        
                        # GRAPH 2: Male Premiums by Term
                        st.markdown("#### Male Premiums by Term")
                        df_male = df_analysis[df_analysis['Gender'] == 'Male']
                        if not df_male.empty:
                            fig_male_prem = go.Figure()
                            for term_label in ['5-Year', '10-Year']:
                                df_term = df_male[df_male['Term'] == term_label]
                                if not df_term.empty:
                                    fig_male_prem.add_trace(go.Scatter(
                                        x=df_term['Age'], y=df_term['Premium'],
                                        mode='lines+markers', name=term_label,
                                        line=dict(width=2), marker=dict(size=8)
                                    ))
                            fig_male_prem.update_layout(
                                title="Male Premiums by Age and Term",
                                xaxis_title="Age (years)",
                                yaxis_title="Annual Premium (UGX)",
                                hovermode='x unified',
                                template='plotly_white',
                                plot_bgcolor='rgba(255,255,255,0.8)',
                                paper_bgcolor='rgba(255,255,255,0)',
                                font=dict(color='#1e293b'),
                                title_font=dict(color='#1e293b', size=16),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                            )
                            st.plotly_chart(fig_male_prem, use_container_width=True)
                        else:
                            st.info("No male data available.")
                        
                        # GRAPH 3: Female Profit Margins by Term
                        st.markdown("#### Female Profit Margins by Term")
                        df_female = df_analysis[df_analysis['Gender'] == 'Female']
                        if not df_female.empty:
                            fig_female_margin = go.Figure()
                            for term_label in ['5-Year', '10-Year']:
                                df_term = df_female[df_female['Term'] == term_label]
                                if not df_term.empty:
                                    fig_female_margin.add_trace(go.Scatter(
                                        x=df_term['Age'], y=df_term['Profit_Margin'],
                                        mode='lines+markers', name=term_label,
                                        line=dict(width=2), marker=dict(size=8)
                                    ))
                            fig_female_margin.update_layout(
                                title="Female Profit Margins by Age and Term",
                                xaxis_title="Age (years)",
                                yaxis_title="Profit Margin (%)",
                                hovermode='x unified',
                                template='plotly_white',
                                plot_bgcolor='rgba(255,255,255,0.8)',
                                paper_bgcolor='rgba(255,255,255,0)',
                                font=dict(color='#1e293b'),
                                title_font=dict(color='#1e293b', size=16),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                            )
                            fig_female_margin.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
                            st.plotly_chart(fig_female_margin, use_container_width=True)
                        else:
                            st.info("No female data available.")
                        
                        # GRAPH 4: Male Profit Margins by Term
                        st.markdown("#### Male Profit Margins by Term")
                        df_male = df_analysis[df_analysis['Gender'] == 'Male']
                        if not df_male.empty:
                            fig_male_margin = go.Figure()
                            for term_label in ['5-Year', '10-Year']:
                                df_term = df_male[df_male['Term'] == term_label]
                                if not df_term.empty:
                                    fig_male_margin.add_trace(go.Scatter(
                                        x=df_term['Age'], y=df_term['Profit_Margin'],
                                        mode='lines+markers', name=term_label,
                                        line=dict(width=2), marker=dict(size=8)
                                    ))
                            fig_male_margin.update_layout(
                                title="Male Profit Margins by Age and Term",
                                xaxis_title="Age (years)",
                                yaxis_title="Profit Margin (%)",
                                hovermode='x unified',
                                template='plotly_white',
                                plot_bgcolor='rgba(255,255,255,0.8)',
                                paper_bgcolor='rgba(255,255,255,0)',
                                font=dict(color='#1e293b'),
                                title_font=dict(color='#1e293b', size=16),
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                            )
                            fig_male_margin.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
                            st.plotly_chart(fig_male_margin, use_container_width=True)
                        else:
                            st.info("No male data available.")
                    else:
                        st.warning("No data available for the analysis. Please try adjusting the age range.")
            
            # =============================================================
            # DETAILED RESULTS EXPANDER
            # =============================================================
            with st.expander(f"Detailed Results - {term}-Year Term", expanded=False):
                # Benefit Structure
                st.markdown("#### Benefit Structure")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div style="background: rgba(37, 99, 235, 0.04); border-radius: 12px; padding: 1rem; border: 1px solid rgba(37, 99, 235, 0.08);">
                        <p style="color: #475569; margin: 0.3rem 0;"> Death Benefit: Sum Assured</p>
                        <p style="color: #475569; margin: 0.3rem 0;"> Disability Benefit: 110% of Fund Value</p>
                        <p style="color: #475569; margin: 0.3rem 0;"> Surrender Benefit: 70% of Fund Value (Year 4+)</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("""
                    <div style="background: rgba(37, 99, 235, 0.04); border-radius: 12px; padding: 1rem; border: 1px solid rgba(37, 99, 235, 0.08);">
                        <p style="color: #475569; margin: 0.3rem 0;"> Surrender Penalty: 30% of Fund Value</p>
                        <p style="color: #475569; margin: 0.3rem 0;"> Maturity Benefit: Sum Assured</p>
                        <p style="color: #475569; margin: 0.3rem 0;"> Management Charge: 2.5% p.a.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Full EPV Tables
                st.markdown('<div class="section-header">EPV Calculations - Detailed Breakdown</div>', unsafe_allow_html=True)
                
                # Death Benefits EPV Table
                st.markdown("#### Death Benefits")
                death_df = pd.DataFrame({
                    'Year': list(range(1, term+1)),
                    'Sum Assured': [sa] * term,
                    'aqd (Death Prob)': list(pricing['aqd']),
                    'Discount Factor': [ (1/(1+0.155)) ** (t+1) for t in range(term) ],
                    'EPV Contribution': list(pricing['epv_death_details'])
                })
                st.dataframe(death_df.style.format({
                    'Sum Assured': '{:,.0f}',
                    'aqd (Death Prob)': '{:.6f}',
                    'Discount Factor': '{:.6f}',
                    'EPV Contribution': '{:,.2f}'
                }), use_container_width=True)
                st.caption(f"Total EPV Death Benefits: UGX {pricing['epv_death']:,.2f}")
                
                # Disability Benefits EPV Table
                st.markdown("#### Disability Benefits (110% of Fund Value)")
                dis_df = pd.DataFrame({
                    'Year': list(range(1, term+1)),
                    'Fund Value': list(pricing['fund_end']),
                    'Disability Amount (110%)': list(1.10 * pricing['fund_end']),
                    'aqdi (Disability Prob)': list(pricing['aqdi']),
                    'Discount Factor': [ (1/(1+0.155)) ** (t+1) for t in range(term) ],
                    'EPV Contribution': list(pricing['epv_dis_details'])
                })
                st.dataframe(dis_df.style.format({
                    'Fund Value': '{:,.2f}',
                    'Disability Amount (110%)': '{:,.2f}',
                    'aqdi (Disability Prob)': '{:.6f}',
                    'Discount Factor': '{:.6f}',
                    'EPV Contribution': '{:,.2f}'
                }), use_container_width=True)
                st.caption(f"Total EPV Disability Benefits: UGX {pricing['epv_dis']:,.2f}")
                
                # Surrender Benefits EPV Table
                st.markdown("#### Surrender Benefits (70% of Fund Value, Year 4+)")
                surr_amounts = [0.70 * pricing['fund_end'][t] if t >= 3 else 0 for t in range(term)]
                surr_df = pd.DataFrame({
                    'Year': list(range(1, term+1)),
                    'Fund Value': list(pricing['fund_end']),
                    'Surrender Amount (70%)': surr_amounts,
                    'aqw (Surrender Prob)': list(pricing['aqw']),
                    'Discount Factor': [ (1/(1+0.155)) ** (t+1) for t in range(term) ],
                    'EPV Contribution': list(pricing['epv_surr_details'])
                })
                st.dataframe(surr_df.style.format({
                    'Fund Value': '{:,.2f}',
                    'Surrender Amount (70%)': '{:,.2f}',
                    'aqw (Surrender Prob)': '{:.6f}',
                    'Discount Factor': '{:.6f}',
                    'EPV Contribution': '{:,.2f}'
                }), use_container_width=True)
                st.caption(f"Total EPV Surrender Benefits: UGX {pricing['epv_surr']:,.2f}")
                
                # Survival Benefit
                st.markdown("#### Survival Benefit (Maturity)")
                st.markdown(f"""
                <div style="background: #f9f9f9; border-radius: 12px; padding: 1rem; border: 1px solid #dddddd;">
                    <p><strong>Sum Assured:</strong> UGX {sa:,.0f}</p>
                    <p><strong>Survival Probability (inforce):</strong> {pricing['inforce'][term-1]:.6f}</p>
                    <p><strong>Discount Factor (v^{term}):</strong> {(1/(1+0.155)) ** term:.6f}</p>
                    <p><strong>EPV Survival Benefit:</strong> UGX {pricing['epv_surv_value']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Expenses EPV Table
                st.markdown("#### Expenses")
                exp_amounts = [init_exp * pricing['premium'] if t == 0 else ren_exp * pricing['premium'] * ((1 + inflation) ** t) for t in range(term)]
                exp_df = pd.DataFrame({
                    'Year': list(range(1, term+1)),
                    'Expense Amount': exp_amounts,
                    'In-force Prob': list(pricing['inforce']),
                    'Discount Factor': [ (1/(1+0.155)) ** t for t in range(term) ],
                    'EPV Contribution': [exp_amounts[t] * pricing['inforce'][t] * ((1/(1+0.155)) ** t) for t in range(term)]
                })
                st.dataframe(exp_df.style.format({
                    'Expense Amount': '{:,.2f}',
                    'In-force Prob': '{:.6f}',
                    'Discount Factor': '{:.6f}',
                    'EPV Contribution': '{:,.2f}'
                }), use_container_width=True)
                st.caption(f"Total EPV Expenses: UGX {pricing['epv_expenses']:,.2f}")
                
                # Commissions EPV Table
                st.markdown("#### Commissions")
                comm_amounts = [init_comm * pricing['premium'] if t == 0 else ren_comm * pricing['premium'] for t in range(term)]
                comm_df = pd.DataFrame({
                    'Year': list(range(1, term+1)),
                    'Commission Amount': comm_amounts,
                    'In-force Prob': list(pricing['inforce']),
                    'Discount Factor': [ (1/(1+0.155)) ** t for t in range(term) ],
                    'EPV Contribution': [comm_amounts[t] * pricing['inforce'][t] * ((1/(1+0.155)) ** t) for t in range(term)]
                })
                st.dataframe(comm_df.style.format({
                    'Commission Amount': '{:,.2f}',
                    'In-force Prob': '{:.6f}',
                    'Discount Factor': '{:.6f}',
                    'EPV Contribution': '{:,.2f}'
                }), use_container_width=True)
                st.caption(f"Total EPV Commissions: UGX {pricing['epv_commissions']:,.2f}")
                
                # Premiums EPV Table
                st.markdown("#### Premiums")
                prem_df = pd.DataFrame({
                    'Year': list(range(1, term+1)),
                    'Premium Amount': [pricing['premium']] * term,
                    'In-force Prob': list(pricing['inforce']),
                    'Discount Factor': [ (1/(1+0.155)) ** t for t in range(term) ],
                    'EPV Contribution': [pricing['premium'] * pricing['inforce'][t] * ((1/(1+0.155)) ** t) for t in range(term)]
                })
                st.dataframe(prem_df.style.format({
                    'Premium Amount': '{:,.2f}',
                    'In-force Prob': '{:.6f}',
                    'Discount Factor': '{:.6f}',
                    'EPV Contribution': '{:,.2f}'
                }), use_container_width=True)
                st.caption(f"Total EPV Premiums: UGX {pricing['epv_premium']:,.2f}")
                
                # EPV Summary
                st.markdown('<div class="section-header">EPV Summary</div>', unsafe_allow_html=True)
                summary_data = {
                    'Component': ['Death Benefits', 'Disability Benefits', 'Surrender Benefits', 'Survival Benefit', 
                                 'Total Benefits', 'Expenses', 'Commissions', 'Premiums'],
                    'EPV (UGX)': [
                        pricing['epv_death'], pricing['epv_dis'], pricing['epv_surr'], 
                        pricing['epv_surv_value'], pricing['epv_benefits'],
                        pricing['epv_expenses'], pricing['epv_commissions'], pricing['epv_premium']
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                st.dataframe(df_summary.style.format({"EPV (UGX)": "{:,.2f}"}).background_gradient(cmap='Blues', subset=['EPV (UGX)']), use_container_width=True)
                
                # Unit Fund Projection
                st.markdown('<div class="section-header">Unit Fund Projection</div>', unsafe_allow_html=True)
                fund_data = {
                    "Year": list(range(1, term+1)),
                    "Allocated Premium": list(profit['alloc']),
                    "B/O Spread": list(profit['spread']),
                    "Mgt Fees": list(profit['mgt_fees']),
                    "Fund at Year End": list(profit['fund_end'])
                }
                df_fund = pd.DataFrame(fund_data)
                st.dataframe(df_fund.style.format({c: "{:,.2f}" for c in df_fund.columns if c != "Year"}), use_container_width=True)
                
                # Fund Growth Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=list(range(1, term+1)), y=profit['fund_end'], mode='lines+markers', 
                                         name='Fund Value', line=dict(color='#2563eb', width=3), 
                                         marker=dict(size=10, color='#2563eb'), fill='tozeroy', 
                                         fillcolor='rgba(37,99,235,0.15)'))
                fig.update_layout(title=f"Unit Fund Growth - {term}-Year Term", xaxis_title="Policy Year", 
                                 yaxis_title="Fund Value (UGX)", hovermode='x unified', template='plotly_white',
                                 plot_bgcolor='rgba(255,255,255,0.8)', paper_bgcolor='rgba(255,255,255,0)',
                                 font=dict(color='#1e293b'), title_font=dict(color='#1e293b', size=16))
                st.plotly_chart(fig, use_container_width=True)
                
                # Profit Vector
                st.markdown('<div class="section-header">Profit Vector</div>', unsafe_allow_html=True)
                profit_data = {
                    "Year": list(range(1, term+1)),
                    "Profit": list(profit['profit'])
                }
                df_profit = pd.DataFrame(profit_data)
                st.dataframe(df_profit.style.format({"Profit": "{:,.2f}"}), use_container_width=True)
                
                colors = ['#22c55e' if p >= 0 else '#ef4444' for p in profit['profit']]
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=list(range(1, term+1)), y=profit['profit'], marker_color=colors, 
                                     text=[f'UGX {p:,.2f}' for p in profit['profit']], textposition='outside'))
                fig2.update_layout(title=f"Annual Profit Vector - {term}-Year Term", xaxis_title="Policy Year",
                                  yaxis_title="Profit (UGX)", hovermode='x unified', template='plotly_white',
                                  plot_bgcolor='rgba(255,255,255,0.8)', paper_bgcolor='rgba(255,255,255,0)',
                                  font=dict(color='#1e293b'), title_font=dict(color='#1e293b', size=16))
                st.plotly_chart(fig2, use_container_width=True)
                
                # Multiple Decrement Table
                st.markdown('<div class="section-header">Multiple Decrement Table</div>', unsafe_allow_html=True)
                decrement_data = {
                    "Age": [age + t for t in range(term)],
                    "qd (Death)": list(pricing['aqd']),
                    "qdi (Disability)": list(pricing['aqdi']),
                    "qw (Surrender)": list(pricing['aqw']),
                    "ap (Survival)": list(pricing['ap']),
                    "In-force": list(pricing['inforce'])
                }
                df_dec = pd.DataFrame(decrement_data)
                st.dataframe(df_dec.style.format({c: "{:.6f}" for c in df_dec.columns if c != "Age"}), use_container_width=True)
            
            # Download
            st.markdown("---")
            st.subheader("Export Results")
            
            results_data = {
                "Metric": ["Premium", "Profit Margin", "NPV of Profit", "NPV of Premium", 
                           "EPV Benefits", "EPV Expenses", "EPV Commissions", "EPV Premium"],
                "Value": [
                    pricing['premium'], 
                    profit['profit_margin'] * 100, 
                    profit['npv_profit'],
                    profit['npv_premium'], 
                    pricing['epv_benefits'], 
                    pricing['epv_expenses'],
                    pricing['epv_commissions'], 
                    pricing['epv_premium']
                ]
            }
            df_results = pd.DataFrame(results_data)
            csv_data = df_results.to_csv(index=False)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="Download Results (CSV)",
                    data=csv_data,
                    file_name=f"policy_quote_age_{age}_{gender}_term_{term}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h2 style="color: #1e293b; font-weight: 300;">Welcome to the Pricing Tool</h2>
            <p style="color: #475569; max-width: 500px; margin: 1rem auto;">
                Enter policyholder details in the sidebar and click 
                <strong style="color: #2563eb;">Calculate Premium</strong> to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">1</div>
                <h4 style="color: #1e293b;">Input Details</h4>
                <p style="color: #475569; font-size: 0.9rem;">Age, Gender, Sum Assured</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">2</div>
                <h4 style="color: #1e293b;">Pricing Engine</h4>
                <p style="color: #475569; font-size: 0.9rem;">Multiple decrement model, EPV calculations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">3</div>
                <h4 style="color: #1e293b;">Results</h4>
                <p style="color: #475569; font-size: 0.9rem;">5-year or 10-year term results</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("Based on the pricing and profit testing model for unit-linked endowment microinsurance products for food market vendors in Uganda.")

if __name__ == "__main__":
    main()
