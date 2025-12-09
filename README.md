
# Storage Facts Aggregator Solution

Combine 31 Ansible playbooks into a single JSON file with all facts.

## 📚 Documentation

1. [FILE_INDEX.md](FILE_INDEX.md) - Start here for navigation
2. [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) - Overview and quick start
3. [FACTS_AGGREGATOR_README.md](FACTS_AGGREGATOR_README.md) - Detailed documentation
4. [JSON_SCHEMA.json](JSON_SCHEMA.json) - Output format specification


## 🚀 Quick Start (Choose One Method)

### Method 1: Ansible Role (Recommended)
```bash
ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass
# Output: all_storage_facts.json
```

### Method 2: Python Script
```bash
python3 gather_all_facts.py
# Output: all_storage_facts.json
```

### Method 3: Bash Helper
```bash
bash quick_start.sh run-quick
# Output: output/all_storage_facts.json
```


## ⚙️ Setup (One Time)

1. **Copy example configuration:**
   ```bash
   cp ansible_vault_vars/example_ansible_vault_storage_var.yml \
     ansible_vault_vars/ansible_vault_storage_var.yml
   ```

2. **Edit with your storage credentials:**
   ```bash
   nano ansible_vault_vars/ansible_vault_storage_var.yml
   ```

3. **Encrypt the file:**
   ```bash
   ansible-vault encrypt ansible_vault_vars/ansible_vault_storage_var.yml
   ```

4. **Create vault password file (optional):**
   ```bash
   echo "your_password" > ~/.vault_pass
   chmod 600 ~/.vault_pass
   ```

5. **Verify setup:**
   ```bash
   bash quick_start.sh check-vault
   ```


## 📊 What Gets Collected

The solution gathers facts from 31 storage components:

| Component | Component |
|-----------|-----------|
| ✓ Audit Log Transfer Destinations | ✓ Snapshots |
| ✓ CLPRs | ✓ Snapshot Groups |
| ✓ Disk Drives | ✓ SNMP Settings |
| ✓ External Parity Groups | ✓ Storage Ports |
| ✓ External Path Groups | ✓ Hardware Installed |
| ✓ External Volumes | ✓ Channel Boards |
| ✓ Host Groups | ✓ Storage Pools |
| ✓ iSCSI Remote Connections | ✓ Storage System |
| ✓ iSCSI Targets | ✓ Users |
| ✓ Journals | ✓ User Groups |
| ✓ Journal Volumes | ✓ Microprocessors |
| ✓ LDEVs (Logical Devices) | ✓ Parity Groups |
| ✓ Quorum Disks | ✓ Remote Connections |
| ✓ Resource Groups | ✓ Server Priority Managers |
| ✓ Shadow Image Groups | ✓ Shadow Image Pairs |


## 🛠️ Utility Scripts

Process and analyze the JSON output:

```bash
python3 process_facts.py -f all_storage_facts.json summary
python3 process_facts.py -f all_storage_facts.json list
python3 process_facts.py -f all_storage_facts.json extract ldevs -o ldevs.json
python3 process_facts.py -f all_storage_facts.json count ldevs
python3 process_facts.py -f all_storage_facts.json filter ldevs status "Defined" -o active.json
python3 process_facts.py -f all_storage_facts.json export ldevs -o ldevs.csv
python3 process_facts.py -f all_storage_facts.json diff -c all_storage_facts_old.json
```


## 📁 Files Created

### Core Solutions
- `gather_all_facts.yml` - Ansible playbook
- `gather_all_facts.py` - Python script
- `quick_start.sh` - Bash helper
- `roles/gather_storage_facts/tasks/main.yml` - 452-line Ansible role

### Utilities
- `process_facts.py` - JSON analyzer

### Documentation
- `FILE_INDEX.md` - Navigation guide (START HERE)
- `SOLUTION_SUMMARY.md` - Overview
- `FACTS_AGGREGATOR_README.md` - Detailed documentation
- `JSON_SCHEMA.json` - Output schema
- `README.md` - This file

### Configuration
- `ansible_vault_vars/example_ansible_vault_storage_var.yml` - Example vault file


## 🔄 Common Workflows

### 1. Gather facts and view summary
```bash
ansible-playbook gather_all_facts.yml --ask-vault-pass
python3 process_facts.py -f output/all_storage_facts.json summary
```

### 2. Extract specific data
```bash
python3 process_facts.py -f all_storage_facts.json extract ldevs -o ldevs.json
```

### 3. Compare storage snapshots
```bash
python3 process_facts.py -f current.json diff -c previous.json
```

### 4. Export to CSV for analysis
```bash
python3 process_facts.py -f all_storage_facts.json export storage_pools -o pools.csv
```


## 🔐 Security

- ✓ Uses Ansible Vault for credential encryption
- ✓ Supports vault password files
- ✓ Never stores passwords in plain text
- ✓ Example configuration provided
- ✓ Guide included in [FACTS_AGGREGATOR_README.md](FACTS_AGGREGATOR_README.md)


## 📋 Requirements

- ✓ Ansible >= 2.10
- ✓ Python >= 3.6
- ✓ hitachivantara.vspone_block collection
- ✓ Storage system with REST API access
- ✓ Valid credentials for storage system


## ⚡ Features

- ✓ Combines 31 facts playbooks into one
- ✓ Single JSON output file
- ✓ Fault tolerant (continues if modules fail)
- ✓ Well organized with clear categories
- ✓ Two execution methods (Ansible + Python)
- ✓ Comprehensive documentation
- ✓ Built-in JSON analysis tools
- ✓ Examples and guides included


## 🤔 Troubleshooting

### Missing collection?
```bash
ansible-galaxy collection install hitachivantara.vspone_block
```

### Vault password issues?
Check: [FACTS_AGGREGATOR_README.md](FACTS_AGGREGATOR_README.md) → Troubleshooting section

### Connection timeout?
Verify: Storage IP, credentials, and network connectivity

**See [FACTS_AGGREGATOR_README.md](FACTS_AGGREGATOR_README.md) for more troubleshooting tips.**


## 📞 Next Steps

1. Read [FILE_INDEX.md](FILE_INDEX.md) for file navigation
2. Read [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) for overview
3. Follow setup instructions above
4. Run one of the quick start commands
5. Use `process_facts.py` to explore output
6. Integrate into your workflows

---

**For detailed help, see:**
- [FACTS_AGGREGATOR_README.md](FACTS_AGGREGATOR_README.md)
- [FILE_INDEX.md](FILE_INDEX.md)
- [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)
