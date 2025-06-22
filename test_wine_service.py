import requests 
import json 
import time 
 
# Wine test data from UCI dataset 
sample_wines = [ 
    { 
        "name": "Average Red Wine", 
        "data": { 
            "fixed_acidity": 7.4, 
            "volatile_acidity": 0.70, 
            "citric_acid": 0.00, 
            "residual_sugar": 1.9, 
            "chlorides": 0.076, 
            "free_sulfur_dioxide": 11.0, 
            "total_sulfur_dioxide": 34.0, 
            "density": 0.9978, 
            "pH": 3.51, 
            "sulphates": 0.56, 
            "alcohol": 9.4 
        } 
    } 
] 
 
def test_wine_service(): 
    base_url = "http://localhost:3333" 
    print("🍷 Testing John's Wine Quality Service") 
    try: 
        response = requests.get(f"{base_url}/wine-health") 
        if response.status_code == 200: 
            print("✅ Wine Service is running") 
            return True 
        else: 
            print("❌ Wine Service health check failed") 
            return False 
    except Exception as e: 
        print(f"❌ Connection error: {e}") 
        return False 
 
if __name__ == "__main__": 
    test_wine_service() 
