import requests

# Ganti dengan API key Anda
API_KEY = "AIzaSyD7_PAF98KwkGPGSHLWPmBF1GsXDAyxEA8"

# Cek model yang tersedia
url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("=" * 60)
    print("MODEL YANG TERSEDIA UNTUK API KEY ANDA:")
    print("=" * 60)
    
    if 'models' in data:
        for model in data['models']:
            name = model.get('name', 'Unknown')
            display_name = model.get('displayName', 'Unknown')
            supported_methods = model.get('supportedGenerationMethods', [])
            
            # Cek apakah support generateContent
            if 'generateContent' in supported_methods:
                print(f"\n✅ {name}")
                print(f"   Display Name: {display_name}")
                print(f"   Methods: {', '.join(supported_methods)}")
    else:
        print("Tidak ada model ditemukan")
        print(data)
else:
    print(f"Error {response.status_code}:")
    print(response.json())

print("\n" + "=" * 60)
