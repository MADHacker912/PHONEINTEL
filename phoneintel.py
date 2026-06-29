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
import json
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

#  Configuration 
CONFIG_FILE = "config.py"
OPENCAGE_API_KEY = None

def load_config():
    """Load API keys from config.py if it exists."""
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

# Banner
BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
║       {Fore.GREEN}📞 PHONEINTEL {Fore.CYAN}          ║
║   {Fore.YELLOW}PhonE NUMBER TRACKER  {Fore.CYAN}     ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}"""

def print_banner():
    print(BANNER)

# Helpers 
def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def country_prompt():
    """Ask user for country and return ISO country code."""
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

def phone_prompt(iso_code):
    """Ask user for phone number and parse it."""
    print(f"\n{Fore.YELLOW}[?] Enter the phone number (without country code; e.g., 9876543210):{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    Or enter with '+' and full country code (e.g., +919876543210):{Style.RESET_ALL}")
    number_input = input(f"{Fore.CYAN}└─> {Style.RESET_ALL}").strip()

    # If user provided full international format
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

def get_location_info(parsed):
    """Extract location, carrier, timezone from parsed number."""
    info = {}

    # Location (region/state/city)
    location = geocoder.description_for_number(parsed, "en")
    info["location"] = location if location else "Unknown"

    # Carrier / Service Provider
    carrier_name = carrier.name_for_number(parsed, "en")
    info["carrier"] = carrier_name if carrier_name else "Unknown"

    # Timezone(s)
    tz_list = timezone.time_zones_for_number(parsed)
    info["timezones"] = ", ".join(tz_list) if tz_list else "Unknown"

    # Country code and national number
    info["country_code"] = f"+{parsed.country_code}"
    info["national_number"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    info["international_number"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    # Number type
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

    # Is possible / valid
    info["is_valid"] = phonenumbers.is_valid_number(parsed)
    info["is_possible"] = phonenumbers.is_possible_number(parsed)

    return info

def geocode_with_opencage(location_name):
    """Use OpenCage API to get lat/lng for a location."""
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

def generate_map(lat, lng, location_name, number_info):
    """Generate an interactive HTML map using Folium."""
    try:
        import folium
    except ImportError:
        print(f"{Fore.YELLOW}[!] Folium not installed. Skipping map generation.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Install with: pip install folium{Style.RESET_ALL}")
        return

    # Clean number for filename
    clean_num = number_info["international_number"].replace(" ", "_").replace("+", "")
    filename = f"location_{clean_num}.html"

    my_map = folium.Map(location=[lat, lng], zoom_start=10)

    popup_text = f"""
    <b>📍 Phone Number:</b> {number_info['international_number']}<br>
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

def display_results(info, lat=None, lng=None, geocoded_location=None):
    """Display all gathered information."""
    print(f"\n{Fore.CYAN}══════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📊 PHONE NUMBER INTELLIGENCE REPORT{Style.RESET_ALL}")
    print(f"{Fore.CYAN}══════════════════════════════════════════{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}📞 Number Information:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}International:{Style.RESET_ALL}    {Fore.GREEN}{info['international_number']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}National:{Style.RESET_ALL}         {Fore.GREEN}{info['national_number']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Country Code:{Style.RESET_ALL}     {Fore.GREEN}{info['country_code']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Valid Number:{Style.RESET_ALL}     {'✅ Yes' if info['is_valid'] else '❌ No'}")
    print(f"  {Fore.WHITE}Possible:{Style.RESET_ALL}         {'✅ Yes' if info['is_possible'] else '❌ No'}")

    print(f"\n{Fore.YELLOW}🌍 Location & Network:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Region/Area:{Style.RESET_ALL}      {Fore.GREEN}{info['location']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Carrier:{Style.RESET_ALL}          {Fore.GREEN}{info['carrier']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Number Type:{Style.RESET_ALL}      {Fore.GREEN}{info['number_type']}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Timezone(s):{Style.RESET_ALL}      {Fore.GREEN}{info['timezones']}{Style.RESET_ALL}")

    if lat and lng:
        print(f"\n{Fore.YELLOW}🗺️ Geolocation (from OpenCage):{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Latitude:{Style.RESET_ALL}       {Fore.GREEN}{lat}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Longitude:{Style.RESET_ALL}      {Fore.GREEN}{lng}{Style.RESET_ALL}")
        if geocoded_location:
            print(f"  {Fore.WHITE}Address:{Style.RESET_ALL}        {Fore.GREEN}{geocoded_location}{Style.RESET_ALL}")

    print(f"{Fore.CYAN}══════════════════════════════════════════{Style.RESET_ALL}")

# Main
def main():
    clear_screen()
    print_banner()

    # Load config
    config_loaded = load_config()
    if not config_loaded:
        print(f"{Fore.YELLOW}[!] No config.py found. Running in basic mode (no map/geocoding).{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    To enable maps, copy config.py.example to config.py and add your API key.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[✓] Config loaded. Map generation enabled.{Style.RESET_ALL}")

    # Step 1: Ask for country
    iso_code, country_name = country_prompt()

    # Step 2: Ask for phone number
    parsed = phone_prompt(iso_code)
    if not parsed:
        print(f"{Fore.RED}[✗] Could not parse number. Exiting.{Style.RESET_ALL}")
        sys.exit(1)

    # Step 3: Extract info
    info = get_location_info(parsed)

    # Step 4: Geocode if API key available
    lat = lng = geocoded_location = None
    if config_loaded and OPENCAGE_API_KEY and info["location"] != "Unknown":
        print(f"{Fore.CYAN}[*] Geocoding location via OpenCage...{Style.RESET_ALL}")
        lat, lng, geocoded_location = geocode_with_opencage(info["location"])

    # Step 5: Display results
    display_results(info, lat, lng, geocoded_location)

    # Step 6: Generate map if geocoded
    if lat and lng:
        generate_map(lat, lng, info["location"], info)
    elif config_loaded and not lat:
        print(f"{Fore.YELLOW}[!] Could not geocode location. Map not generated.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}[✓] Done!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted by user. Exiting.{Style.RESET_ALL}")
        sys.exit(0)
# BY SAKSHAM GUPTA
# INSTA ID _vibecode
#DISCORD ID _obito_gupta
