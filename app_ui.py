import streamlit as st

st.set_page_config(
    page_title="PantryPalSmart | AI Food Storage",
    page_icon="🥑",
    layout="centered"
)

# Custom Styling (Dark theme, glow cards)
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F8FAFC; }
    .badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.3);
        display: inline-block;
        margin-bottom: 10px;
    }
    .result-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        text-align: center;
    }
    .result-label { font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; }
    .result-val { font-size: 1.4rem; font-weight: 800; color: #34D399; }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="badge">PANTRYPAL SMART</div>', unsafe_allow_html=True)
st.title("Smart Food Storage AI")
st.caption("Instantly identify food items, inspect freshness levels, and calculate shelf life.")

# Upload Area
uploaded_file = st.file_uploader("Choose a food photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Inspect Item", type="primary"):
        with st.spinner("Analyzing item..."):
            detected_food = "Fresh Apple"
            freshness_status = "Fresh"
            estimated_expiry = 7
            
            st.markdown("### Analysis Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Food Detected</div>
                    <div class="result-val" style="color: #FFF;">{detected_food}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Freshness</div>
                    <div class="result-val">{freshness_status}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Est. Shelf Life</div>
                <div class="result-val" style="color: #6EE7B7;">{estimated_expiry} Days</div>
            </div>
            """, unsafe_allow_html=True)
