#!/usr/bin/env python3
""" ____  __  ______  _   _____________   ________________ 
   / __ \/ / / / __ \/ | / / ____/  _/ | / /_  __/ ____/ / 
  / /_/ / /_/ / / / /  |/ / __/  / //  |/ / / / / __/ / /  
 / ____/ __  / /_/ / /|  / /____/ // /|  / / / / /___/ /___
/_/   /_/ /_/\____/_/ |_/_____/___/_/ |_/ /_/ /_____/_____/

PhoneNum Locator - Track phone number location, carrier & generate map.
Works on Termux (Android) and standard Linux/macOS terminals.
Author: SAKSHAM GUPTA
"""

import sys
import os
import re
import json
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import init, Fore, Style

init(autoreset=True)

# Configuration
CONFIG_FILE = "config.py"
OPENCAGE_API_KEY = None

def load_config():
    global OPENCAGE_API_KEY
    try:
        if os.path.exists(CONFIG_FILE):
            from config import OPENCAGE_API_KEY as KEY
            OPENCAGE_API_KEY = KEY
            return True
        return False
    except (ImportError, ModuleNotFoundError):
        return False

# Country Code Mapping 
COUNTRY_CODES = {
    "afghanistan": "AF", "albania": "AL", "algeria": "DZ", "andorra": "AD",
    "angola": "AO", "argentina": "AR", "armenia": "AM", "australia": "AU",
    "austria": "AT", "azerbaijan": "AZ", "bahrain": "BH", "bangladesh": "BD",
    "belarus": "BY", "belgium": "BE", "bolivia": "BO", "bosnia": "BA",
    "brazil": "BR", "brunei": "BN", "bulgaria": "BG", "cambodia": "KH",
    "cameroon": "CM", "canada": "CA", "chile": "CL", "china": "CN",
    "colombia": "CO", "costa rica": "CR", "croatia": "HR", "cuba": "CU",
    "cyprus": "CY", "czech": "CZ", "czech republic": "CZ", "denmark": "DK",
    "dominican republic": "DO", "ecuador": "EC", "egypt": "EG", "el salvador": "SV",
    "estonia": "EE", "ethiopia": "ET", "finland": "FI", "france": "FR",
    "georgia": "GE", "germany": "DE", "ghana": "GH", "greece": "GR",
    "guatemala": "GT", "honduras": "HN", "hong kong": "HK", "hungary": "HU",
    "iceland": "IS", "india": "IN", "indonesia": "ID", "iran": "IR",
    "iraq": "IQ", "ireland": "IE", "israel": "IL", "italy": "IT",
    "jamaica": "JM", "japan": "JP", "jordan": "JO", "kazakhstan": "KZ",
    "kenya": "KE", "kuwait": "KW", "kyrgyzstan": "KG", "laos": "LA",
    "latvia": "LV", "lebanon": "LB", "libya": "LY", "liechtenstein": "LI",
    "lithuania": "LT", "luxembourg": "LU", "macau": "MO", "madagascar": "MG",
    "malaysia": "MY", "maldives": "MV", "mali": "ML", "malta": "MT",
    "mauritius": "MU", "mexico": "MX", "monaco": "MC", "mongolia": "MN",
    "montenegro": "ME", "morocco": "MA", "myanmar": "MM", "namibia": "NA",
    "nepal": "NP", "netherlands": "NL", "new zealand": "NZ", "nicaragua": "NI",
    "nigeria": "NG", "north korea": "KP", "norway": "NO", "oman": "OM",
    "pakistan": "PK", "palestine": "PS", "panama": "PA", "paraguay": "PY",
    "peru": "PE", "philippines": "PH", "poland": "PL", "portugal": "PT",
    "puerto rico": "PR", "qatar": "QA", "romania": "RO", "russia": "RU",
    "saudi arabia": "SA", "senegal": "SN", "serbia": "RS", "singapore": "SG",
    "slovakia": "SK", "slovenia": "SI", "somalia": "SO", "south africa": "ZA",
    "south korea": "KR", "spain": "ES", "sri lanka": "LK", "sudan": "SD",
    "sweden": "SE", "switzerland": "CH", "syria": "SY", "taiwan": "TW",
    "tajikistan": "TJ", "tanzania": "TZ", "thailand": "TH", "tunisia": "TN",
    "turkey": "TR", "turkmenistan": "TM", "uganda": "UG", "ukraine": "UA",
    "united arab emirates": "AE", "united kingdom": "GB", "uk": "GB",
    "usa": "US", "united states": "US", "uruguay": "UY", "uzbekistan": "UZ",
    "vatican city": "VA", "venezuela": "VE", "vietnam": "VN", "yemen": "YE",
    "zambia": "ZM", "zimbabwe": "ZW",
}

