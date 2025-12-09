# Storage Facts Aggregator - File Index

## 📋 Start Here

- **`SOLUTION_SUMMARY.md`** - Overview of the entire solution and how to use it
- **`FACTS_AGGREGATOR_README.md`** - Detailed documentation and troubleshooting

## 🚀 Quick Start Options

Choose one method to gather facts:

### Method 1: Ansible Role (Recommended)
- **File**: `gather_all_facts.yml`
- **Usage**: `ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass`
- **Implementation**: `roles/gather_storage_facts/tasks/main.yml` (452 lines)

### Method 2: Python Script
- **File**: `gather_all_facts.py` (executable)
- **Usage**: `python3 gather_all_facts.py --output-file storage_facts.json`
- **Features**: Dynamic playbook generation, flexible configuration

### Method 3: Bash Helper
- **File**: `quick_start.sh` (executable)
- **Usage**: `bash quick_start.sh run-quick`
- **Features**: Setup, validation, and easy commands

## 🛠️ Utility Scripts

### Process & Analyze Output
- **File**: `process_facts.py`
- **Functions**:
  - `summary` - Display statistics
  - `list` - List all categories
  - `extract` - Extract specific category
  - `count` - Count items
  - `filter` - Filter by key-value
  - `export` - Export as CSV
  - `diff` - Compare two files
  - `validate` - Validate JSON structure

**Example**: `python3 process_facts.py -f all_storage_facts.json summary`

## 📁 File Structure

```
ansible-facts-dump/
├── Original Playbooks (31 files)
│   ├── audit_log_transfer_dest_facts.yml
│   ├── clpr_facts.yml
│   ├── disk_drive_facts.yml
│   ├── ... (28 more files)
│   └── user_group_facts.yml
│
├── Solution Files (NEW)
│   ├── gather_all_facts.yml                    # Main playbook
│   ├── gather_all_facts.py                     # Python solution
│   ├── quick_start.sh                          # Bash helper
│   ├── process_facts.py                        # JSON processor
│   │
│   ├── Documentation
│   │   ├── SOLUTION_SUMMARY.md                 # Overview
│   │   ├── FACTS_AGGREGATOR_README.md          # Detailed guide
│   │   ├── JSON_SCHEMA.json                    # Output schema
│   │   └── FILE_INDEX.md                       # This file
│   │
│   ├── Ansible Role
│   │   └── roles/
│   │       └── gather_storage_facts/
│   │           └── tasks/
│   │               └── main.yml                # 452 lines of tasks
│   │
│   └── Configuration
│       └── ansible_vault_vars/
│           └── example_ansible_vault_storage_var.yml
│
└── Output (Generated)
    └── all_storage_facts.json                  # Combined facts (created at runtime)
```

## 📊 Facts Collected

The solution collects and combines facts from these 31 storage components:

| Component | Ansible Module |
|-----------|----------------|
| Audit Log Transfer Destinations | `hv_audit_log_transfer_dest_facts` |
| CLPRs | `hv_clpr_facts` |
| Disk Drives | `hv_disk_drive_facts` |
| External Parity Groups | `hv_external_paritygroup_facts` |
| External Path Groups | `hv_external_path_group_facts` |
| External Volumes | `hv_external_volume_facts` |
| Host Groups | `hv_hg_facts` |
| iSCSI Remote Connections | `hv_iscsi_remote_connection_facts` |
| iSCSI Targets | `hv_iscsi_target_facts` |
| Journals | `hv_journal_facts` |
| Journal Volumes | `hv_journal_volume_facts` |
| LDEVs | `hv_ldev_facts` |
| Microprocessors | `hv_mp_facts` |
| Parity Groups | `hv_paritygroup_facts` |
| Quorum Disks | `hv_quorum_disk_facts` |
| Remote Connections | `hv_remote_connection_facts` |
| Resource Groups | `hv_resource_group_facts` |
| Server Priority Managers | `hv_server_priority_manager_facts` |
| Shadow Image Groups | `hv_shadow_image_group_facts` |
| Shadow Image Pairs | `hv_shadow_image_pair_facts` |
| Snapshots | `hv_snapshot_facts` |
| Snapshot Groups | `hv_snapshot_group_facts` |
| SNMP Settings | `hv_snmp_settings_facts` |
| Storage Ports | `hv_storage_port_facts` |
| Hardware Installed | `hv_storage_system_monitor_facts` |
| Channel Boards | `hv_storage_system_monitor_facts` |
| Storage Pools | `hv_storagepool_facts` |
| Storage System | `hv_storagesystem_facts` |
| Users | `hv_user_facts` |
| User Groups | `hv_user_group_facts` |

## 🔐 Configuration & Setup

