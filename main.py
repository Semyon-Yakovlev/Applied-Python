import streamlit as st
import pandas as pd
import plotly.express as px


data = pd.read_csv('prepared_data.csv', index_col = [0])
GENDER = st.sidebar.multiselect('Выберите пол', data['GENDER'].unique())
LOAN_NUM_TOTAL = st.sidebar.multiselect('Выберите количество взятых кредитов', data['LOAN_NUM_TOTAL'].unique())
PERSONAL_INCOME = st.sidebar.slider("Выберите доход", data.PERSONAL_INCOME.min(), data.PERSONAL_INCOME.max(), 
                        (data.PERSONAL_INCOME.min(), data.PERSONAL_INCOME.max()))
CHILD_TOTAL = st.sidebar.slider("Выберите количество детей", data.CHILD_TOTAL.min(), data.CHILD_TOTAL.max(), 
                        (data.CHILD_TOTAL.min(), data.CHILD_TOTAL.max()))
data = data[data['GENDER'].isin(GENDER)]
data = data[data['LOAN_NUM_TOTAL'].isin(LOAN_NUM_TOTAL)]
data = data[data["PERSONAL_INCOME"].between(PERSONAL_INCOME[0], PERSONAL_INCOME[1])]
data = data[data["CHILD_TOTAL"].between(CHILD_TOTAL[0], CHILD_TOTAL[1])]

st.title("Разведочный анализ данных")


st.subheader('Посмотрим на числовые характеристики столбцов')
st.write(data.describe())
st.write(f'После очистки данных в датасете осталось {data.shape[0]} строки')
st.write(f'Минимальный доход составил {data.PERSONAL_INCOME.min()}')
st.write(f'Максимальное доход составил {data.PERSONAL_INCOME.max()}')


st.subheader('Распределение дохода семьи на скрипичном графике')
fig = px.violin(data, x="FAMILY_INCOME", y="AGE")
st.plotly_chart(fig)
st.write(f"Средний возраст {round(data['AGE'].mean(),0)} со средним доходом {round(data['PERSONAL_INCOME'].mean(),0)}")


st.subheader('Распределение дохода по количеству детей')
fig = px.scatter(data, x='CHILD_TOTAL', y='PERSONAL_INCOME')
st.plotly_chart(fig)
st.write('Чем меньше детей, тем больше доход, но есть исключения')


st.subheader('Посмотрим на гистограмму пола и количества детей')
fig = px.histogram(data, x='GENDER', y='CHILD_TOTAL')
st.plotly_chart(fig)
st.write('У мужчин больше всего детей')



st.subheader('Посмотрим на количество закрытых кредитов и количество зависимых от человека людей')
fig = px.scatter(data, x='DEPENDANTS', y='LOAN_NUM_CLOSED')
st.plotly_chart(fig)
st.write('В целом понятно, если ты помогаешь большому количеству людей=> закрываешь меньше кредитов')


st.subheader('Корреляция')
corr = px.imshow(
  data.drop('FAMILY_INCOME', axis = 1).corr())
st.plotly_chart(corr)
st.write('Сильная корреляция между количеством количеством закрытых и взятых кредитов')
st.write('Корреляции между признаками AGREEMENT_RK и ID_CLIENT')