# Indian States Ka Direct Mapping 
# Kuch states ke STD codes / area patterns se direct match
INDIA_STATE_KEYWORDS = {
    "andhra pradesh": "andhra pradesh",
    "ap": "andhra pradesh",
    "arunachal pradesh": "arunachal pradesh",
    "assam": "assam",
    "bihar": "bihar",
    "chhattisgarh": "chhattisgarh",
    "goa": "goa",
    "gujarat": "gujarat",
    "haryana": "haryana",
    "himachal pradesh": "himachal pradesh",
    "hp": "himachal pradesh",
    "jharkhand": "jharkhand",
    "karnataka": "karnataka",
    "kerala": "kerala",
    "madhya pradesh": "madhya pradesh",
    "mp": "madhya pradesh",
    "maharashtra": "maharashtra",
    "manipur": "manipur",
    "meghalaya": "meghalaya",
    "mizoram": "mizoram",
    "nagaland": "nagaland",
    "odisha": "odisha",
    "orissa": "odisha",
    "punjab": "punjab",
    "rajasthan": "rajasthan",
    "sikkim": "sikkim",
    "tamil nadu": "tamil nadu",
    "tn": "tamil nadu",
    "telangana": "telangana",
    "tripura": "tripura",
    "uttar pradesh": "uttar pradesh",
    "up": "uttar pradesh",
    "uttarakhand": "uttarakhand",
    "uk": "uttarakhand",
    "west bengal": "west bengal",
    "wb": "west bengal",
    "delhi": "delhi",
    "new delhi": "delhi",
    "chandigarh": "chandigarh",
    "puducherry": "puducherry",
    "pondicherry": "puducherry",
    "jammu and kashmir": "jammu & kashmir",
    "jammu & kashmir": "jammu & kashmir",
    "ladakh": "ladakh",
    "andaman": "andaman & nicobar",
    "andaman & nicobar": "andaman & nicobar",
    "dadra": "dadra & nagar haveli",
    "daman": "daman & diu",
    "lakshadweep": "lakshadweep",
}

# US State Mapping
US_STATE_KEYWORDS = {
    "alabama": "alabama", "al": "alabama",
    "alaska": "alaska", "ak": "alaska",
    "arizona": "arizona", "az": "arizona",
    "arkansas": "arkansas", "ar": "arkansas",
    "california": "california", "ca": "california",
    "colorado": "colorado", "co": "colorado",
    "connecticut": "connecticut", "ct": "connecticut",
    "delaware": "delaware", "de": "delaware",
    "florida": "florida", "fl": "florida",
    "georgia": "georgia", "ga": "georgia",
    "hawaii": "hawaii", "hi": "hawaii",
    "idaho": "idaho", "id": "idaho",
    "illinois": "illinois", "il": "illinois",
    "indiana": "indiana", "in": "indiana",
    "iowa": "iowa", "ia": "iowa",
    "kansas": "kansas", "ks": "kansas",
    "kentucky": "kentucky", "ky": "kentucky",
    "louisiana": "louisiana", "la": "louisiana",
    "maine": "maine", "me": "maine",
    "maryland": "maryland", "md": "maryland",
    "massachusetts": "massachusetts", "ma": "massachusetts",
    "michigan": "michigan", "mi": "michigan",
    "minnesota": "minnesota", "mn": "minnesota",
    "mississippi": "mississippi", "ms": "mississippi",
    "missouri": "missouri", "mo": "missouri",
    "montana": "montana", "mt": "montana",
    "nebraska": "nebraska", "ne": "nebraska",
    "nevada": "nevada", "nv": "nevada",
    "new hampshire": "new hampshire", "nh": "new hampshire",
    "new jersey": "new jersey", "nj": "new jersey",
    "new mexico": "new mexico", "nm": "new mexico",
    "new york": "new york", "ny": "new york",
    "north carolina": "north carolina", "nc": "north carolina",
    "north dakota": "north dakota", "nd": "north dakota",
    "ohio": "ohio", "oh": "ohio",
    "oklahoma": "oklahoma", "ok": "oklahoma",
    "oregon": "oregon", "or": "oregon",
    "pennsylvania": "pennsylvania", "pa": "pennsylvania",
    "rhode island": "rhode island", "ri": "rhode island",
    "south carolina": "south carolina", "sc": "south carolina",
    "south dakota": "south dakota", "sd": "south dakota",
    "tennessee": "tennessee", "tn": "tennessee",
    "texas": "texas", "tx": "texas",
    "utah": "utah", "ut": "utah",
    "vermont": "vermont", "vt": "vermont",
    "virginia": "virginia", "va": "virginia",
    "washington": "washington", "wa": "washington",
    "west virginia": "west virginia", "wv": "west virginia",
    "wisconsin": "wisconsin", "wi": "wisconsin",
    "wyoming": "wyoming", "wy": "wyoming",
}

