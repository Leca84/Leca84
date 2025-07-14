import pandas as pd
import os
import re
import numpy as np
import datetime
from IPython.display import HTML

# Установка текущей даты
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Функции для стилизации
def style_negative_positive(val):
    if isinstance(val, (int, float)):
        color = 'red' if val < 0 else 'green' if val > 0 else 'black'
        weight = 'bold' if abs(val) > 10 else 'normal'
        return f'color: {color}; font-weight: {weight}'
    return ''

def highlight_attention(val):
    if val == 'Прирост более 20% между всеми периодами':
        return 'color: red; font-weight: bold'
    return ''

def highlight_consistent_growth(row):
    if len(dates) >= 2:
        for i in range(len(dates)-1):
            prev_date = dates[i]
            next_date = dates[i+1]
            growth_col = f"growth_{prev_date}_to_{next_date}"
            if growth_col in row and row[growth_col] <= 20:
                return [''] * len(row)
        return ['background-color: #ffcccc'] * len(row)
    return [''] * len(row)

# Поиск файлов с данными
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
pattern = re.compile(r'GP_MIS4_capacity_\d{4}-\d{2}-\d{2}.csv')
file_names = sorted([f for f in os.listdir(parent_directory) if pattern.match(f)])[-3:]

if len(file_names) < 2:
    print("Недостаточно файлов для сравнения (min = 2)")
    exit()

# Загрузка и подготовка данных
dfs = []
for file in file_names:
    try:
        date = re.search(r'\d{4}-\d{2}-\d{2}', file).group()
        df = pd.read_csv(os.path.join(parent_directory, file), sep=';', encoding='utf-8', header=0)
        
        # Стандартизация столбцов
        df.columns = df.columns.str.lower()
        df['file_date'] = date
        
        # Проверка и добавление обязательных столбцов
        required_cols = ['владелец', 'name_modul', 'schema_name', 'root_table', 
                        'impact_size_gb', 'table_size_gb']
        for col in required_cols:
            if col not in df.columns:
                df[col] = np.nan
                
        # Добавление obj_description, если отсутствует
        if 'obj_description' not in df.columns:
            df['obj_description'] = np.nan
            
        dfs.append(df)
    except Exception as e:
        print(f"Ошибка при загрузке файла {file}: {str(e)}")

if not dfs:
    print("Нет данных для анализа")
    exit()

# Объединение данных
combined_df = pd.concat(dfs, ignore_index=True)

# Получение уникальных дат
dates = sorted(list(set(combined_df['file_date'])), key=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))[-3:]

if len(dates) < 2:
    print("Недостаточно дат для сравнения (min = 2)")
    exit()

