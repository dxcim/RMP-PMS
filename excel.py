from openpyxl import load_workbook

wb = load_workbook(filename='dataset.xlsx')
data = wb.active
readings = ""

for i in range(3, 2000):
    col = "E" + str(i)
    if int(data[col].value) < 89:
        #upd_col = "K" +str(i)
        readings = "Low SpO2 Levels "
    col = "G" + str(i)
    next_col = "G" + str(i+1)
    prev_col = "G" + str(i-1)
    hr_col = "D" + str(i)
    if data[col].value == data[prev_col].value + 1:
        data[hr_col].value += 7
    elif data[col].value == data[prev_col].value - 1:
        data[hr_col].value -= 7
    if data[col].value > 38:
        readings += "High Temperature"
    elif data[col].value < 36:
        readings += "Low Temperature"
    data["K" + str(i)] = readings