from nsepython import nse_get_index_quote, nse_quote_ltp, nse_quote
import json

try:
    print("Fetching NIFTY 50...")
    nifty = nse_get_index_quote("nifty 50")
    print(f"NIFTY: {nifty}")
except Exception as e:
    print(f"NIFTY Error: {e}")

try:
    print("Fetching TRIDENT...")
    trident = nse_quote("TRIDENT")
    print(f"TRIDENT: {trident}")
except Exception as e:
    print(f"TRIDENT Error: {e}")

try:
    print("Fetching VIKASECO...")
    vikas = nse_quote("VIKASECO")
    print(f"VIKASECO: {vikas}")
except Exception as e:
    print(f"VIKASECO Error: {e}")
