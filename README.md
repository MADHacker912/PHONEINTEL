```markdown
# 📞 PhoneNum Locator

A powerful **Phone Number Intelligence Toolkit** written in **Python**.

It helps analyze publicly available metadata associated with phone numbers, such as region, carrier, timezone, and validation status. It also supports generating an interactive map when an OpenCage API key is provided.

> ⚠️ **Educational & Authorized Use Only**
>
> This project is intended for educational purposes, cybersecurity learning, and authorized security testing. Always obtain proper authorization before analyzing phone numbers that do not belong to you.

---

# ✨ Features

- 🌍 Country-first workflow
- 📍 Region detection
- 📡 Carrier detection
- 🕐 Timezone identification
- 📄 Number type detection
- ✅ Number validation
- 🗺️ Interactive HTML map generation (Optional)
- 📱 Fully compatible with Termux
- 🎨 Beautiful colored terminal output

---

# 📸 Preview

```

╔══════════════════════════════════════════╗
║       📞 PhoneNum Locator v1.0           ║
║   Phone Number Intelligence Toolkit     ║
╚══════════════════════════════════════════╝

[?] Enter Country:
└─> India

[✓] Country detected: India (ISO: IN)

[?] Enter Phone Number:
└─> 9876543210

═══════════════════════════════════════
PHONE NUMBER INTELLIGENCE REPORT
═══════════════════════════════════════

International : +91 98765 43210
Carrier       : Airtel
Region        : Maharashtra
Timezone      : Asia/Kolkata
Type          : Mobile
Valid         : Yes
Possible      : Yes

````

---

# 🚀 Installation

## Linux / macOS

```bash
git clone https://github.com/yourusername/PhoneNum-Locator.git

cd PHONEINTEL

 sudo apt install -r requirements.txt
````

---

## Termux

```bash
pkg update && pkg upgrade -y

pkg install python git -y

git clone https://github.com/yourusername/PhoneNum-Locator.git

cd PHONEINTEL

pip install -r requirements.txt
```

---

# 🎮 Usage

Simply run

```bash
python3 phoneintel.py
```

---

# 🗺️ Enable Map Generation (Optional)

Get a free API key from **OpenCage Geocoding**.

Open the configuration file:

```bash
cd config.py
```

Edit it:

```python
OPENCAGE_API_KEY = "YOUR_API_KEY"
```

Run the program again.

An interactive HTML map will be generated automatically.

---

# 📂 Output

```
location_919876543210.html
```

Open the generated HTML file in any web browser.

---

# ⚙️ Technologies Used

| Module       | Purpose                |
| ------------ | ---------------------- |
| phonenumbers | Parsing & Validation   |
| geocoder     | Region Detection       |
| carrier      | Carrier Detection      |
| timezone     | Timezone Detection     |
| OpenCage API | Coordinates (Optional) |
| Folium       | Interactive Maps       |

---

# 📱 Termux Tips

* Run `termux-setup-storage` once after installation.
* Install OpenSSL if SSL errors occur.

```bash
pkg install openssl
```

* Generated maps can be opened using Chrome or Firefox.

---

# 🛠 Troubleshooting

| Problem             | Solution                                                                               |
| ------------------- | -------------------------------------------------------------------------------------- |
| ModuleNotFoundError | `pip install -r requirements.txt`                                                      |
| Map not generated   | Add a valid OpenCage API key                                                           |
| Permission denied   | `chmod +x phonenum_locator.py`                                                         |
| Wrong location      | Phone metadata provides approximate regional information, not precise device locations |

---

# 📋 Project Structure

```
PhoneNum-Locator/
│
├── phonenum_locator.py
├── config.py.example
├── requirements.txt
├── README.md
└── output/
```

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# ⚠️ Legal Disclaimer

This software is intended **only for educational purposes and authorized security testing**.

The tool analyzes publicly available metadata associated with phone numbers. It **does not** provide real-time device tracking or access to private information.

Users are solely responsible for complying with all applicable laws and regulations. The developer assumes no responsibility for misuse of this software.

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the project

🐞 Report bugs

💡 Suggest new features

---

<p align="center">
Made with ❤️ in Python
</p>

# STAY ETHICAL, STAY SAFE
```
