
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="تحليل التخصصات التعليمية", layout="wide")

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

st.title("🎓 تحليل التخصصات التعليمية حسب الجهات")

uploaded_file = st.file_uploader("ارفع ملف بيانات الموظفين", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_sheet = st.selectbox("اختر الجهة (Sheet):", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()

    if 'الدائرة' in df.columns and 'المستوى التعليمي' in df.columns:
        st.subheader("🔹 توزيع التخصصات التعليمية - لجميع الجهات")

        grouped = df.groupby(['الدائرة', 'المستوى التعليمي']).size().reset_index(name='عدد')
        total_per_dept = grouped.groupby('الدائرة')['عدد'].transform('sum')
        grouped['النسبة'] = round((grouped['عدد'] / total_per_dept) * 100, 1)
        grouped['label'] = grouped.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

        fig_all = px.bar(
            grouped,
            x='الدائرة',
            y='عدد',
            color='المستوى التعليمي',
            text='label',
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Blues[::-1]
        )
        fig_all.update_traces(textposition='inside', insidetextanchor='middle')
        fig_all.update_layout(title='توزيع التخصصات التعليمية لجميع الجهات', title_x=0.5, xaxis_tickangle=-45)
        st.plotly_chart(fig_all, use_container_width=True)

        st.subheader("🔹 توزيع التخصصات التعليمية لكل جهة على حدة")

        unique_depts = df['الدائرة'].dropna().unique()

        for dept in sorted(unique_depts):
            dept_df = df[df['الدائرة'] == dept]
            edu_counts = dept_df['المستوى التعليمي'].value_counts().reset_index()
            edu_counts.columns = ['المستوى التعليمي', 'عدد']
            edu_counts['النسبة'] = round((edu_counts['عدد'] / edu_counts['عدد'].sum()) * 100, 1)
            edu_counts['label'] = edu_counts.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

            st.markdown(f"#### {dept}")
            fig = px.bar(
                edu_counts,
                x='المستوى التعليمي',
                y='عدد',
                text='label',
                color='المستوى التعليمي',
                color_discrete_sequence=px.colors.sequential.Blues[::-1]
            )
            fig.update_traces(textposition='inside', insidetextanchor='middle')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
