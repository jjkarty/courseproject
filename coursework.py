from google.colab import files
uploaded = files.upload()


import pandas as pd
df = pd.read_csv('oprosdata.csv')

df.head()

df.describe()

df.info()

df = df.drop(columns=['ID'])
df = df.reset_index(drop=True)
df.insert(0, 'ID', df.index)
df.head()

df['Город проживания:'].unique()


def classify_region(city):
    if 'Москва' in city or 'Московская область' in city:
        return 'Москва и Московская область'
    else:
        return 'Другие регионы'

df['Регион'] = df['Город проживания:'].apply(classify_region)
df.head()

# Redefine the function to classify sector
def classify_sector(it, fin):
    if it == 'Да' and fin == 'Да':
        return 'IT+Финансы'
    elif it == 'Да' or fin == 'Да':
        return 'Смешанная'
    else:
        return 'Другое'

# Apply the classification
df['Сфера'] = df.apply(
    lambda row: classify_sector(row['Информационные технологии:'], row['Финансы:']), axis=1
)

# Reinitialize the results dictionary
results = {}

# Show confirmation
df[['Информационные технологии:', 'Финансы:', 'Сфера']].head()

import pandas as pd

# 1. Доля из Москвы и МО

moscow_share = (df['Регион'] == 'Москва и Московская область').mean() * 100
results['Доля из Москвы и МО (%)'] = round(moscow_share, 2)


# 2. Распределение по возрастам (%)

age_dist = df['Ваш возраст:'].value_counts(normalize=True).mul(100).round(2)




# 3. Распределение по IT/Финансы (%)


sector_dist = df['Сфера'].value_counts(normalize=True).mul(100).round(2)

summary_df = pd.DataFrame({
    'Возраст (%)': age_dist,
    'Сфера (%)': sector_dist
}).fillna('')
summary_df.to_excel("сводка.xlsx")

# 4. Доля (%) респондентов в каждой возрастной категории, которые отметили: личное посещение офиса, общение в чате, звонки в колл-центр, мессенджеры, то же самое не для возраста, а для IT_финансы;

contact_columns = [
    'Какие каналы взаимодействия с финансовыми организациями Вы предпочитаете? / Личное посещение офиса',
    'Какие каналы взаимодействия с финансовыми организациями Вы предпочитаете? / Общение в чате мобильного приложения / на сайте',
    'Какие каналы взаимодействия с финансовыми организациями Вы предпочитаете? / Звонки в колл-центр',
    'Какие каналы взаимодействия с финансовыми организациями Вы предпочитаете? / Мессенджеры (WhatsApp, Telegram и т.д.)'
]

contact_by_age = df.groupby('Ваш возраст:')[contact_columns].apply(lambda x: x.notna().sum())
total_by_age = df['Ваш возраст:'].value_counts()
contact_by_age_percent = contact_by_age.div(total_by_age, axis=0).mul(100).round(2)

contact_by_sector = df.groupby('Сфера')[contact_columns].apply(lambda x: x.notna().sum())
total_by_sector = df['Сфера'].value_counts()
contact_by_sector_percent = contact_by_sector.div(total_by_sector, axis=0).mul(100).round(2)


# 5. Доля (%) респондентов, которые выбрали личное посещение и надежность одновременно;

strategy_columns = [col for col in df.columns if 'В случае проблем' in col or 'В случае вопросов' in col]
strategy_by_age = df.groupby('Ваш возраст:')[strategy_columns].apply(lambda x: x.notna().sum())
strategy_by_age_percent = strategy_by_age.div(total_by_age, axis=0).mul(100).round(2)

strategy_by_sector = df.groupby('Сфера')[strategy_columns].apply(lambda x: x.notna().sum())
strategy_by_sector_percent = strategy_by_sector.div(total_by_sector, axis=0).mul(100).round(2)



# 6. Доля (%) респондентов в каждой возрастной категории, которые отметили разные стратегии (сообщаю, пишу и т.д. при проблемах и вопросах); то же самое не для возраста, а для IT_финансы;

strategy_columns = [col for col in df.columns if 'стратегии' in col.lower()]
strategy_by_age = df.groupby('Ваш возраст:')[strategy_columns].apply(lambda x: x.notna().sum())
strategy_by_age_percent = strategy_by_age.div(total_by_age, axis=0).mul(100).round(2)

strategy_by_sector = df.groupby('Сфера')[strategy_columns].apply(lambda x: x.notna().sum())
strategy_by_sector_percent = strategy_by_sector.div(total_by_sector, axis=0).mul(100).round(2)


#7. Распределение возрастов и IT_финансов (от общего числа респондентов в этих категориях) по критериям (простота, оперативная обратная связь и т.д.)


criteria_columns = [col for col in df.columns if 'критерии' in col.lower()]
criteria_by_age = df.groupby('Ваш возраст:')[criteria_columns].apply(lambda x: x.notna().sum())
criteria_by_age_percent = criteria_by_age.div(total_by_age, axis=0).mul(100).round(2)

criteria_by_sector = df.groupby('Сфера')[criteria_columns].apply(lambda x: x.notna().sum())
criteria_by_sector_percent = criteria_by_sector.div(total_by_sector, axis=0).mul(100).round(2)

# Save everything into one Excel file


excel_path = "opros_full_results.xlsx"

with pd.ExcelWriter(excel_path) as writer:
    contact_by_age_percent.to_excel(writer, sheet_name='Каналы_по_возрасту')
    contact_by_sector_percent.to_excel(writer, sheet_name='Каналы_по_сфере')
    strategy_by_age_percent.to_excel(writer, sheet_name='Стратегии_по_возрасту')
    strategy_by_sector_percent.to_excel(writer, sheet_name='Стратегии_по_сфере')
    criteria_by_age_percent.to_excel(writer, sheet_name='Критерии_по_возрасту')
    criteria_by_sector_percent.to_excel(writer, sheet_name='Критерии_по_сфере')
from google.colab import files
files.download('opros_full_results.xlsx')


import matplotlib.pyplot as plt


# Classify into four categories
def classify_activity(it, fin):
    if it == 'Да' and fin == 'Да':
        return 'IT and Finance'
    elif it == 'Да' and fin != 'Да':
        return 'IT only'
    elif it != 'Да' and fin == 'Да':
        return 'Finance only'
    else:
        return 'Neither IT nor Finance'

df['Activity'] = df.apply(
    lambda row: classify_activity(row['Информационные технологии:'], row['Финансы:']), axis=1
)

# Pie chart for age distribution
age_counts = df['Ваш возраст:'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Age Distribution of Respondents')
plt.axis('equal')
plt.show()

# Pie chart for activity categories
activity_counts = df['Activity'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Current Activity of Respondents')
plt.axis('equal')
plt.show()