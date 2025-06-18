
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="مخطط تعليمي لكل دائرة منفصلة", layout="wide")
st.title("🏢 تحليل المستوى التعليمي - كل دائرة في رسم مكدّس منفصل")

uploaded_file = st.file_uploader("ارفع ملف بيانات الموظفين", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_sheet = st.selectbox("اختر الجهة (Sheet):", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()

    if 'الدائرة' in df.columns and 'المستوى التعليمي' in df.columns:
        unique_depts = df['الدائرة'].dropna().unique()

        for dept in sorted(unique_depts):
            st.subheader(f"📌 {dept}")
            dept_df = df[df['الدائرة'] == dept]

            edu_counts = dept_df['المستوى التعليمي'].value_counts().reset_index()
            edu_counts.columns = ['المستوى التعليمي', 'عدد']
            edu_counts['النسبة'] = round((edu_counts['عدد'] / edu_counts['عدد'].sum()) * 100, 1)
            edu_counts['label'] = edu_counts.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

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
