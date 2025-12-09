# Storage Facts Aggregator - Complete Solution

## Overview

This solution aggregates facts from **31 different storage components** from all attached Ansible playbooks into a single JSON file. Two complementary approaches are provided.

## Files Created

### Core Solutions

1. **`gather_all_facts.yml`** - Main playbook (uses the Ansible role)
2. **`roles/gather_storage_facts/tasks/main.yml`** - Ansible role that gathers all facts
3. **`gather_all_facts.py`** - Python script to automate fact gathering

### Utilities & Documentation

4. **`quick_start.sh`** - Bash helper script for common operations
5. **`process_facts.py`** - Utility to analyze and process the JSON output
6. **`FACTS_AGGREGATOR_README.md`** - Comprehensive documentation
7. **`JSON_SCHEMA.json`** - JSON schema describing the output structure

## Quick Start

### Option 1: Using Ansible Role (Recommended)

```bash
# Run the playbook
ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass

# Or with password prompt
ansible-playbook gather_all_facts.yml --ask-vault-pass
```

### Option 2: Using Python Script

```bash
# Make executable
chmod +x gather_all_facts.py

# Run with defaults
python3 gather_all_facts.py

# Run with custom options
python3 gather_all_facts.py --output-file storage_facts.json --vault-password-file ~/.vault_pass
```

### Option 3: Using Bash Helper

```bash
# First time setup
bash quick_start.sh setup

# Run fact gathering
bash quick_start.sh run-quick

# Check all options
bash quick_start.sh help
```

## What Gets Collected

The solution gathers facts from:

| Category | Module |
|----------|--------|
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
| LDEVs (Logical Devices) | `hv_ldev_facts` |
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
| Hardware Installed | `hv_storage_system_monitor_facts` (hardware_installed) |
| Channel Boards | `hv_storage_system_monitor_facts` (channel_boards) |
| Storage Pools | `hv_storagepool_facts` |
| Storage System | `hv_storagesystem_facts` |
| Users | `hv_user_facts` |
| User Groups | `hv_user_group_facts` |

## Output Format

All facts are combined into a single JSON file with this structure:

```json
{
  "audit_log_transfer_destinations": {...},
  "clpr": {...},
  "disk_drives": {...},
  "external_parity_groups": {...},
  ...
}
```

Each category contains the data returned by its respective Ansible fact module.

## Processing the Output

### View Summary
```bash
python3 process_facts.py -f all_storage_facts.json summary
```

### List All Categories
```bash
python3 process_facts.py -f all_storage_facts.json list
```

### Extract Specific Category
```bash
python3 process_facts.py -f all_storage_facts.json extract ldevs -o ldevs.json
```

### Count Items in Category
```bash
python3 process_facts.py -f all_storage_facts.json count ldevs
```

### Filter by Key-Value
```bash
python3 process_facts.py -f all_storage_facts.json filter ldevs status "Defined" -o active_ldevs.json
```

### Export to CSV
```bash
python3 process_facts.py -f all_storage_facts.json export ldevs -o ldevs.csv
```

### Compare Two Files
```bash
python3 process_facts.py -f all_storage_facts.json diff -c all_storage_facts_old.json
```

## Configuration

### Set Up Vault Variables

1. Copy the example file:
```bash
cp ansible_vault_vars/example_ansible_vault_storage_var.yml \
   ansible_vault_vars/ansible_vault_storage_var.yml
```

2. Edit with your storage system details:
```yaml
storage_address: "192.168.1.100"
vault_storage_username: "admin"
vault_storage_secret: "password"
```

3. Encrypt with Ansible Vault:
```bash
ansible-vault encrypt ansible_vault_vars/ansible_vault_storage_var.yml
```

### Create Vault Password File (Optional)

```bash
echo "your_vault_password" > ~/.vault_pass
chmod 600 ~/.vault_pass
```

Then use it with:
```bash
ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass
```

## Requirements

- **Ansible** >= 2.10
- **Python** >= 3.6
- **hitachivantara.vspone_block** collection

Install collection:
```bash
ansible-galaxy collection install hitachivantara.vspone_block
```

## Architecture

### Method 1: Ansible Role

```
gather_all_facts.yml (playbook)
    ↓
roles/gather_storage_facts/ (role)
    ├─ tasks/main.yml
    │   ├─ Gathers 31+ fact modules
    │   ├─ Aggregates into single dict
    │   └─ Saves to JSON file
    └─ Handles errors gracefully
```

### Method 2: Python Script

```
gather_all_facts.py (Python script)
    ├─ Generates dynamic playbook
    ├─ Executes via subprocess
    └─ Returns JSON output
```

Both methods produce identical output formats.

## Key Features

✅ **Comprehensive**: Gathers all available facts in one operation  
✅ **Fault Tolerant**: Continues even if individual modules fail  
✅ **Flexible**: Choose between Ansible or Python execution  
✅ **Well Organized**: Clear category names in output  
✅ **Documented**: JSON schema and examples provided  
✅ **Scriptable**: Process output with included utilities  
✅ **Secure**: Vault support for sensitive credentials  
✅ **Fast**: Parallel fact gathering where possible  

## Troubleshooting

### "Module not found" errors
```bash
ansible-galaxy collection install hitachivantara.vspone_block --upgrade
```

### Vault password issues
```bash
# Test vault file access
ansible-vault view ansible_vault_vars/ansible_vault_storage_var.yml --ask-vault-pass
```

### Connection timeouts
- Verify storage system IP address
- Check network connectivity
- Confirm credentials are correct

### Python dependencies
```bash
pip install ansible
```

## Best Practices

1. **Regular snapshots**: Run fact gathering periodically to track changes
2. **Version control**: Store results in git
3. **Secure credentials**: Always use Ansible Vault
4. **Backup output**: Keep JSON files for comparison and auditing
5. **Monitor changes**: Use the diff functionality to track modifications

## Examples

### Schedule Daily Fact Gathering
```bash
# Add to crontab
0 2 * * * cd /path/to/ansible-facts-dump && ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass >> facts_cron.log 2>&1
```

### Generate Reports
```python
import json
import datetime

with open('all_storage_facts.json') as f:
    facts = json.load(f)

report = {
    'timestamp': datetime.datetime.now().isoformat(),
    'total_ldevs': len(facts.get('ldevs', {}).get('data', [])),
    'total_snapshots': len(facts.get('snapshots', {}).get('data', [])),
    'storage_pools': len(facts.get('storage_pools', {}).get('data', [])),
}

print(json.dumps(report, indent=2))
```

### Integrate with Larger Workflow
```yaml
- name: Complete Storage Management
  hosts: localhost
  gather_facts: false
  
  roles:
    - gather_storage_facts  # Collect facts
    - analyze_storage       # Analyze capacity
    - generate_reports      # Create reports
    - alert_on_changes      # Monitor for changes
```

## Support

For issues with:
- **Ansible**: See [Ansible Documentation](https://docs.ansible.com)
- **Hitachi Collection**: Check [Hitachi VSPOne Documentation](https://github.com/hitachivantara/vspone-block-ansible)
- **This Solution**: Review `FACTS_AGGREGATOR_README.md`

---

**Solution created**: December 9, 2025  
**Last updated**: December 9, 2025
