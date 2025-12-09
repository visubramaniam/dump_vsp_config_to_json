#!/bin/bash

#############################################################################
# Storage Facts Aggregator - Quick Start Guide
# 
# This script provides common commands for gathering storage facts
#############################################################################

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_usage() {
    cat << EOF
${BLUE}Storage Facts Aggregator - Quick Start${NC}

Usage: bash quick_start.sh [COMMAND] [OPTIONS]

Commands:
    setup              Install dependencies and prepare environment
    run-role           Run using Ansible role (recommended)
    run-python         Run using Python script
    run-quick          Run with minimal options
    check-vault        Verify vault setup and credentials
    clean              Remove output files and temporary data
    help               Show this help message

Examples:
    bash quick_start.sh setup
    bash quick_start.sh run-role
    bash quick_start.sh run-python --output-file custom.json
    bash quick_start.sh check-vault

EOF
}

setup() {
    print_info "Setting up Storage Facts Aggregator..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found. Please install Python 3.6+"
        return 1
    fi
    print_success "Python 3 found: $(python3 --version)"
    
    # Check Ansible
    if ! command -v ansible &> /dev/null; then
        print_warning "Ansible not found. Installing..."
        pip3 install ansible
    fi
    print_success "Ansible found: $(ansible --version | head -n 1)"
    
    # Check Hitachi collection
    if ! ansible-galaxy collection list | grep -q hitachivantara.vspone_block; then
        print_info "Installing hitachivantara.vspone_block collection..."
        ansible-galaxy collection install hitachivantara.vspone_block
    fi
    print_success "hitachivantara.vspone_block collection is installed"
    
    # Make Python script executable
    if [ -f "gather_all_facts.py" ]; then
        chmod +x gather_all_facts.py
        print_success "gather_all_facts.py is executable"
    fi
    
    # Create output directory
    mkdir -p output
    print_success "Output directory created"
    
    print_success "Setup complete!"
    return 0
}

run_role() {
    print_info "Running facts gathering using Ansible role..."
    
    local output_file="${1:-output/all_storage_facts.json}"
    
    if [ -f "gather_all_facts.yml" ]; then
        ansible-playbook gather_all_facts.yml \
            -e facts_output_file="$output_file" \
            --vault-password-file ~/.vault_pass 2>/dev/null || \
        ansible-playbook gather_all_facts.yml \
            -e facts_output_file="$output_file" \
            --ask-vault-pass
        
        if [ -f "$output_file" ]; then
            print_success "Facts saved to: $output_file"
            print_info "File size: $(du -h "$output_file" | cut -f1)"
            return 0
        fi
    else
        print_warning "gather_all_facts.yml not found"
        return 1
    fi
}

run_python() {
    print_info "Running facts gathering using Python script..."
    
    if [ -f "gather_all_facts.py" ]; then
        python3 gather_all_facts.py "$@"
        return $?
    else
        print_warning "gather_all_facts.py not found"
        return 1
    fi
}

run_quick() {
    print_info "Running quick facts gathering (with role)..."
    
    if command -v ansible-playbook &> /dev/null; then
        if [ -f "gather_all_facts.yml" ]; then
            # Try vault password file first, then prompt
            if [ -f ~/.vault_pass ]; then
                ansible-playbook gather_all_facts.yml --vault-password-file ~/.vault_pass
            else
                ansible-playbook gather_all_facts.yml --ask-vault-pass
            fi
            
            if [ -f "output/all_storage_facts.json" ]; then
                print_success "Facts gathering complete!"
                print_info "Output: output/all_storage_facts.json"
                print_info "Size: $(du -h output/all_storage_facts.json | cut -f1)"
                return 0
            fi
        else
            print_warning "gather_all_facts.yml not found"
            return 1
        fi
    else
        print_warning "ansible-playbook not found. Running setup first..."
        setup && run_quick
    fi
}

check_vault() {
    print_info "Checking Ansible Vault setup..."
    
    local vault_file="ansible_vault_vars/ansible_vault_storage_var.yml"
    
    if [ ! -f "$vault_file" ]; then
        print_warning "Vault file not found: $vault_file"
        return 1
    fi
    
    print_success "Vault file found: $vault_file"
    
    # Try to read vault file
    if [ -f ~/.vault_pass ]; then
        print_info "Using vault password file: ~/.vault_pass"
        if ansible-vault view "$vault_file" --vault-password-file ~/.vault_pass &>/dev/null; then
            print_success "Vault file is readable and contains valid data"
            ansible-vault view "$vault_file" --vault-password-file ~/.vault_pass
            return 0
        else
            print_warning "Could not read vault file. Check password."
            return 1
        fi
    else
        print_info "No vault password file found at ~/.vault_pass"
        print_info "Attempting to read vault with password prompt..."
        ansible-vault view "$vault_file" --ask-vault-pass
    fi
}

clean() {
    print_info "Cleaning up temporary files and outputs..."
    
    if [ -d "output" ]; then
        print_warning "Removing output directory..."
        rm -rf output
    fi
    
    print_success "Cleanup complete"
}

# Main script logic
case "${1:-help}" in
    setup)
        setup
        ;;
    run-role)
        shift
        run_role "$@"
        ;;
    run-python)
        shift
        run_python "$@"
        ;;
    run-quick)
        run_quick
        ;;
    check-vault)
        check_vault
        ;;
    clean)
        clean
        ;;
    help)
        print_usage
        ;;
    *)
        print_warning "Unknown command: $1"
        print_usage
        exit 1
        ;;
esac