1. **Set up vault variables**:
   ```bash
   cp ansible_vault_vars/example_ansible_vault_storage_var.yml \
      ansible_vault_vars/ansible_vault_storage_var.yml
   # Edit with your storage credentials
   ansible-vault encrypt ansible_vault_vars/ansible_vault_storage_var.yml
   ```

2. **Install dependencies**:
   ```bash
   ansible-galaxy collection install hitachivantara.vspone_block
   ```

3. **Create vault password file** (optional):
   ```bash
   echo "your_password" > ~/.vault_pass
   chmod 600 ~/.vault_pass
   ```

## 🚦 Common Commands

### Gather Facts
```bash
# Using Ansible playbook
ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass

# Using Python script
python3 gather_all_facts.py

# Using bash helper
bash quick_start.sh run-quick
```

### Analyze Results
```bash
# View summary
python3 process_facts.py -f all_storage_facts.json summary

# Extract category
python3 process_facts.py -f all_storage_facts.json extract ldevs -o ldevs.json

# Filter results
python3 process_facts.py -f all_storage_facts.json filter ldevs status "Defined" -o active.json

# Compare files
python3 process_facts.py -f current.json diff -c previous.json
```

## 📋 Output JSON Structure

```json
{
  "audit_log_transfer_destinations": {...},
  "clpr": {...},
  "disk_drives": {...},
  "external_parity_groups": {...},
  "external_path_groups": {...},
  "external_volumes": {...},
  "host_groups": {...},
  "iscsi_remote_connections": {...},
  "iscsi_targets": {...},
  "journals": {...},
  "journal_volumes": {...},
  "ldevs": {...},
  "microprocessors": {...},
  "parity_groups": {...},
  "quorum_disks": {...},
  "remote_connections": {...},
  "resource_groups": {...},
  "server_priority_managers": {...},
  "shadow_image_groups": {...},
  "shadow_image_pairs": {...},
  "snapshots": {...},
  "snapshot_groups": {...},
  "snmp_settings": {...},
  "storage_ports": {...},
  "hardware_installed": {...},
  "channel_boards": {...},
  "storage_pools": {...},
  "storage_system": {...},
  "users": {...},
  "user_groups": {...}
}
```

Each category contains the structured data returned by its respective Ansible module.

## 🔍 File Descriptions

### Core Implementation

| File | Lines | Purpose |
|------|-------|---------|
| `gather_all_facts.yml` | 23 | Main playbook that orchestrates the role |
| `roles/gather_storage_facts/tasks/main.yml` | 452 | Ansible role containing all fact-gathering tasks |
| `gather_all_facts.py` | 358 | Python script for dynamic fact gathering |

### Utilities

| File | Lines | Purpose |
|------|-------|---------|
| `quick_start.sh` | 250 | Bash helper for setup and common operations |
| `process_facts.py` | 398 | Utility to analyze and process JSON output |

### Documentation

| File | Purpose |
|------|---------|
| `SOLUTION_SUMMARY.md` | Quick overview and examples |
| `FACTS_AGGREGATOR_README.md` | Comprehensive documentation |
| `JSON_SCHEMA.json` | JSON structure and schema definition |
| `FILE_INDEX.md` | This file - navigation guide |

### Configuration

| File | Purpose |
|------|---------|
| `ansible_vault_vars/example_ansible_vault_storage_var.yml` | Example vault variables template |

## 🎯 Next Steps

1. **Read**: Start with `SOLUTION_SUMMARY.md` for an overview
2. **Configure**: Set up vault variables following instructions
3. **Test**: Run `bash quick_start.sh setup` to verify dependencies
4. **Execute**: Choose and run one of the fact-gathering methods
5. **Analyze**: Use `process_facts.py` to explore the output
6. **Integrate**: Incorporate into your automation workflows

## 📞 Support Resources

- **Ansible Documentation**: https://docs.ansible.com
- **Hitachi VSPOne Collection**: https://galaxy.ansible.com/ui/repo/published/hitachivantara/vspone_block/
- **VSP Storage Documentation**: Contact Hitachi support

## ✨ Key Features Summary

✅ **31 Storage Components** - Gathers facts from all major storage components  
✅ **Two Methods** - Choose between Ansible role or Python script  
✅ **Fault Tolerant** - Continues if individual modules fail  
✅ **JSON Output** - Standard JSON format for integration  
✅ **Well Documented** - Comprehensive guides and examples  
✅ **Processing Tools** - Built-in utilities to analyze output  
✅ **Secure** - Vault support for credentials  
✅ **Scriptable** - Easily integrate into automation workflows  

---

**Created**: December 9, 2025  
**Solution Type**: Ansible Role + Python Script + Bash Helper  
**Output Format**: JSON  
**Components Aggregated**: 31 storage fact modules
