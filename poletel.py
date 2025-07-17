# Импорт необходимых библиотек
import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from clover.srv import SetLEDEffect

# Инициализация ноды 'flight'
rospy.init_node('flight')

# Создание объектов-прокси для работы с сервисами
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

# Функция для ожидания прилёта в navigate-точку
def wait_arrival(tolerance=0.2):
    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

# Алгоритм полёта
set_effect(effect='fill', r=0, g=0, b=255)  # Залить всю строку светодиодной ленты синим цветом
navigate(z=1.5, auto_arm=True, frame_id='body')  # Взлёт на высоту 1.5 метра
wait_arrival()
navigate(y=-0.5, z=1.5, frame_id='aruco_24')  # Полёт в коородинаты x=0, y=-0.5, z=1.5 относительно аруко маркера 24
wait_arrival()
set_effect(effect='fade', r=0, g=255, b=0  # Плавное перетекание цветов светодиодной ленты в зелёный цвет
rospy.sleep(3)  # Задержка 3 секунды
navigate(y=0.5, z=1.5, frame_id='aruco_24')  #  Полёт в коородинаты x=0, y=0.5, z=1.5 относительно аруко маркера 24
wait_arrival()
set_effect(effect='wipe', r=255, g=255, b=0)  # "надвигание" жёлтого цвета на светодиодной ленте
rospy.sleep(3)  # Задержка 3 секунды
navigate(y=0.5, z=2, frame_id='aruco_24')  # Полёт в коородинаты x=0, y=0.5, z=2 относительно аруко маркера 24
wait_arrival()
set_effect(effect='blink', r=0, g=255, b=255)  # Мигание светодиодной ленты бирюзовым цветом
rospy.sleep(3)  # Задержка 3 секунды
navigate(y=-0.5, z=2, frame_id='aruco_24')  # Полёт в коородинаты x=0, y=-0.5, z=2 относительно аруко маркера 24
wait_arrival()
set_effect(effect='blink_fast', r=255, g=255, b=255)  # Быстрое мигание светодиодной ленты белым цветом
wait_arrival()
rospy.sleep(3)  #  Задержка 3 секунды
navigate(z=2, frame_id='aruco_42')  # Полёт в координаты x=0, y=0, z=2 относительно аруко маркера 42
set_effect(effect='rainbow')  # Переливание светодиодной ленты цветами радуги
wait_arrival()
land()  # Посадка
