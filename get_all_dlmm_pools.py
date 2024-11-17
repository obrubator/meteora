import requests
import json

def get_pait_info():
    url = "https://dlmm-api.meteora.ag/pair/all"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        print(json.dumps(data, indent=2))
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении информации о PAIT: {str(e)}")
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON ответа.")

if __name__ == "__main__":
    get_pait_info()