# Создание сводной таблицы
try:
    pivot_df = combined_df.pivot_table(
        index=['владелец', 'name_modul', 'schema_name', 'root_table'],
        columns='file_date',
        values=['impact_size_gb', 'table_size_gb'],
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Выравнивание мультииндекса столбцов
    pivot_df.columns = ['_'.join(col).strip('_') for col in pivot_df.columns.values]
    
    # Добавление obj_description из последнего файла
    if 'obj_description' in dfs[-1].columns:
        obj_descriptions = dfs[-1][['schema_name', 'root_table', 'obj_description']].drop_duplicates()
        pivot_df = pd.merge(pivot_df, obj_descriptions, on=['schema_name', 'root_table'], how='left')

except Exception as e:
    print(f"Ошибка при создании сводной таблицы: {str(e)}")
    pivot_df = pd.DataFrame()

# Расчет роста между датами
if len(dates) >= 2 and not pivot_df.empty:
    # Расчет промежуточных ростов
    for i in range(len(dates)-1):
        prev_date = dates[i]
        next_date = dates[i+1]
        prev_col = f"impact_size_gb_{prev_date}"
        next_col = f"impact_size_gb_{next_date}"
        
        if prev_col in pivot_df.columns and next_col in pivot_df.columns:
            valid_mask = (pivot_df[prev_col] > 0) & (pivot_df[next_col].notna())
            pivot_df[f"growth_{prev_date}_to_{next_date}"] = np.nan
            pivot_df.loc[valid_mask, f"growth_{prev_date}_to_{next_date}"] = (
                (pivot_df.loc[valid_mask, next_col] - pivot_df.loc[valid_mask, prev_col]) / 
                pivot_df.loc[valid_mask, prev_col]
            ) * 100

    # Расчет общего роста
    first_date = dates[0]
    last_date = dates[-1]
    first_col = f"impact_size_gb_{first_date}"
    last_col = f"impact_size_gb_{last_date}"
    
    if first_col in pivot_df.columns and last_col in pivot_df.columns:
        valid_mask = (pivot_df[first_col] > 0) & (pivot_df[last_col].notna())
        pivot_df['total_growth'] = np.nan
        pivot_df.loc[valid_mask, 'total_growth'] = (
            (pivot_df.loc[valid_mask, last_col] - pivot_df.loc[valid_mask, first_col]) / 
            pivot_df.loc[valid_mask, first_col]
        ) * 100
        
        # Абсолютное изменение в GB
        pivot_df['total_growth_gb'] = pivot_df[last_col] - pivot_df[first_col]

# Добавление столбца attention (рост >20% между всеми последовательными периодами)
if len(dates) >= 3 and not pivot_df.empty:
    growth_cols = [f"growth_{dates[i]}_to_{dates[i+1]}" for i in range(len(dates)-1)]
    if all(col in pivot_df.columns for col in growth_cols):
        pivot_df['attention'] = np.where(
            pivot_df[growth_cols].gt(20).all(axis=1),
            'Прирост более 20% между всеми периодами',
            ''
        )

# Фильтрация результатов
result_df = pd.DataFrame()
if len(dates) >= 2 and not pivot_df.empty and 'total_growth' in pivot_df.columns:
    last_col = f"impact_size_gb_{dates[-1]}"
    if last_col in pivot_df.columns:
        filter_conditions = [
            pivot_df['total_growth'] > 9,
            pivot_df[last_col] > 100
        ]
        result_df = pivot_df[np.logical_and.reduce(filter_conditions)].sort_values(
            'total_growth_gb' if 'total_growth_gb' in pivot_df.columns else last_col,
            ascending=False
        )

if result_df.empty:
    print("Нет таблиц, удовлетворяющих условиям (рост >9% и размер >100GB)")
    exit()

# Создаем две версии DataFrame: одну с числовыми данными для градиента, другую с форматированными строками для отображения
gradient_df = result_df.copy()
display_df = result_df.copy()

# Подготовка отображаемых данных (форматированные строки)
for i in range(len(dates)-1):
    prev_date = dates[i]
    next_date = dates[i+1]
    growth_col = f"growth_{prev_date}_to_{next_date}"
    size_col1 = f"impact_size_gb_{prev_date}"
    size_col2 = f"impact_size_gb_{next_date}"
    
    if all(col in display_df.columns for col in [growth_col, size_col1, size_col2]):
        display_df[growth_col] = display_df.apply(
            lambda x: f"{x[growth_col]:+.2f}% ({(x[size_col2] - x[size_col1]):+.2f} GB)" 
            if pd.notna(x[growth_col]) else "",
            axis=1
        )

if all(col in display_df.columns for col in ['total_growth', 'total_growth_gb']):
    display_df['total_growth_formatted'] = display_df.apply(
        lambda x: f"{x['total_growth_gb']:+.2f} GB ({x['total_growth']:+.2f}%)" 
        if pd.notna(x['total_growth']) else "",
        axis=1
    )

# Переименовываем столбцы в отображаемом DataFrame
display_column_rename = {
    **{f"impact_size_gb_{date}": f"Size ({date})" for date in dates 
      if f"impact_size_gb_{date}" in display_df.columns},
    **{f"growth_{dates[i]}_to_{dates[i+1]}": f"Growth {dates[i]}→{dates[i+1]}" 
       for i in range(len(dates)-1) 
       if f"growth_{dates[i]}_to_{dates[i+1]}" in display_df.columns},
    'total_growth_formatted': 'Total Growth (GB, %)',
    'attention': 'Attention'
}
display_df = display_df.rename(columns={k: v for k, v in display_column_rename.items() if k in display_df.columns})

# Переименовываем столбцы в градиентном DataFrame (только размеры, рост оставляем числовым)
gradient_column_rename = {
    **{f"impact_size_gb_{date}": f"Size ({date})" for date in dates 
      if f"impact_size_gb_{date}" in gradient_df.columns},
    'attention': 'Attention'
}
gradient_df = gradient_df.rename(columns={k: v for k, v in gradient_column_rename.items() if k in gradient_df.columns})

# Добавляем столбец Владелец в отображаемый DataFrame
if 'владелец' in display_df.columns:
    display_df['Владелец'] = display_df['владелец']
    gradient_df['Владелец'] = gradient_df['владелец']

# Создаем финальный DataFrame для отображения
final_columns = []
base_cols = ['Владелец', 'schema_name', 'root_table', 'obj_description', 
            'Total Growth (GB, %)', 'Attention']
final_columns.extend([col for col in base_cols if col in display_df.columns])

size_cols = [f"Size ({date})" for date in dates if f"Size ({date})" in display_df.columns]
final_columns.extend(size_cols)

growth_cols = [f"Growth {dates[i]}→{dates[i+1]}" for i in range(len(dates)-1) 
              if f"Growth {dates[i]}→{dates[i+1]}" in display_df.columns]
final_columns.extend(growth_cols)

final_columns = [col for col in final_columns if col in display_df.columns]

# Устраняем дублирование строк - группируем по schema_name и root_table, берем первую запись
display_df_dedup = display_df.drop_duplicates(subset=['schema_name', 'root_table'], keep='first')
gradient_df_dedup = gradient_df.drop_duplicates(subset=['schema_name', 'root_table'], keep='first')

final_display_df = display_df_dedup[final_columns].copy()

# Стилизация таблицы
try:
    styled_df = final_display_df.style
    
    # Применяем стили для столбца attention
    if 'Attention' in final_display_df.columns:
        try:
            styled_df = styled_df.applymap(highlight_attention, subset=['Attention'])
        except:
            pass
    
    # Форматирование столбцов размера
    format_rules = {}
    for col in final_display_df.columns:
        if col.startswith('Size ('):
            format_rules[col] = '{:.2f} GB'
    
    if format_rules:
        try:
            styled_df = styled_df.format(format_rules)
        except:
            pass
    
        # Применяем градиентную заливку к числовым данным
        try:
            # Градиент для Total Growth (используем числовое значение из gradient_df)
            if 'total_growth_gb' in gradient_df_dedup.columns and 'Total Growth (GB, %)' in final_display_df.columns:
                total_growth_values = gradient_df_dedup['total_growth_gb'].values
                if len(total_growth_values) > 0 and not np.isnan(total_growth_values).all():
                    min_val = np.nanmin(total_growth_values)
                    max_val = np.nanmax(total_growth_values)
                    
                    # Создаем функцию для применения градиента на основе числовых значений
                    def apply_gradient_total(s):
                        colors = []
                        for i, val in enumerate(s):
                            try:
                                numeric_val = total_growth_values[i]
                                if pd.isna(numeric_val):
                                    colors.append('')
                                else:
                                    # Нормализуем значение к диапазону 0-1
                                    if max_val != min_val:
                                        norm_val = (numeric_val - min_val) / (max_val - min_val)
                                    else:
                                        norm_val = 0.5
                                    
                                    # Применяем цветовую схему (красный для высоких значений)
                                    red_intensity = int(255 * norm_val)
                                    green_intensity = int(255 * (1 - norm_val))
                                    colors.append(f'background-color: rgb({red_intensity}, {green_intensity}, 100)')
                            except:
                                colors.append('')
                        return colors
                    
                    styled_df = styled_df.apply(apply_gradient_total, subset=['Total Growth (GB, %)'])
                    print(f"Применен градиент к столбцу 'Total Growth (GB, %)' (диапазон: {min_val:.2f} - {max_val:.2f})")
            
            # Градиент для промежуточных ростов
            for i in range(len(dates)-1):
                growth_col_name = f"Growth {dates[i]}→{dates[i+1]}"
                growth_col_original = f"growth_{dates[i]}_to_{dates[i+1]}"
                
                if growth_col_original in gradient_df_dedup.columns and growth_col_name in final_display_df.columns:
                    # Вычисляем абсолютные изменения в GB для градиента
                    prev_col = f"impact_size_gb_{dates[i]}"
                    next_col = f"impact_size_gb_{dates[i+1]}"
                    
                    if prev_col in gradient_df_dedup.columns and next_col in gradient_df_dedup.columns:
                        growth_gb_values = gradient_df_dedup[next_col] - gradient_df_dedup[prev_col]
                        
                        if len(growth_gb_values) > 0 and not np.isnan(growth_gb_values).all():
                            min_val = np.nanmin(growth_gb_values)
                            max_val = np.nanmax(growth_gb_values)
                            
                            def apply_gradient_growth(s, growth_values=growth_gb_values):
                                colors = []
                                for j, val in enumerate(s):
                                    try:
                                        numeric_val = growth_values.iloc[j] if hasattr(growth_values, 'iloc') else growth_values[j]
                                        if pd.isna(numeric_val):
                                            colors.append('')
                                        else:
                                            # Нормализуем значение к диапазону 0-1
                                            if max_val != min_val:
                                                norm_val = (numeric_val - min_val) / (max_val - min_val)
                                            else:
                                                norm_val = 0.5
                                            
                                            # Применяем цветовую схему
                                            red_intensity = int(255 * norm_val)
                                            green_intensity = int(255 * (1 - norm_val))
                                            colors.append(f'background-color: rgb({red_intensity}, {green_intensity}, 100)')
                                    except:
                                        colors.append('')
                                return colors
                            
                            styled_df = styled_df.apply(apply_gradient_growth, subset=[growth_col_name])
                            print(f"Применен градиент к столбцу '{growth_col_name}' (диапазон: {min_val:.2f} - {max_val:.2f})")
            
        except Exception as e:
            print(f"Предупреждение: не удалось применить градиенты - {str(e)}")
    
    # Устанавливаем заголовок и общие стили
    styled_df = styled_df.set_caption(
        f"Tables with growth >9% and size >100GB (compared {dates[0]} to {dates[-1]})"
    ).set_properties(**{
        'text-align': 'center',
        'border': '1px solid #ddd',
        'max-width': '150px',
        'font-size': '12px'
    })
    
    # Сохранение в HTML
    html_file = f"capacity_comparison_{current_date}.html"
    try:
        if hasattr(styled_df, 'to_html'):
            html_content = styled_df.to_html()
        else:
            html_content = styled_df.render()
        
        with open(html_file, 'w', encoding='utf-8-sig') as f:
            f.write(html_content)
        print(f"\nОтчет успешно сохранен в файл: {html_file}")
        
    except Exception as e:
        print(f"Ошибка при сохранении HTML: {str(e)}")
    
    # Вывод в Jupyter
    try:
        from IPython.display import display
        display(styled_df)
    except ImportError:
        print("Таблица готова к отображению (IPython.display недоступен)")

except Exception as e:
    print(f"Ошибка при создании таблицы: {str(e)}")
    # В случае ошибки стилизации, выводим простую таблицу
    try:
        print("\nВывод простой таблицы без стилизации:")
        print(final_display_df.to_string())
    except:
        print("Не удалось вывести таблицу")