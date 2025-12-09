#!/usr/bin/env python3
"""
Storage Facts Aggregator
Purpose: Gather all storage system facts from a VSP storage array using
         Ansible and combine them into a single JSON file.

Usage:
    python3 gather_all_facts.py [--output-file OUTPUT_FILE] [--vars-file VARS_FILE]

Requirements:
    - ansible>=2.10
    - hitachivantara.vspone_block collection installed
    - Vault variables file with storage credentials
"""

import json
import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional


class StorageFactsAggregator:
    """Aggregates storage facts from multiple Ansible fact modules."""

    # All fact modules to gather, mapped to their output keys
    FACTS_MODULES = {
        'audit_log_transfer_dest': 'hitachivantara.vspone_block.vsp.hv_audit_log_transfer_dest_facts',
        'clpr': 'hitachivantara.vspone_block.vsp.hv_clpr_facts',
        'disk_drives': 'hitachivantara.vspone_block.vsp.hv_disk_drive_facts',
        'external_parity_groups': 'hitachivantara.vspone_block.vsp.hv_external_paritygroup_facts',
        'external_path_groups': 'hitachivantara.vspone_block.vsp.hv_external_path_group_facts',
        'external_volumes': 'hitachivantara.vspone_block.vsp.hv_external_volume_facts',
        'host_groups': 'hitachivantara.vspone_block.vsp.hv_hg_facts',
        'iscsi_remote_connections': 'hitachivantara.vspone_block.vsp.hv_iscsi_remote_connection_facts',
        'iscsi_targets': 'hitachivantara.vspone_block.vsp.hv_iscsi_target_facts',
        'journals': 'hitachivantara.vspone_block.vsp.hv_journal_facts',
        'journal_volumes': 'hitachivantara.vspone_block.vsp.hv_journal_volume_facts',
        'ldevs': 'hitachivantara.vspone_block.vsp.hv_ldev_facts',
        'microprocessors': 'hitachivantara.vspone_block.vsp.hv_mp_facts',
        'parity_groups': 'hitachivantara.vspone_block.vsp.hv_paritygroup_facts',
        'quorum_disks': 'hitachivantara.vspone_block.vsp.hv_quorum_disk_facts',
        'remote_connections': 'hitachivantara.vspone_block.vsp.hv_remote_connection_facts',
        'resource_groups': 'hitachivantara.vspone_block.vsp.hv_resource_group_facts',
        'server_priority_managers': 'hitachivantara.vspone_block.vsp.hv_server_priority_manager_facts',
        'shadow_image_groups': 'hitachivantara.vspone_block.vsp.hv_shadow_image_group_facts',
        'shadow_image_pairs': 'hitachivantara.vspone_block.vsp.hv_shadow_image_pair_facts',
        'snapshots': 'hitachivantara.vspone_block.vsp.hv_snapshot_facts',
        'snapshot_groups': 'hitachivantara.vspone_block.vsp.hv_snapshot_group_facts',
        'snmp_settings': 'hitachivantara.vspone_block.vsp.hv_snmp_settings_facts',
        'storage_ports': 'hitachivantara.vspone_block.vsp.hv_storage_port_facts',
        'hardware_installed': 'hitachivantara.vspone_block.vsp.hv_storage_system_monitor_facts',
        'channel_boards': 'hitachivantara.vspone_block.vsp.hv_storage_system_monitor_facts',
        'storage_pools': 'hitachivantara.vspone_block.vsp.hv_storagepool_facts',
        'storage_system': 'hitachivantara.vspone_block.vsp.hv_storagesystem_facts',
        'users': 'hitachivantara.vspone_block.vsp.hv_user_facts',
        'user_groups': 'hitachivantara.vspone_block.vsp.hv_user_group_facts',
    }

    def __init__(self, 
                 vars_file: str = 'ansible_vault_vars/ansible_vault_storage_var.yml',
                 output_file: str = 'all_storage_facts.json',
                 vault_password_file: Optional[str] = None):
        """
        Initialize the aggregator.
        
        Args:
            vars_file: Path to the Ansible vault variables file
            output_file: Path where the JSON output will be saved
            vault_password_file: Path to vault password file (if needed)
        """
        self.vars_file = vars_file
        self.output_file = output_file
        self.vault_password_file = vault_password_file
        self.all_facts: Dict[str, Any] = {}

    def generate_playbook(self) -> str:
        """Generate a dynamic Ansible playbook for gathering all facts."""
        
        playbook_content = f"""---
- name: Gather All Storage System Facts
  hosts: localhost
  gather_facts: false

  vars_files:
    - {self.vars_file}

  vars:
    connection_info:
      address: "{{{{ storage_address }}}}"
      username: "{{{{ vault_storage_username }}}}"
      password: "{{{{ vault_storage_secret }}}}"

  tasks:
"""
        
        # Add tasks for each fact module
        for key, module in self.FACTS_MODULES.items():
            # Special handling for monitor facts that need spec
            if key in ['hardware_installed', 'channel_boards']:
                if key == 'hardware_installed':
                    spec = """        spec:
          query: "hardware_installed"
          include_component_option: false"""
                else:
                    spec = """        spec:
          query: "channel_boards\""""
                
                playbook_content += f"""
    - name: Get {key}
      {module}:
        connection_info: "{{{{ connection_info }}}}"
{spec}
      register: {key}_result
      ignore_errors: true

    - name: Set fact for {key}
      set_fact:
        all_facts_{key}: "{{{{ {key}_result.get('data', {{}}) }}}}"
      ignore_errors: true
"""
            else:
                playbook_content += f"""
    - name: Get {key}
      {module}:
        connection_info: "{{{{ connection_info }}}}"
      register: {key}_result
      ignore_errors: true

    - name: Set fact for {key}
      set_fact:
        all_facts_{key}: "{{{{ {key}_result.get('data', {{}}) }}}}"
      ignore_errors: true
"""
        
        # Add task to aggregate all facts
        aggregation_vars = ", ".join([f"all_facts_{key}" for key in self.FACTS_MODULES.keys()])
        
        playbook_content += f"""
    - name: Aggregate all facts
      set_fact:
        combined_facts:
"""
        
        for key in self.FACTS_MODULES.keys():
            playbook_content += f"          {key}: \"{{{{ all_facts_{key} }}}}\"\n"
        
        playbook_content += """
    - name: Display aggregated facts
      debug:
        msg: "Aggregated {{ combined_facts | length }} fact categories"

    - name: Save facts to JSON file
      copy:
        content: "{{ combined_facts | to_nice_json }}"
        dest: """ + f'"{self.output_file}"' + """
      register: save_result

    - name: Confirm file saved
      debug:
        msg: "Facts saved to {{ save_result.dest }}"
"""
        
        return playbook_content

    def run(self) -> bool:
        """
        Execute the fact gathering playbook.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create temporary playbook file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.yml',
                delete=False,
                dir='.'
            ) as f:
                playbook_path = f.name
                f.write(self.generate_playbook())
            
            print(f"[*] Generated playbook: {playbook_path}")
            
            # Build ansible-playbook command
            cmd = ['ansible-playbook', playbook_path]
            
            # Add vault password file if provided
            if self.vault_password_file:
                cmd.extend(['--vault-password-file', self.vault_password_file])
            
            print(f"[*] Running: {' '.join(cmd)}")
            
            # Execute the playbook
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True
            )
            
            # Clean up temporary file
            Path(playbook_path).unlink(missing_ok=True)
            
            if result.returncode == 0:
                print(f"\n[✓] Facts successfully gathered and saved to: {self.output_file}")
                
                # Verify the JSON file was created
                if os.path.exists(self.output_file):
                    with open(self.output_file, 'r') as f:
                        data = json.load(f)
                    print(f"[✓] JSON file contains {len(data)} fact categories")
                    return True
                else:
                    print(f"[✗] Output file not found: {self.output_file}")
                    return False
            else:
                print(f"\n[✗] Playbook execution failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            print(f"[✗] Error during execution: {e}")
            return False

    def run_simple(self) -> bool:
        """
        Execute using the existing Ansible role.
        
        This method runs the pre-configured gather_all_facts.yml playbook.
        """
        try:
            cmd = [
                'ansible-playbook',
                'gather_all_facts.yml',
                '-e', f'facts_output_file={self.output_file}'
            ]
            
            if self.vault_password_file:
                cmd.extend(['--vault-password-file', self.vault_password_file])
            
            print(f"[*] Running: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode == 0:
                print(f"\n[✓] Facts successfully gathered and saved to: {self.output_file}")
                return True
            else:
                print(f"\n[✗] Playbook execution failed with return code: {result.returncode}")
                return False
                
        except Exception as e:
            print(f"[✗] Error during execution: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Gather all storage system facts into a JSON file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using default settings
  python3 gather_all_facts.py

  # Specify custom output file
  python3 gather_all_facts.py --output-file /tmp/storage_facts.json

  # Use vault password file
  python3 gather_all_facts.py --vault-password-file ~/.vault_pass

  # Custom variables file
  python3 gather_all_facts.py --vars-file /path/to/vars.yml
        """
    )
    
    parser.add_argument(
        '--output-file',
        '-o',
        default='all_storage_facts.json',
        help='Output JSON file path (default: all_storage_facts.json)'
    )
    
    parser.add_argument(
        '--vars-file',
        '-v',
        default='ansible_vault_vars/ansible_vault_storage_var.yml',
        help='Path to Ansible vault variables file (default: ansible_vault_vars/ansible_vault_storage_var.yml)'
    )
    
    parser.add_argument(
        '--vault-password-file',
        '-p',
        help='Path to Ansible vault password file'
    )
    
    parser.add_argument(
        '--use-role',
        action='store_true',
        help='Use the existing Ansible role instead of generating a playbook'
    )
    
    args = parser.parse_args()
    
    # Create aggregator
    aggregator = StorageFactsAggregator(
        vars_file=args.vars_file,
        output_file=args.output_file,
        vault_password_file=args.vault_password_file
    )
    
    print("=" * 70)
    print("Storage Facts Aggregator")
    print("=" * 70)
    print(f"Output file: {args.output_file}")
    print(f"Vars file: {args.vars_file}")
    if args.vault_password_file:
        print(f"Vault password file: {args.vault_password_file}")
    print("=" * 70)
    print()
    
    # Run the aggregator
    if args.use_role:
        success = aggregator.run_simple()
    else:
        success = aggregator.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
