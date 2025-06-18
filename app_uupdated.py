
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="تحليل تفصيلي للمستوى التعليمي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        background-color: #f5f8fc;
    }
    .section-header {
        font-size: 22px;
        color: #1e3d59;
        margin-top: 20px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 تحليل المستوى التعليمي لكل دائرة (مخططات منفصلة)")

uploaded_file = st.file_uploader("ارفع ملف بيانات الموظفين", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_sheet = st.selectbox("اختر الجهة (Sheet):", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()

    if 'الدائرة' in df.columns and 'المستوى التعليمي' in df.columns:
        edu_grouped = df.groupby(['الدائرة', 'المستوى التعليمي']).size().reset_index(name='عدد')
        total_per_dept = edu_grouped.groupby('الدائرة')['عدد'].transform('sum')
        edu_grouped['النسبة'] = round((edu_grouped['عدد'] / total_per_dept) * 100, 1)
        edu_grouped['label'] = edu_grouped.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

        fig_facets = px.bar(
            edu_grouped,
            x='المستوى التعليمي',
            y='عدد',
            text='label',
            color='المستوى التعليمي',
            color_discrete_sequence=px.colors.sequential.Blues[::-1],
            facet_col='الدائرة',
            facet_col_wrap=3,
            title="مخططات منفصلة لكل دائرة - توزيع المستوى التعليمي"
        )

        fig_facets.update_traces(textposition='inside', insidetextanchor='middle')
        fig_facets.update_layout(title_x=0.5)
        st.plotly_chart(fig_facets, use_container_width=True)
