from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import time
import random
import requests
from concurrent import futures

# URL вашего Go-сервиса
CALLBACK_URL = "http://localhost:8080/api/async/update-result"
executor = futures.ThreadPoolExecutor(max_workers=1)

def calculate_intermediate_energy(data):
    """
    Расчет промежуточной энергии ТОЧНО по вашим формулам.
    
    Принимает:
    {
        "combustion_id": 123,
        "fuel_id": 456,
        "fuel_volume": 10.5,      # FuelVolume из CombustionsFuels
        "heat": 50.2,             # Fuel.Heat
        "molar_mass": 16.04,      # Fuel.MolarMass
        "density": 0.85,          # Fuel.Density
        "is_gas": true,           # Fuel.IsGas
        "molar_volume": 22.414    # CombustionCalculation.MolarVolume
    }
    """
    # Извлекаем данные
    combustion_id = data["combustion_id"]
    fuel_id = data["fuel_id"]
    fuel_volume = float(data["fuel_volume"])
    heat = float(data["heat"])
    is_gas = data.get("is_gas", False)
    
    print(f"🔬 Начало расчета для combustion_id={combustion_id}, fuel_id={fuel_id}")
    print(f"   Объем: {fuel_volume}, Теплота: {heat}, Газ: {is_gas}")
    
    # 1. Имитация долгого расчета (5-10 секунд)
    delay = random.uniform(5, 10)
    print(f"   Задержка: {delay:.1f} секунд...")
    time.sleep(delay)
    
    # 2. РАСЧЕТ ПО ВАШИМ ФОРМУЛАМ
    intermediate_energy = 0
    
    if is_gas:
        # Для газа: heat * molar_mass * fuel_volume / molar_volume
        molar_mass = float(data.get("molar_mass", 0))
        molar_volume = float(data.get("molar_volume", 22.414))
        
        intermediate_energy = heat * molar_mass * fuel_volume / molar_volume
        
        print(f"   Формула газа: {heat} * {molar_mass} * {fuel_volume} / {molar_volume}")
    else:
        # Для жидкости: heat * density * fuel_volume
        density = float(data.get("density", 0))
        
        intermediate_energy = heat * density * fuel_volume
        
        print(f"   Формула жидкости: {heat} * {density} * {fuel_volume}")
    
    # Округляем до 4 знаков как в вашей БД
    result = round(intermediate_energy, 4)
    
    print(f"✅ Расчет завершен")
    print(f"   Результат: {result} кДж")
    
    # 3. Возвращаем результат
    return {
        "combustion_id": combustion_id,
        "fuel_id": fuel_id,
        "intermediate_energy": result,
        "calculation_time": round(delay, 2),
        "success": True  # Всегда успех по вашему требованию
    }

def send_result_to_go_service(task):
    """
    Отправка результата в Go-сервис.
    """
    try:
        result = task.result()
        
        combustion_id = result["combustion_id"]
        fuel_id = result["fuel_id"]
        energy = result["intermediate_energy"]
        
        # Токен для проверки (8 байт как в задании)
        TOKEN = "abc123def456"  # замените на ваш
        
        payload = {
            "combustion_id": combustion_id,
            "fuel_id": fuel_id,
            "result": energy,
            "token": TOKEN
        }
        
        print(f"📤 Отправка в Go-сервис...")
        print(f"   combustion_id: {combustion_id}, fuel_id: {fuel_id}")
        print(f"   energy: {energy} кДж")
        
        # Отправляем POST запрос
        response = requests.post(
            CALLBACK_URL,
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"✅ Результат отправлен успешно!")
        else:
            print(f"❌ Ошибка HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Ошибка в колбэке: {e}")

@api_view(['POST'])
def calculate_energy(request):
    """
    Запуск асинхронного расчета промежуточной энергии.
    
    Пример запроса:
    POST http://localhost:8001/calculate/
    
    {
        "combustion_id": 123,
        "fuel_id": 456,
        "fuel_volume": 10.5,
        "heat": 50.2,
        "molar_mass": 16.04,
        "density": 0.85,
        "is_gas": true,
        "molar_volume": 22.414
    }
    """
    # Проверяем обязательные поля
    required_fields = ['combustion_id', 'fuel_id', 'fuel_volume', 'heat']
    for field in required_fields:
        if field not in request.data:
            return Response({
                "error": f"Отсутствует обязательное поле: {field}",
                "required_fields": required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Преобразуем типы
        data = {
            "combustion_id": int(request.data["combustion_id"]),
            "fuel_id": int(request.data["fuel_id"]),
            "fuel_volume": float(request.data["fuel_volume"]),
            "heat": float(request.data["heat"]),
            "is_gas": bool(request.data.get("is_gas", False)),
            "molar_mass": float(request.data.get("molar_mass", 0)),
            "density": float(request.data.get("density", 0)),
            "molar_volume": float(request.data.get("molar_volume", 22.414))
        }
    except (ValueError, TypeError) as e:
        return Response({
            "error": "Некорректные типы данных",
            "details": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Проверяем данные для расчета
    if data["is_gas"] and data["molar_mass"] <= 0:
        return Response({
            "error": "Для газа требуется molar_mass > 0"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not data["is_gas"] and data["density"] <= 0:
        return Response({
            "error": "Для жидкости требуется density > 0"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Запускаем асинхронный расчет
    print(f"🚀 Запуск расчета для fuel_id={data['fuel_id']}")
    
    task = executor.submit(calculate_intermediate_energy, data)
    task.add_done_callback(send_result_to_go_service)
    
    # Немедленно отвечаем
    return Response({
        "status": "processing",
        "message": "Расчет промежуточной энергии запущен",
        "combustion_id": data["combustion_id"],
        "fuel_id": data["fuel_id"],
        "formula": "gas: heat * molar_mass * volume / molar_volume, liquid: heat * density * volume",
        "estimated_time": "5-10 секунд",
        "callback_url": CALLBACK_URL
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def health_check(request):
    """
    Проверка работоспособности сервиса.
    """
    return Response({
        "status": "healthy",
        "service": "Async Energy Calculation Service",
        "endpoint": "POST /calculate/",
        "formulas": {
            "gas": "intermediate_energy = heat * molar_mass * fuel_volume / molar_volume",
            "liquid": "intermediate_energy = heat * density * fuel_volume"
        }
    })