import requests
import json
import time
import pickle

# Путь для сохранения состояния
STATE_FILE = 'dlmm_meteora_pools_state.pkl'

def load_previous_pools():
    try:
        with open(STATE_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def save_previous_pools(previous_pools):
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(previous_pools, f)

def get_dlmm_pools():
    url = "https://dlmm-api.meteora.ag/pair/all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении списка пулов: {str(e)}")
        return []
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON ответа.")
        return []

def check_for_new_pools(pools_data, previous_pools=None):
    if previous_pools is None:
        return pools_data
    
    new_pools = []
    for pool in pools_data:
        if pool['address'] not in [p['address'] for p in previous_pools]:
            new_pools.append(pool)
    
    return new_pools

def process_pool_info(pool):
    print(f"\nPool Address: {pool['address']}")
    print(f"Name: {pool['name']}")
    
    token_a = pool['mint_x']
    token_b = pool['mint_y']
    
    print(f"Token X: {token_a}")
    print(f"Token Y: {token_b}")
    
    print(f"Reserve X Amount: {pool['reserve_x_amount']}")
    print(f"Reserve Y Amount: {pool['reserve_y_amount']}")
    
    print(f"Liquidity: {float(pool['liquidity']):,.8f}")
    print(f"Current Price: {float(pool['current_price']):,.8f}")
    
    print(f"Base Fee Percentage: {pool['base_fee_percentage']}%")
    print(f"Max Fee Percentage: {pool['max_fee_percentage']}%")
    
    print(f"Cumulative Trade Volume: {float(pool['cumulative_trade_volume']):,.2f}")
    print(f"Cumulative Fee Volume: {float(pool['cumulative_fee_volume']):,.2f}")
    
    print(f"APR: {float(pool.get('apr', 0)):,.2f}%")
    print(f"APY: {float(pool.get('apy', 0)):,.2f}%")
    
    print(f"Farming APR: {float(pool.get('farm_apr', 0)):,.2f}%")
    print(f"Farming APY: {float(pool.get('farm_apy', 0)):,.2f}%")

def main():
    previous_pools = load_previous_pools()
    
    while True:
        pools_data = get_dlmm_pools()
        
        if pools_data:
            print(f"\nПроверка {len(pools_data)} пула(ов)...")
            
            new_pools = check_for_new_pools(pools_data, previous_pools)
            
            if new_pools:
                print(f"\nНайдено {len(new_pools)} новых пула(ов):")
                for pool in new_pools:
                    process_pool_info(pool)
            else:
                print("Новых пулов не найдено.")
            
            save_previous_pools(pools_data)
            previous_pools = pools_data
        
        time.sleep(30)

if __name__ == "__main__":
    main()
