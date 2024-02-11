import matplotlib.pyplot as plt
from math import *


H = 5600 # характерестическая высота (м)
A = 19.625 # площадь поперечного сечения ракеты (м^2)
d = 2.32 # безразмерный коэффициент сопротивления формы
p0 = 1.225 # плотность воздуха (кг/м^3)
tanks_fuel_of_L110 = 116800 # количество топлива в баках L110 (кг)
tanks_fuel_of_S200 = 207000 # количество топлива в баках S200 (кг)
fuel_consumption_of_L110 = 558 # расход топлива двумя двигателями Vikas первой ступени L110 (кс/с)
fuel_consumption_of_S200 = 1820 # расход топлива твердотопливными ускорителями S200 (кс/с)
fuel_combustion_time_of_L110 = round(tanks_fuel_of_L110 / fuel_consumption_of_L110, 1) # время сгорания всего топлива первой ступении L110 (с)
fuel_combustion_time_of_S200 = round(tanks_fuel_of_S200 / fuel_consumption_of_S200, 1) # время сгорания всего топлива в твердотопливных ускорителях (с)
thrust_L110 = 863200 * 2 # тяга ступени L110 (кН)
thrust_S200 = 4942300 * 2 #  суммарная тяга ускорителей S200 (кН)
time_start_L110 = fuel_combustion_time_of_S200 # момент времени, когда запустились двигатели Vikas (топливо в S200 закончилось)
time_end_L110 = fuel_combustion_time_of_S200 + fuel_combustion_time_of_L110 # момент времени, когда топливо закончилось в L110 (остоединение L110)
time_end_S200 =  fuel_combustion_time_of_S200 # момент времени, когда топливо в S200 закончилось (отсоединение S200)
mass_L110 = 9670 + tanks_fuel_of_L110 # масса первой ступени L110, поститанная с топливом
mass_S200 = (30760 + tanks_fuel_of_S200) * 2 # суммарная масса ускорителей S200, посчитанная с весом топлива
other_mass = 44538 # масса отсльных, неважных для построения математической модели, компонентов летательного аппарата
mass = other_mass + mass_L110 + mass_S200

mass_changes_list = [mass] # список, хранящий значение массы в конкретный момент времени, интервалы записи значения в список определяются переменной dt
time_points = [round(i / 10, 1) for i in range(1, int((time_end_L110) * 10))] # список временых отметок, "отмеченных на числовой оси графиков"
dt = 0.1 # Шаг по времени

vx = [0] # список, хранящий значения проекции скорости по горизонтальной оси в переодичные моменты времени
vy = [0] # список, хранящий значения проекции скорости по вертикальной оси в переодичные моменты времени
x = [0] # список, хранящий значения координаты по горизонтальной оси оси в переодичные моменты времени 
y = [15] # список, хранящий значения координаты по вертикальной оси в переодичные моменты времени (начальная высота 15, так как KSP определяет высоту в начальный момент около 15 м)
height_list = list() # список, хранящий значения высоты летательного аппарата в переодичные моменты времени
pitch = [90] # список, хранящий значения угла наклона относительно начального горизонта в переодичные моменты времени

altitude_file = open("file_altitude.txt", 'r') 

for line in altitude_file:
    data = line.split()
    height_list.append(float(data[1])) # распределение данных из файла
    pitch.append(round(float(data[2]), 2)) # распределение данных из файла

num_of_lines = len(pitch) # число строк в файле 

default_time = 0.1 # счётчик времени для S200  
since_start_L110 = 0.1 # счётчик времени для L110

while default_time <= time_end_L110: # условие входа в цикл - наличие топлива
    flag = True # флаг старта since_start_L110
    
    if default_time < time_start_L110: # время, когда работают только S200
        mass_changes_list.append(mass - 2 * fuel_consumption_of_S200 * default_time)
        flag = False
        
    elif time_end_S200 <= default_time < time_end_L110: # время, когда работает только L110
        mass_changes_list.append(mass - mass_S200 - fuel_consumption_of_L110 * since_start_L110) 
        
    elif default_time == time_end_L110: # время, когда L110 перестает работать
        mass_changes_list.append(mass - mass_S200 - mass_L110) 
    
    if flag: # если flag == True, то это означает, что нужно вести подсчет времени работы L110
        since_start_L110 = round(since_start_L110 + dt, 1)
    default_time = round(default_time + dt, 1) # подсчет времени default_time
          
dt = 0.117 # усреденное значение интервала логирования

