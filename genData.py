import openpyxl
import random
import pandas as pd


def gen_sheet(filename, headers, data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for col, header in enumerate(headers.keys(), start=1):
        sheet.cell(row=1, column=col, value=header)

    for row, point_data in enumerate(data, start=2):
        for col, key in enumerate(headers.keys(), start=1):
            sheet.cell(row=row, column=col, value=point_data[key])

    workbook.save(filename)


def gen_points_name(qtd):
    names: list[str] = []
    for name in range(1, qtd+1):
        names.append(f"Ponto{name}")
    return names


def gen_random_data(points, headers, qtd, start_date, end_date):
    data = []
    date_range = pd.date_range(start_date, end_date)
    date_iter = iter(date_range)

    for point in points:
        for _ in range(qtd):
            try:
                date = next(date_iter)  # Get the next date from the iterator
            except StopIteration:  # If all dates have been used, raise an error
                raise ValueError("Quantity exceeds available dates in the specified time interval.")

            point_data = {"Ponto": point, "Data": date.strftime("%Y-%m-%d")}
            # point_data = {"Ponto": random.choice(points), "Data": date.strftime("%Y-%m-%d")}
            for key, limits in headers.items():
                if key != "Ponto" and limits is not None:
                    min_limit, max_limit = limits
                    value = round(random.uniform(min_limit, max_limit), 2)
                    point_data[key] = value
            data.append(point_data)

    # Modify 10% of the values in each column to be outliers
    for key, limits in headers.items():
        if key != "Ponto" and key != "Data" and limits is not None:
            num_points_to_modify = int(len(data) * 0.1)
            points_to_modify = random.sample(data, num_points_to_modify)

            for point in points_to_modify:
                min_limit, max_limit = limits
                outlier_value = random.uniform(max_limit * 1.1, max_limit * 2)  # Adjust range for outliers
                point[key] = round(outlier_value, 2)
    return data


#Header can be changed to ur neccesity, try like: "header  name": (x,y) also: x is lower_limit and y is upper_limit
headers = {
    "Ponto": None,
    "Data": None,
    "Temperatura da água (°C)": (20, 32),
    "pH": (6, 9),
    "Coliformes Termotolerantes": (0, 4000),
    "Turbidez": (0, 5),
    "Oxigênio Dissolvido": (5, 20),
    "Demanda bioquímica de oxigênio": (2, 8),
    "Solidos Totais": (0, 200),
    "Fósforo total":(0,5),
    "Nitrogênio total":(0,5)
}

points = gen_points_name(10)
data = gen_random_data(points, headers, 500,"2000-01-01","2024-01-30")
gen_sheet("dados_with_10%_outlier.xlsx", headers, data)
