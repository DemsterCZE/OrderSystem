# ☕ Kavárna U Pole – Project Documentation

## 📋 Repository Structure
- `/config` - Django configuration files.
- `/OrderSystem` - Core application logic, business rules, and test suites.
- `/bin` - Utility scripts.
- `/static` - CSS assets
- `/images` - Visual assets for documentation.
- `/templates` - HTML templates (including dynamic QR code generation).
- `Dockerfile` & `docker-compose.yml` - Containerization setup for quick deployment.
- `db.sqlite3` - Pre-made database with baseline data.
- `requirements.txt` - Python dependency list.
- `manage.py` - Project management script (server execution, migrations, admin creation, and testing).


## 🛠 Installation & Setup
1. Clone the repository.
2. Navigate to the repository root directory in your terminal.
3. Execute the following command: 
```bash
docker-compose up --build
```
3. Access the application at: `http://localhost:8000`


❗ IMPORTANT: To test QR code functionality on mobile devices, use your computer's local network IP address (e.g., http://192.168.1.15:8000) instead of localhost. Both the PC and mobile device must be connected to the same network.

💡 PRO TIP: Use the provided automation scripts in the /bin directory. Run bin/start_container_windows.bat or bin/start_container_linux.sh to automatically build the environment, run migrations, and launch the browser.

## 👤 Admin Access
Use the following credentials to access the Django Administration panel:

* **Admin URL:** `http://localhost:8000/admin` 
* **Username:** `root`
* **Password:** `1234`

Use this panel to manage staff accounts, table configurations, and menu items.

## 👨‍🍳 Staff Access 
Staff members have access to a central dashboard to accept and process incoming orders.

* **Dashboard URL:** `http://localhost:8000/orders/` 
* **PPre-configured accounts:** `emp1`, `emp2`
* **Password for both:** `hesloheslo`
> 🔐 **Security Note:** Access to the dashboard and order management functionality is protected by an authentication layer. Unauthorized access attempts will be automatically redirected to the login page.

### Empty Dashboard preview
![Dashboard without order](images/dashboard_no_order.png)

### Non-empty dashboard preview
![Dashboard with order](images/dashboard_with_order.png)

### Display order detail
To display order detail you need to click the magnifying glass in the right corner of order card
![Magnifying glass](images/view_order_detail.png)

### Order detail preview
![Order detail](images/order_detail.png)

## 🪑 Customer access (Tables)
Guests interact with the menu and their orders through a dedicated table interface.

* **Main Hub:** `http://localhost:8000/` (List of all tables)
* **Specific Table Page:** `http://localhost:8000/table/<ID_STOLU>/`

### Order Workflow:
1. **Check-in** The guest scans a dynamically generated QR code or clicks "Open Menu." button.
2. **Selection:** The guest selects items via the UI and submits the order.

### Customer UI preview
![Table summary](images/table_detail.png)

### Order creation preview
![Order creation](images/order_creation.png)


## 🧪 Automated Testing
1. Open your terminal in the project root directory.
2. Run the tests using the following command:
```bash
    docker-compose exec web python manage.py test
```
💡 TIP: You can also use the prepared scripts for testing: bin/run_tests_windows.bat or bin/run_tests_linux.sh

## Developed by Petr Zemánek
