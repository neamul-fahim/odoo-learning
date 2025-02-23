import xmlrpc.client
import json

# Odoo server details
URL = "http://localhost:8071"  # Change to your Odoo server address
DB = "odoo_18"  # Change to your database name
USERNAME = "fahim"  # Admin username
PASSWORD = "fahim"  # Admin password

# Connect to Odoo
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

if not uid:
    print("❌ Authentication failed. Check credentials.")
    exit()

models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Load mail server config
with open("/opt/odoo/custom_addons/odoo_18/mail_server_setup/mail_servers.json", "r") as file:
    mail_servers = json.load(file)

for server in mail_servers:
    # Check if mail server already exists
    existing = models.execute_kw(DB, uid, PASSWORD, "ir.mail_server", "search",
                                 [[("smtp_host", "=", server["smtp_host"])]])

    if not existing:
        # Create new mail server entry
        mail_server_id = models.execute_kw(DB, uid, PASSWORD, "ir.mail_server", "create", [server])
        print(f"✅ Mail server '{server['name']}' created with ID: {mail_server_id}")
    else:
        print(f"✅ Mail server '{server['name']}' already exists. Skipping.")

print("🚀 All mail servers configured successfully!")
