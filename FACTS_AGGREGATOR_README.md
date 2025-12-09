# Storage Facts Aggregator

This solution provides two methods to gather all storage system facts from a Hitachi VSP storage array and combine them into a single JSON file.

## Overview

The solution collects facts from 31 different storage components including:
- Audit logs
- CLPRs
- Disk drives
- External volumes and parity groups
- Host groups
- iSCSI targets and connections
- Journals and journal volumes
- Logical devices (LDEVs)
- Microprocessors (MPs)
- Parity and resource groups
- Quorum disks
- Remote connections
- Server priority managers
- Shadow image groups and pairs
- Snapshots and snapshot groups
- SNMP settings
- Storage ports and pools
- Storage system info
- Users and user groups

## Method 1: Ansible Role (Recommended)

### Structure

```
roles/
└── gather_storage_facts/
    └── tasks/
        └── main.yml          # Main role tasks
```

### Usage

```bash
# Run the playbook
ansible-playbook gather_all_facts.yml

# Run with custom output file
ansible-playbook gather_all_facts.yml -e facts_output_file=/path/to/output.json

# Run with vault password
ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass

# Run with specific inventory
ansible-playbook gather_all_facts.yml -i inventory.yml
```

### Features

- **Fault Tolerant**: Uses `ignore_errors: true` so one failed module doesn't stop the entire process
- **Organized Output**: Each fact category is clearly labeled in the output JSON
- **Easy Integration**: Can be included in larger playbooks or modified as needed
- **Clear Logging**: Debug messages show what's being gathered

### Output

The role creates a JSON file (default: `/tmp/all_storage_facts.json`) with structure:

```json
{
  "audit_log_transfer_destinations": {...},
  "clpr": {...},
  "disk_drives": {...},
  "external_parity_groups": {...},
  ...
}
```

## Method 2: Python Script

### Usage

```bash
# Make script executable
chmod +x gather_all_facts.py

# Run with default settings
python3 gather_all_facts.py

# Specify output file
python3 gather_all_facts.py --output-file storage_facts.json

# Use vault password file
python3 gather_all_facts.py --vault-password-file ~/.vault_pass

# Use custom variables file
python3 gather_all_facts.py --vars-file /path/to/vars.yml

# Use the Ansible role instead of generating a playbook
python3 gather_all_facts.py --use-role
```

### Features

- **Dynamic Playbook Generation**: Creates playbook on the fly
- **Flexible**: Supports multiple configuration options
- **Automated**: Handles temporary file creation and cleanup
- **Error Handling**: Clear error messages and return codes

### Requirements

```
ansible>=2.10
hitachivantara.vspone_block collection
python>=3.6
```

## Configuration

### Vault Variables File

Ensure your `ansible_vault_vars/ansible_vault_storage_var.yml` contains:

```yaml
---
storage_address: "192.168.1.100"
vault_storage_username: "admin"
vault_storage_secret: "password"
```

Encrypt with vault:

```bash
ansible-vault encrypt ansible_vault_vars/ansible_vault_storage_var.yml
```

### Output Configuration (Ansible Role Only)

In `gather_all_facts.yml`, customize:

```yaml
vars:
  facts_output_dir: "{{ playbook_dir }}/output"
  facts_output_file: "{{ facts_output_dir }}/all_storage_facts.json"
```

## Output JSON Format

```json
{
  "audit_log_transfer_destinations": {
    "data": [...]
  },
  "clpr": {
    "data": [...]
  },
  "disk_drives": {
    "data": [...]
  },
  "external_parity_groups": {
    "data": [...]
  },
  "external_path_groups": {
    "data": [...]
  },
  "external_volumes": {
    "data": [...]
  },
  "host_groups": {
    "data": [...]
  },
  "iscsi_remote_connections": {
    "data": [...]
  },
  "iscsi_targets": {
    "data": [...]
  },
  "journals": {
    "data": [...]
  },
  "journal_volumes": {
    "data": [...]
  },
  "ldevs": {
    "data": [...]
  },
  "microprocessors": {
    "data": [...]
  },
  "parity_groups": {
    "data": [...]
  },
  "quorum_disks": {
    "data": [...]
  },
  "remote_connections": {
    "data": [...]
  },
  "resource_groups": {
    "data": [...]
  },
  "server_priority_managers": {
    "data": [...]
  },
  "shadow_image_groups": {
    "data": [...]
  },
  "shadow_image_pairs": {
    "data": [...]
  },
  "snapshots": {
    "data": [...]
  },
  "snapshot_groups": {
    "data": [...]
  },
  "snmp_settings": {
    "data": [...]
  },
  "storage_ports": {
    "data": [...]
  },
  "hardware_installed": {
    "data": [...]
  },
  "channel_boards": {
    "data": [...]
  },
  "storage_pools": {
    "data": [...]
  },
  "storage_system": {
    "data": [...]
  },
  "users": {
    "data": [...]
  },
  "user_groups": {
    "data": [...]
  }
}
```

## Troubleshooting

### Vault Password Issues

```bash
# If using vault password file
ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass

# Or prompt for password
ansible-playbook gather_all_facts.yml --ask-vault-pass
```

### Module Not Found

Ensure the collection is installed:

```bash
ansible-galaxy collection install hitachivantara.vspone_block
```

### Connection Issues

Verify storage system credentials:

```bash
ansible localhost -m hitachivantara.vspone_block.vsp.hv_storagesystem_facts \
  -e 'connection_info={address: 192.168.1.100, username: admin, password: pass}'
```

### Python Script Issues

Check Python version:

```bash
python3 --version  # Should be 3.6+
```

Check Ansible installation:

```bash
ansible --version
```

## Advanced Usage

### Filter Output

Process the JSON output:

```python
import json

with open('all_storage_facts.json') as f:
    facts = json.load(f)
    
# Get only LDEV information
ldevs = facts.get('ldevs', {})
print(json.dumps(ldevs, indent=2))
```

### Integrate into Larger Playbook

```yaml
- name: Large Playbook
  hosts: localhost
  gather_facts: false
  
  roles:
    - gather_storage_facts  # Collects all facts
    - process_facts         # Process the collected facts
    - report_facts          # Generate reports
```

### Customize Collection

Edit `roles/gather_storage_facts/tasks/main.yml` to:
- Remove specific fact modules you don't need
- Add additional modules
- Modify output field names
- Add conditional gathering based on variables

## Performance

- **Time**: Depends on storage system and network latency (typically 30-120 seconds)
- **Memory**: Minimal for aggregation (< 100MB)
- **Disk**: Output JSON typically 1-10MB depending on storage configuration

## Best Practices

1. **Use vault for credentials**: Never store passwords in plain text
2. **Test first**: Run on non-production system first
3. **Version control**: Keep playbooks in git
4. **Schedule regularly**: Use cron or similar to collect facts periodically
5. **Backup results**: Store JSON output in version control or backup system

## License

These playbooks and scripts are provided as examples. Adapt them to your environment and requirements.
