
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="تحليل المستوى التعليمي", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        background-color: #f5f8fc;
    }
    .metric-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
    }
    .section-header {
        font-size: 20px;
        color: #1e3d59;
        margin-top: 20px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 تحليل الموظفين حسب المستوى التعليمي")

uploaded_file = st.file_uploader("ارفع ملف بيانات الموظفين", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_sheet = st.selectbox("اختر الجهة (Sheet):", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()

    if 'الدائرة' in df.columns and 'المستوى التعليمي' in df.columns:
        st.subheader("📊 التوزيع الإجمالي للمستوى التعليمي")

        edu_total = df['المستوى التعليمي'].value_counts().reset_index()
        edu_total.columns = ['المستوى التعليمي', 'عدد']
        edu_total['النسبة'] = round((edu_total['عدد'] / edu_total['عدد'].sum()) * 100, 1)
        edu_total['label'] = edu_total.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

        fig_total = px.bar(
            edu_total,
            x='المستوى التعليمي',
            y='عدد',
            text='label',
            color='المستوى التعليمي',
            color_discrete_sequence=px.colors.sequential.Blues[::-1]
        )
        fig_total.update_traces(textposition='inside', insidetextanchor='middle')
        fig_total.update_layout(title='إجمالي توزيع المستوى التعليمي', title_x=0.5, showlegend=False)
        st.plotly_chart(fig_total, use_container_width=True)

        st.subheader("🏢 التوزيع حسب كل جهة (Stacked)")

        grouped = df.groupby(['الدائرة', 'المستوى التعليمي']).size().reset_index(name='عدد')
        total_per_dept = grouped.groupby('الدائرة')['عدد'].transform('sum')
        grouped['النسبة'] = round((grouped['عدد'] / total_per_dept) * 100, 1)
        grouped['label'] = grouped.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

        fig_stacked = px.bar(
            grouped,
            x='الدائرة',
            y='عدد',
            color='المستوى التعليمي',
            text='label',
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Blues[::-1]
        )
        fig_stacked.update_traces(textposition='inside', insidetextanchor='middle')
        fig_stacked.update_layout(title='توزيع المستوى التعليمي حسب كل دائرة', title_x=0.5, xaxis_tickangle=-45)
        st.plotly_chart(fig_stacked, use_container_width=True)
