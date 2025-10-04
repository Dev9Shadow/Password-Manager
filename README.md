# 🔐 Password Manager

A **secure and modern password manager** built with **Python** and **CustomTkinter**.
It provides an elegant graphical interface to store, manage, and encrypt your passwords safely — all stored locally with strong encryption.

---

## ✨ Features

- **🔒 Secure Encryption:** All passwords are encrypted before being stored.
- **🔑 Master Password:** Protected by a securely hashed master password.
- **➕ Account Management:** Add, edit, and delete accounts easily.
- **🎲 Password Generator:** Generate strong, random passwords automatically.
- **📋 Clipboard Support:** Quickly copy credentials to the clipboard.
- **🎨 Modern Interface:** Built with a sleek and responsive UI using CustomTkinter.
- **💾 Local Database:** Uses SQLite for secure, local storage.

---

## 🚀 Installation

### **Requirements**

- Python **3.7+**
- `pip` (Python package manager)

### **Install dependencies**

```bash
pip install -r requirements.txt
```

### **Main dependencies**

* `customtkinter` → Modern GUI framework
* `pillow` → Image handling
* `cryptography` → Data encryption
* `pyperclip` → Clipboard operations

## 📁 Project Structure

<pre class="overflow-visible!" data-start="1319" data-end="2135"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>password_manager/
│
├── main.py                     </span><span># Main entry point</span><span>
├── requirements.txt            </span><span># Dependencies</span><span>
├── config/
│   └── settings.py             </span><span># Global configuration</span><span>
├── core/
│   ├── database.py             </span><span># Database management</span><span>
│   ├── encryption.py           </span><span># Encryption functions</span><span>
│   └── password_generator.py   </span><span># Password generation</span><span>
├── gui/
│   ├── main_window.py          </span><span># Main window</span><span>
│   ├── dialogs/                </span><span># Application dialogs</span><span>
│   └── widgets/                </span><span># Custom widgets</span><span>
├── utils/
│   ├── geometry.py             </span><span># Geometry utilities</span><span>
│   ├── clipboard.py            </span><span># Clipboard manager</span><span>
│   └── validators.py           </span><span># Validation functions</span><span>
├── assets/
│   └── images/                 </span><span># Icons and images</span><span>
└── data/
    └── database/               </span><span># Database files</span><span>
</span></span></code></div></div></pre>

---

## 🎮 Usage

### **Start the application**

<pre class="overflow-visible!" data-start="2185" data-end="2211"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python main.py
</span></span></code></div></div></pre>

### **First Launch**

1. Set a **strong master password** on first use.
2. Use this master password to unlock your data later.

### **Main Features**

#### ➕ Add an Account

1. Click on **“Add Account”**
2. Fill in fields: Website, Username, Password
3. Use the generator for a secure password
4. Click **“Save Account”**

#### ✏️ Edit an Account

1. Select an account in the list
2. Click **“Edit Account”**
3. Modify the desired information
4. Save changes

#### ❌ Delete an Account

1. Select an account
2. Click **“Supp Account”**
3. Confirm deletion

#### 👁️ View Encrypted Data

1. Right-click on an account
2. Select **“View Data”**
3. Enter your master password to decrypt data

#### 📋 Context Menu

* **Copy Site** → Copy the website name
* **Copy Login** → Copy the username
* **Copy Password** → Copy the password
* **View Data** → Decrypt and view credentials

---

## 🔒 Security

### **Encryption**

* Uses **Fernet (AES-128 symmetric encryption)**
* Key derived via **PBKDF2 with SHA-256**
* Unique **salt** for each key derivation

### **Master Password**

* Hashed with **PBKDF2-HMAC-SHA256**
* **100,000 iterations** to resist brute-force attacks
* Random **16-byte salt**

### **Database**

* Sensitive data is encrypted before storage
* Stored locally in **SQLite** (no network transmission)

---

## 🛠️ Technical Architecture

### **MVC Pattern**

* **Model:** `core/database.py`, `core/encryption.py`
* **View:** `gui/` (windows & widgets)
* **Controller:** `gui/main_window.py`

### **Design Patterns**

* **Factory Pattern** → For dialog creation
* **Observer Pattern** → For event callbacks
* **Strategy Pattern** → For validation strategies

### **Best Practices**

* Separation of concerns
* Modular and reusable code
* Robust error handling
* Centralized configuration
* Integrated logging system

---

## 🔧 Configuration

All configuration parameters are located in `config/settings.py`:

* **Colors:** Theme customization
* **Dimensions:** Window size and layout
* **Messages:** UI text
* **Validation:** Input validation rules
* **Generator:** Password generator settings

---

## 🧪 Development

### **Add New Features**

* **New dialog:** `gui/dialogs/`
* **New widget:** `gui/widgets/`
* **New business logic:** `core/`
* **New utilities:** `utils/`

### **Tests**

To add your own tests:

<pre class="overflow-visible!" data-start="4600" data-end="4645"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>mkdir</span><span> tests
</span><span># Add your test files</span><span>
</span></span></code></div></div></pre>

---

## 🤝 Contribution

1. **Fork** the repository
2. **Create** a new branch for your feature
3. **Commit** your changes
4. **Push** the branch
5. **Open** a Pull Request

---

## 🐛 Known Issues

* Icons may not display if the `assets/images/` directory is missing
* Compatible with **Python 3.7+** only
* Optimized for screens **1920×1080 and higher**

---

## 💡 Future Improvements

* Implement **data visualization** in the right-click menu (view decrypted password)
* Add a **“Forgot Master Password”** recovery feature
* Enhance password strength indicator
* Support cloud synchronization
