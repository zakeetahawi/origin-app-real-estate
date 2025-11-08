# 🗄️ Database Information
## Origin App - SQLite Database

---

## ⚠️ **Important Notice**

This SQLite database file (`db.sqlite3`) is included in the repository for **DEVELOPMENT AND DEMONSTRATION PURPOSES ONLY**.

---

## 📋 **Database Details**

### **File**: `db.sqlite3`
- **Type**: SQLite 3
- **Purpose**: Development & Testing
- **Size**: Variable (grows with data)
- **Encoding**: UTF-8

---

## 🔒 **Security Considerations**

### **⚠️ WARNING**:
```
This database may contain:
- Sample user accounts
- Test data
- Development credentials
- Demo properties and contracts

🚨 DO NOT USE IN PRODUCTION WITHOUT:
1. Changing all passwords
2. Removing test data
3. Reviewing all user accounts
4. Migrating to PostgreSQL/MySQL
```

---

## 🎯 **Recommended Usage**

### **For Development**:
```bash
# Use the included database as-is
python manage.py runserver

# Access with default credentials (if any)
# Check QUICK_START_GUIDE.md for details
```

### **For Production**:
```bash
# DO NOT use SQLite in production!
# Configure PostgreSQL or MySQL instead

# Example PostgreSQL setup:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'originapp_prod',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Migrate data:
python manage.py dumpdata > data.json
# Configure new database
python manage.py migrate
python manage.py loaddata data.json
```

---

## 📊 **Database Schema**

### **Applications**:
- **Core**: Users, Roles, Permissions, Notifications
- **Properties**: Properties, Types, Features, Images
- **Owners**: Property Owners
- **Clients**: Tenants/Buyers
- **Contracts**: Rental Contracts, Payments
- **Sales**: Sales Contracts, Reservations, Payments
- **Maintenance**: Maintenance Requests
- **Financial**: Accounts, Invoices, Payments, Budgets

### **Total Tables**: 36+
### **Total Models**: 36+

---

## 🔄 **Migration Commands**

### **Reset Database** (Development Only):
```bash
# Backup first!
cp db.sqlite3 db.sqlite3.backup

# Delete and recreate
rm db.sqlite3
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### **Backup Database**:
```bash
# Simple copy
cp db.sqlite3 backups/db_$(date +%Y%m%d_%H%M%S).sqlite3

# Export data
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### **Restore from Backup**:
```bash
# From SQLite file
cp backups/db_20251108.sqlite3 db.sqlite3

# From JSON dump
python manage.py loaddata backup_20251108.json
```

---

## 🚀 **Production Setup**

### **Why NOT SQLite in Production?**
```
❌ Limited concurrency
❌ No network access
❌ Limited scaling
❌ Single file = single point of failure
❌ No replication
❌ Limited backup options
```

### **Recommended: PostgreSQL**
```
✅ Better concurrency
✅ Network access
✅ Horizontal scaling
✅ Advanced features
✅ Replication support
✅ Better backup tools
✅ Production-ready
```

---

## 📝 **Initial Data**

### **Sample Accounts** (if any):
```
⚠️ Change these immediately in production!

Admin User:
Username: admin
Password: [Check setup docs]

Demo Users:
- Manager, Staff, Client accounts
- All with demo passwords
```

### **Sample Data**:
```
The database may include:
- Demo properties
- Sample contracts
- Test maintenance requests
- Example financial records
- Demo notifications

🗑️ Clean before production use!
```

---

## 🛠️ **Database Maintenance**

### **Optimize Database**:
```bash
# SQLite optimization
python manage.py dbshell
> VACUUM;
> ANALYZE;
> .exit
```

### **Check Integrity**:
```bash
python manage.py dbshell
> PRAGMA integrity_check;
> .exit
```

### **View Statistics**:
```bash
python manage.py dbshell
> .tables
> .schema [table_name]
> .exit
```

---

## 📊 **Data Migration to Production**

### **Step-by-Step**:

#### **1. Export from SQLite**:
```bash
# Export all data
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude contenttypes \
    --exclude auth.permission \
    --indent 2 \
    > production_data.json
```

#### **2. Setup PostgreSQL**:
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
> CREATE DATABASE originapp_prod;
> CREATE USER originapp WITH PASSWORD 'secure_password';
> GRANT ALL PRIVILEGES ON DATABASE originapp_prod TO originapp;
> \q
```

#### **3. Configure Django**:
```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'originapp_prod',
        'USER': 'originapp',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### **4. Migrate & Load**:
```bash
# Run migrations
python manage.py migrate

# Load data
python manage.py loaddata production_data.json

# Verify
python manage.py check
```

---

## 🔐 **Security Checklist**

### **Before Production**:
- [ ] Change all default passwords
- [ ] Remove demo/test accounts
- [ ] Clear sample data
- [ ] Review user permissions
- [ ] Enable SSL/TLS
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Migrate to PostgreSQL
- [ ] Configure firewall
- [ ] Enable audit logging

---

## 📚 **Useful Commands**

### **Database Info**:
```bash
# Check database size
ls -lh db.sqlite3

# Count records
python manage.py shell
>>> from django.apps import apps
>>> for model in apps.get_models():
...     print(f"{model.__name__}: {model.objects.count()}")
```

### **Quick Queries**:
```bash
python manage.py dbshell
> SELECT COUNT(*) FROM auth_user;
> SELECT COUNT(*) FROM properties_property;
> SELECT COUNT(*) FROM contracts_contract;
> .exit
```

---

## ⚡ **Performance Tips**

### **SQLite Optimization**:
```python
# In settings.py for better SQLite performance
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
            'journal_mode': 'WAL',
            'synchronous': 'NORMAL',
        }
    }
}
```

---

## 🆘 **Troubleshooting**

### **Database Locked**:
```bash
# Kill all connections
fuser -k db.sqlite3

# Or restart server
pkill -f runserver
python manage.py runserver
```

### **Corruption**:
```bash
# Check integrity
sqlite3 db.sqlite3 "PRAGMA integrity_check;"

# Recover
sqlite3 db.sqlite3 ".dump" | sqlite3 db_recovered.sqlite3
mv db_recovered.sqlite3 db.sqlite3
```

---

## 📞 **Support**

For database-related issues:
1. Check Django documentation
2. Review SQLite documentation
3. See PostgreSQL migration guide
4. Contact system administrator

---

## ⚠️ **Final Warning**

```
🚨 NEVER commit sensitive data to Git!
🚨 NEVER use SQLite in production!
🚨 ALWAYS backup before changes!
🚨 ALWAYS use strong passwords!
🚨 ALWAYS review security settings!
```

---

**Database Status**: Development/Demo  
**Last Updated**: November 8, 2025  
**Version**: SQLite 3  
**Purpose**: Development & Testing Only  

---

*For production deployment, migrate to PostgreSQL or MySQL!*
