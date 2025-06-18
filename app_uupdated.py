
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="المستوى التعليمي - كل جهة في عمود", layout="wide")
st.title("📊 توزيع المستوى التعليمي - كل جهة في عمود منفصل")

uploaded_file = st.file_uploader("ارفع ملف بيانات الموظفين", type=["xlsx"])

if uploaded_file:
    all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
    selected_sheet = st.selectbox("اختر الجهة (Sheet):", list(all_sheets.keys()))
    df = all_sheets[selected_sheet]
    df.columns = df.columns.str.strip()

    if 'الدائرة' in df.columns and 'المستوى التعليمي' in df.columns:
        grouped = df.groupby(['الدائرة', 'المستوى التعليمي']).size().reset_index(name='عدد')
        total_per_dept = grouped.groupby('الدائرة')['عدد'].transform('sum')
        grouped['النسبة'] = round((grouped['عدد'] / total_per_dept) * 100, 1)
        grouped['label'] = grouped.apply(lambda row: f"{row['عدد']} | {row['النسبة']}%", axis=1)

        fig = px.bar(
            grouped,
            x='الدائرة',
            y='عدد',
            color='المستوى التعليمي',
            text='label',
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Blues[::-1]
        )

        fig.update_traces(textposition='inside', insidetextanchor='middle')
        fig.update_layout(title='توزيع المستوى التعليمي داخل كل دائرة (Stacked Columns)', title_x=0.5, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