STATE_MAP = {
    "IN": INDIA_STATE_KEYWORDS,
    "US": US_STATE_KEYWORDS,
}

# ─── Banner ──────────────────────────────────────────────────
BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║       {Fore.GREEN}📞 Phoneintel{Fore.CYAN}          ║
║   {Fore.YELLOW}Phone Number Locator    {Fore.CYAN}  ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}"""

def print_banner():
    print(BANNER)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Extract State from Location String 
def extract_state_from_location(location_text, iso_code):
    """Location string se state extract karo (jaise 'Maharashtra, India' se 'Maharashtra')."""
    if not location_text or location_text == "Unknown":
        return None

    location_lower = location_text.lower()
    
    # Pehle commas se split karo
    parts = [p.strip() for p in location_lower.split(",")]
    
    # Country-specific state detection
    if iso_code == "IN":
        # Kisi bhi part mein Indian state ka naam hai?
        for keyword, state in INDIA_STATE_KEYWORDS.items():
            for part in parts:
                if keyword in part:
                    return state.title()
        # Direct match nahi mila to pehla non-country part do
        for part in parts:
            if "india" not in part and part.strip():
                return part.strip().title()
    
    elif iso_code == "US":
        for keyword, state in US_STATE_KEYWORDS.items():
            for part in parts:
                if keyword in part:
                    return state.title()
        for part in parts:
            if "united states" not in part and "usa" not in part and part.strip():
                return part.strip().title()
    
    # Fallback: pehla meaningful part
    for part in parts:
        country_variants = ["india", "united states", "usa", "uk", "united kingdom", 
                           "germany", "australia", "canada", "china", "japan"]
        if part.strip() and part.strip() not in country_variants:
            return part.strip().title()
    
    return None

# Country Prompt
def country_prompt():
    print(f"\n{Fore.YELLOW}[?] Enter the country name (e.g., India, USA, Germany):{Style.RESET_ALL}")
    country_input = input(f"{Fore.CYAN}└─> {Style.RESET_ALL}").strip().lower()

    if country_input in COUNTRY_CODES:
        iso_code = COUNTRY_CODES[country_input]
        print(f"{Fore.GREEN}[✓] Country detected: {country_input.title()} (ISO: {iso_code}){Style.RESET_ALL}")
        return iso_code, country_input.title()
    else:
        print(f"{Fore.RED}[✗] Country '{country_input}' not found in database.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Please enter the ISO country code directly (e.g., IN, US, DE):{Style.RESET_ALL}")
        iso_code = input(f"{Fore.CYAN}└─> {Style.RESET_ALL}").strip().upper()
        return iso_code, country_input.title()

# State Prompt
def state_prompt(iso_code):
    """Puchho ki user state batana chahta hai ya nahi."""
    print(f"\n{Fore.YELLOW}[?] Do you know which state this number belongs to? (y/n){Style.RESET_ALL}")
    choice = input(f"{Fore.CYAN}└─> {Style.RESET_ALL}").strip().lower()
    
    if choice in ["y", "yes", "yeah", "ha", "h", "haan"]:
        print(f"\n{Fore.YELLOW}[?] Enter the state name (e.g., Maharashtra, California, Texas):{Style.RESET_ALL}")
        user_state = input(f"{Fore.CYAN}└─> {Style.RESET_ALL}").strip().lower()
        
        # Check in state map
        state_map_for_country = STATE_MAP.get(iso_code, {})
        matched_state = None
        for keyword, state in state_map_for_country.items():
            if keyword == user_state or user_state in keyword or keyword in user_state:
                matched_state = state
                break
        
        if matched_state:
            print(f"{Fore.GREEN}[✓] State recognized: {matched_state.title()}{Style.RESET_ALL}")
            return matched_state
        else:
            print(f"{Fore.YELLOW}[!] State '{user_state.title()}' not in our database. Will auto-detect.{Style.RESET_ALL}")
            return user_state
    
    elif choice in ["n", "no", "nahi", "nhi"]:
        print(f"{Fore.CYAN}[*] No problem! Will auto-detect the state from the number.{Style.RESET_ALL}")
        return None
    
    else:
        print(f"{Fore.YELLOW}[!] Didn't understand. Will auto-detect.{Style.RESET_ALL}")
        return None

#  Phone Prompt 
def phone_prompt(iso_code):
    print(f"\n{Fore.YELLOW}[?] Enter the phone number (without country code; e.g., 9876543210):{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    Or enter with '+' and full country code (e.g., +919876543210):{Style.RESET_ALL}")
    number_input = input(f"{Fore.CYAN}└─> {Style.RESET_ALL}").strip()

    if number_input.startswith("+"):
        raw_number = number_input
    else:
        raw_number = number_input

    try:
        parsed = phonenumbers.parse(raw_number, iso_code)
        if not phonenumbers.is_valid_number(parsed):
            print(f"{Fore.RED}[✗] Invalid phone number for {iso_code}.{Style.RESET_ALL}")
            return None
        return parsed
    except phonenumbers.NumberParseException as e:
        print(f"{Fore.RED}[✗] Error parsing number: {e}{Style.RESET_ALL}")
        return None

# Get Location Info
def get_location_info(parsed):
    info = {}

    location = geocoder.description_for_number(parsed, "en")
    info["location"] = location if location else "Unknown"

    carrier_name = carrier.name_for_number(parsed, "en")
    info["carrier"] = carrier_name if carrier_name else "Unknown"

    tz_list = timezone.time_zones_for_number(parsed)
    info["timezones"] = ", ".join(tz_list) if tz_list else "Unknown"

    info["country_code"] = f"+{parsed.country_code}"
    info["national_number"] = phonenumbers.format_number(
        parsed, phonenumbers.PhoneNumberFormat.NATIONAL
    )
    info["international_number"] = phonenumbers.format_number(
        parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
    )

    number_type_map = {
        0: "Fixed Line",
        1: "Mobile",
        2: "Fixed Line or Mobile",
        3: "Toll Free",
        4: "Premium Rate",
        5: "Shared Cost",
        6: "VoIP",
        7: "Personal Number",
        8: "Pager",
        9: "Universal Access Number",
        10: "Voicemail",
    }

    ntype = phonenumbers.number_type(parsed)
    info["number_type"] = number_type_map.get(ntype, "Unknown")
    info["is_valid"] = phonenumbers.is_valid_number(parsed)
    info["is_possible"] = phonenumbers.is_possible_number(parsed)

    return info
# State Match Check 
def check_state_match(detected_state, user_state, iso_code):
    """Check karo ki user ka diya hua state, detected state se match karta hai ya nahi."""
    if not user_state or not detected_state:
        return None  # Koi comparison possible nahi
    
    user_lower = user_state.lower().strip()
    detected_lower = detected_state.lower().strip()
    
    if user_lower == detected_lower:
        return True
    # Partial match bhi check karo
    if user_lower in detected_lower or detected_lower in user_lower:
        return True
    
    return False

# Geocode with OpenCage 
def geocode_with_opencage(location_name):
    if not OPENCAGE_API_KEY:
        return None, None, None
    
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": location_name,
        "key": OPENCAGE_API_KEY,
        "language": "en",
        "limit": 1,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data["results"]:
            geom = data["results"][0]["geometry"]
            formatted = data["results"][0]["formatted"]
            return geom["lat"], geom["lng"], formatted
        return None, None, None
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Geocoding API error: {e}{Style.RESET_ALL}")
        return None, None, None

# Generate Map 
def generate_map(lat, lng, location_name, number_info):
    try:
        import folium
    except ImportError:
        print(f"{Fore.YELLOW}[!] Folium not installed. Skipping map.{Style.RESET_ALL}")
        return
    
    clean_num = number_info["international_number"].replace(" ", "_").replace("+", "")
    filename = f"location_{clean_num}.html"
    
    my_map = folium.Map(location=[lat, lng], zoom_start=10)
    
    popup_text = f"""
    <b>📍 Number:</b> {number_info['international_number']}<br>
    <b>🌍 Location:</b> {location_name}<br>
    <b>📡 Carrier:</b> {number_info['carrier']}<br>
    <b>📄 Type:</b> {number_info['number_type']}<br>
    <b>🕐 Timezone:</b> {number_info['timezones']}
    """
    
    folium.Marker(
        [lat, lng],
        popup=folium.Popup(popup_text, max_width=350),
        tooltip=location_name,
        icon=folium.Icon(color="red", icon="phone", prefix="fa")
    ).add_to(my_map)
    
    my_map.save(filename)
    print(f"{Fore.GREEN}[✓] Map saved: {filename}{Style.RESET_ALL}")

# Display Results 
def display_results(info, detected_state, user_state, state_match, lat=None, lng=None):
    """Sab kuch display karo with state comparison."""
    print(f"\n{Fore.CYAN}══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📊 PHONE NUMBER INTELLIGENCE REPORT{Style.RESET_ALL}")
    print(f"{Fore.CYAN}══════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}📞 Number Information:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}International:{Style.RESET_ALL}    {Fore.GREEN}{info['international_number']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}National:{Style.RESET_ALL}         {Fore.GREEN}{info['national_number']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Country Code:{Style.RESET_ALL}     {Fore.GREEN}{info['country_code']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Valid:{Style.RESET_ALL}            {'✅ Yes' if info['is_valid'] else '❌ No'}")
    print(f"  {Fore.WHITE}Possible:{Style.RESET_ALL}         {'✅ Yes' if info['is_possible'] else '❌ No'}")
    
    print(f"\n{Fore.YELLOW}📌 Location & State:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Full Location:{Style.RESET_ALL}    {Fore.GREEN}{info['location']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Detected State:{Style.RESET_ALL}   {Fore.CYAN}{detected_state if detected_state else 'Could not determine'}{Style.RESET_ALL}")
    
    # State match result
    if user_state:
        print(f"  {Fore.WHITE}You entered:{Style.RESET_ALL}      {Fore.YELLOW}{user_state.title()}{Style.RESET_ALL}")
        if state_match is True:
            print(f"  {Fore.GREEN}✅ MATCH: Number IS registered in {user_state.title()}{Style.RESET_ALL}")
        elif state_match is False:
            print(f"  {Fore.RED}❌ MISMATCH: Number is registered in {detected_state}, NOT {user_state.title()}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}⚠️  Could not verify state match.{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}📡 Network Info:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Carrier:{Style.RESET_ALL}          {Fore.GREEN}{info['carrier']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Number Type:{Style.RESET_ALL}      {Fore.GREEN}{info['number_type']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Timezone(s):{Style.RESET_ALL}      {Fore.GREEN}{info['timezones']}{Style.RESET_ALL}")
    
    if lat and lng:
        print(f"\n{Fore.YELLOW}🗺️ Coordinates (approx):{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Latitude:{Style.RESET_ALL}       {Fore.GREEN}{lat}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Longitude:{Style.RESET_ALL}      {Fore.GREEN}{lng}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}══════════════════════════════════════════{Style.RESET_ALL}")

# Main Function 
def main():
    clear_screen()
    print_banner()
    
    # Config load karo
    config_loaded = load_config()
    if not config_loaded:
        print(f"{Fore.YELLOW}[!] No config.py found. Running in basic mode.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[✓] Config loaded.{Style.RESET_ALL}")
    
    # Step 1: Country
    iso_code, country_name = country_prompt()
    
    # Step 2: State (optional — user bata sakta hai ya nahi)
    user_state = state_prompt(iso_code)
    
    # Step 3: Phone number
    parsed = phone_prompt(iso_code)
    if not parsed:
        print(f"{Fore.RED}[✗] Could not parse number. Exiting.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Step 4: Info extract karo
    info = get_location_info(parsed)
    
    # Step 5: State detect karo location string se
    detected_state = extract_state_from_location(info["location"], iso_code)
    
    # Step 6: Match check
    state_match = check_state_match(detected_state, user_state, iso_code)
    
    # Step 7: Geocode (agar API key ho)
    lat = lng = None
    search_location = detected_state if detected_state else info["location"]
    if config_loaded and OPENCAGE_API_KEY and search_location:
        print(f"{Fore.CYAN}[*] Geocoding location...{Style.RESET_ALL}")
        lat, lng, _ = geocode_with_opencage(search_location)
    
    # Step 8: Display
    display_results(info, detected_state, user_state, state_match, lat, lng)
    
    # Step 9: Map
    if lat and lng:
        generate_map(lat, lng, f"{search_location}, {country_name}", info)
    
    print(f"\n{Fore.CYAN}[✓] Done!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted. Exiting.{Style.RESET_ALL}")
        sys.exit(0)
# BY SAKSHAM GUPTA
# INSTA ID - _vibecoder
#DISCORD ID - _obito_gupta_