default_time = 0.1 # счетчик времени
for i in range(1, num_of_lines): # вычисление изменения высоты согласно математической модели
    j = i - 1 # для читаемости кода ниже
    
    if default_time < time_start_L110: # время, когда работают только S200
        thrust = thrust_S200
        
    elif time_end_S200 <= default_time <= time_end_L110: # время, когда работает только L110
        thrust = thrust_L110
    
    vy.append(vy[j] + dt * (thrust * sin(pitch[j] * pi / 180) - mass_changes_list[j] * 9.81 - 0.5 * p0 * exp(-y[j] / H)
                                * d * A * vy[j] ** 2 * sin(pitch[j] * pi / 180)) / mass_changes_list[j])
    y.append(y[j] + vy[i] * dt) # подсчет высоты в момент default_time    
    default_time = round(default_time + dt, 1) # подсчет времени default_time

# # Вывод графика зависимости высоты от времени
plt.title("График зависимости высоты от времени")
plt.xlabel("время, c")
plt.ylabel("высота, м")
plt.grid()
plt.plot(time_points[:num_of_lines-1], height_list[:num_of_lines-1], color='#32CD32',label="Kerbal Space Program")
plt.plot(time_points[:num_of_lines-1], y[:num_of_lines-1], color='#CD5C5C', linewidth=2, label="Математическая модель")
plt.legend()
plt.show()

velocity_file = open("file_velocity.txt", 'r') 
vx = [0] # перезапись данных
vy = [0] # перезапись данных
x = [0] # перезапись данных
y = [15] # перезапись данных
pitch = list([90]) # перезапись данных
mass_changes_list = [mass] # перезапись данных
time_list = list() # спискок для временных отметок
speedfile = list() # список, предназначенный для записи значений абсолютной скорости, полученной из проекций скоростей

dt = 0.1 # тут изменился шаг по времени, т.к. при выгрузке данных о скорости в ksp не удалось достичь 0.1

for line in velocity_file:
    data = line.split()
    time_list.append(round(float(data[0]), 2)) # распределение данных из файла
    pitch.append(round(float(data[1]), 2)) # распределение данных из файла
    speedfile.append(round(float(data[2]), 2)) # распределение данных из файла

    
num_of_lines = len(pitch) # число строк в файле 

default_time = 0.1 # счётчик времени для S200  
since_start_L110 = 0.1 # счётчик времени для L110

while default_time <= time_end_L110:
    flag = True # флаг старта since_start_L110
    
    if default_time < time_start_L110: # время, когда работают только S200
        mass_changes_list.append(mass - 2 * fuel_consumption_of_S200 * default_time) 
        flag = False
    
    elif time_end_S200 <= default_time < time_end_L110: # для момента работы l110
        mass_changes_list.append(mass - mass_S200  - fuel_consumption_of_L110 * since_start_L110) 
    
    elif default_time == time_end_L110: # для момента окончания работы l110
        mass_changes_list.append(mass - mass_S200 - mass_L110) 
        
    if flag: # если flag == True, то это означает, что нужно вести подсчет времени работы L110
        since_start_L110 = round(since_start_L110 + dt,1)
        
    default_time = round(default_time + dt,1) # подсчет времени default_time
    
default_time = 0.15
        
for i in range(1, num_of_lines): # вычисление изменения скорости согласно математической модели
    j = i - 1 # для читаемости кода ниже
    
    if default_time < time_start_L110:
        thrust = thrust_S200
          
    elif time_end_S200 <= default_time <= time_end_L110:
        thrust = thrust_L110
    
    vx.append(vx[j] + dt * (thrust * cos(pitch[j] * pi / 180) - 0.5 * p0 * exp(-y[j] / H) * d * A * vx[j] ** 2
                            * cos(pitch[j] * pi / 180)) / mass_changes_list[j])     
    vy.append(vy[j] + dt * (thrust * sin(pitch[j] * pi / 180) - mass_changes_list[j] * 9.81 - 0.5 * p0 * exp(-y[j] / H)
                            * d * A * vy[j] ** 2 * sin(pitch[j] * pi / 180)) / mass_changes_list[j])
    y.append(y[j] + vy[i] * dt)
    default_time = round(default_time + dt, 2)        
        
index = 815
velocity = [sqrt(vx[i] ** 2 + vy[i] ** 2) for i in range(index)] 

# Вывод графика зависимости скорости от времени
plt.title("График зависимости скорости от времени") 
plt.xlabel("время, c")
plt.ylabel("скорость, м/c")
plt.grid()
plt.plot(time_list[:index-1], speedfile[:index-1], color='#32CD32',label="Kerbal Space Program")
plt.plot(time_list[:index-1], velocity[:index-1], color='#CD5C5C', linewidth=2, label="Математическая модель")
plt.legend()
plt.show()