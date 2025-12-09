#!/usr/bin/env python3
"""
Storage Facts JSON Processor

Utility script to process and analyze the aggregated storage facts JSON file.
Provides various operations such as extraction, filtering, and reporting.

Usage:
    python3 process_facts.py [COMMAND] [OPTIONS]
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class StorageFactsProcessor:
    """Process and analyze storage facts JSON data."""

    def __init__(self, json_file: str):
        """
        Initialize processor with JSON file.
        
        Args:
            json_file: Path to the JSON facts file
        """
        self.json_file = json_file
        self.data = self._load_json()

    def _load_json(self) -> Dict[str, Any]:
        """Load JSON file."""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {self.json_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON file: {self.json_file}")
            sys.exit(1)

    def summary(self) -> None:
        """Display summary statistics of facts."""
        print("\n" + "=" * 70)
        print("Storage Facts Summary")
        print("=" * 70)
        print(f"File: {self.json_file}")
        print(f"Loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nTotal Fact Categories: {len(self.data)}")
        print("\nBreakdown:")
        
        total_items = 0
        for category, content in sorted(self.data.items()):
            if isinstance(content, dict):
                data_list = content.get('data', [])
                if isinstance(data_list, list):
                    count = len(data_list)
                else:
                    count = 1 if data_list else 0
            else:
                count = 0
            
            total_items += count
            status = "✓" if count > 0 else "-"
            print(f"  [{status}] {category:40s}: {count:6d} items")
        
        print(f"\nTotal Items: {total_items}")
        print("=" * 70 + "\n")

    def extract(self, category: str, output_file: str) -> None:
        """Extract specific fact category to file."""
        if category not in self.data:
            print(f"Error: Category '{category}' not found")
            print(f"Available categories: {', '.join(sorted(self.data.keys()))}")
            sys.exit(1)
        
        extracted = self.data[category]
        with open(output_file, 'w') as f:
            json.dump(extracted, f, indent=2)
        
        print(f"✓ Extracted '{category}' to {output_file}")

    def list_categories(self) -> None:
        """List all available fact categories."""
        print("\nAvailable Fact Categories:")
        print("-" * 70)
        for category in sorted(self.data.keys()):
            print(f"  - {category}")
        print()

    def filter(self, category: str, key: str, value: str, output_file: str) -> None:
        """Filter items in a category by key-value."""
        if category not in self.data:
            print(f"Error: Category '{category}' not found")
            sys.exit(1)
        
        data = self.data[category]
        if not isinstance(data, dict) or 'data' not in data:
            print(f"Error: Category '{category}' has unexpected structure")
            sys.exit(1)
        
        items = data['data']
        if not isinstance(items, list):
            print(f"Error: Data in '{category}' is not a list")
            sys.exit(1)
        
        filtered = [item for item in items if isinstance(item, dict) and item.get(key) == value]
        
        result = {'data': filtered}
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✓ Filtered {len(filtered)} items from '{category}' where {key}={value}")
        print(f"✓ Results saved to {output_file}")

    def validate(self) -> None:
        """Validate JSON structure."""
        print("\nValidating Storage Facts JSON...")
        print("-" * 70)
        
        errors = []
        warnings = []
        
        # Check main structure
        if not isinstance(self.data, dict):
            errors.append("Root element is not a dictionary")
        
        # Check each category
        for category, content in self.data.items():
            if not isinstance(content, dict):
                warnings.append(f"Category '{category}' is not a dictionary")
            else:
                if 'data' in content:
                    data = content['data']
                    if not isinstance(data, (list, dict)):
                        warnings.append(f"Category '{category}' data is neither list nor dict")
                else:
                    warnings.append(f"Category '{category}' missing 'data' key")
        
        # Report results
        if errors:
            print(f"\n✗ Errors found ({len(errors)}):")
            for error in errors:
                print(f"  - {error}")
            return_code = 1
        else:
            print("✓ No errors found")
            return_code = 0
        
        if warnings:
            print(f"\n! Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  - {warning}")
        
        print()
        return return_code

    def count(self, category: str) -> None:
        """Count items in a category."""
        if category not in self.data:
            print(f"Error: Category '{category}' not found")
            sys.exit(1)
        
        content = self.data[category]
        if isinstance(content, dict):
            data = content.get('data', [])
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                count = 1
            else:
                count = 0
        else:
            count = 0
        
        print(f"Category '{category}' contains {count} items")

    def export_csv(self, category: str, output_file: str) -> None:
        """Export category data as CSV."""
        import csv
        
        if category not in self.data:
            print(f"Error: Category '{category}' not found")
            sys.exit(1)
        
        content = self.data[category]
        if not isinstance(content, dict) or 'data' not in content:
            print(f"Error: Category '{category}' has unexpected structure")
            sys.exit(1)
        
        items = content['data']
        if not isinstance(items, list) or len(items) == 0:
            print(f"Error: No items to export from '{category}'")
            sys.exit(1)
        
        # Get all keys from all items
        fieldnames = set()
        for item in items:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
        
        fieldnames = sorted(list(fieldnames))
        
        # Write CSV
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)
        
        print(f"✓ Exported {len(items)} items from '{category}' to {output_file}")
        print(f"✓ Columns: {', '.join(fieldnames[:5])}...")

    def diff(self, other_file: str) -> None:
        """Compare with another facts file."""
        try:
            with open(other_file, 'r') as f:
                other_data = json.load(f)
        except Exception as e:
            print(f"Error: Could not load file {other_file}: {e}")
            sys.exit(1)
        
        print("\nComparing Storage Facts Files...")
        print("-" * 70)
        
        # Compare keys
        keys1 = set(self.data.keys())
        keys2 = set(other_data.keys())
        
        only_in_first = keys1 - keys2
        only_in_second = keys2 - keys1
        common = keys1 & keys2
        
        print(f"\nCategories in first file only ({len(only_in_first)}):")
        for key in sorted(only_in_first):
            print(f"  - {key}")
        
        print(f"\nCategories in second file only ({len(only_in_second)}):")
        for key in sorted(only_in_second):
            print(f"  - {key}")
        
        print(f"\nCommon categories ({len(common)}):")
        for key in sorted(common):
            count1 = self._get_item_count(self.data[key])
            count2 = self._get_item_count(other_data[key])
            symbol = "=" if count1 == count2 else "≠"
            print(f"  [{symbol}] {key:40s}: {count1:6d} vs {count2:6d}")
        
        print()

    @staticmethod
    def _get_item_count(content: Any) -> int:
        """Get item count from content."""
        if isinstance(content, dict):
            data = content.get('data', [])
            if isinstance(data, list):
                return len(data)
            elif isinstance(data, dict):
                return 1
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Process and analyze storage facts JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Display summary
  python3 process_facts.py -f all_storage_facts.json summary
  
  # List all categories
  python3 process_facts.py -f all_storage_facts.json list
  
  # Extract specific category
  python3 process_facts.py -f all_storage_facts.json extract ldevs -o ldevs.json
  
  # Count items in category
  python3 process_facts.py -f all_storage_facts.json count ldevs
  
  # Filter by key-value
  python3 process_facts.py -f all_storage_facts.json filter ldevs status "Defined" -o active_ldevs.json
  
  # Validate JSON
  python3 process_facts.py -f all_storage_facts.json validate
  
  # Export to CSV
  python3 process_facts.py -f all_storage_facts.json export ldevs -o ldevs.csv
  
  # Compare two files
  python3 process_facts.py -f all_storage_facts.json diff -c all_storage_facts_old.json
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        required=True,
        help='Path to storage facts JSON file'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Summary command
    subparsers.add_parser('summary', help='Display summary statistics')
    
    # List command
    subparsers.add_parser('list', help='List all fact categories')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate JSON structure')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract specific category')
    extract_parser.add_argument('category', help='Category name to extract')
    extract_parser.add_argument('-o', '--output', required=True, help='Output file')
    
    # Count command
    count_parser = subparsers.add_parser('count', help='Count items in category')
    count_parser.add_argument('category', help='Category name')
    
    # Filter command
    filter_parser = subparsers.add_parser('filter', help='Filter items in category')
    filter_parser.add_argument('category', help='Category name')
    filter_parser.add_argument('key', help='Key to filter by')
    filter_parser.add_argument('value', help='Value to match')
    filter_parser.add_argument('-o', '--output', required=True, help='Output file')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export category as CSV')
    export_parser.add_argument('category', help='Category name')
    export_parser.add_argument('-o', '--output', required=True, help='Output file')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Compare with another file')
    diff_parser.add_argument('-c', '--compare', required=True, help='File to compare with')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Create processor
    processor = StorageFactsProcessor(args.file)
    
    # Execute command
    if args.command == 'summary':
        processor.summary()
    elif args.command == 'list':
        processor.list_categories()
    elif args.command == 'validate':
        processor.validate()
    elif args.command == 'extract':
        processor.extract(args.category, args.output)
    elif args.command == 'count':
        processor.count(args.category)
    elif args.command == 'filter':
        processor.filter(args.category, args.key, args.value, args.output)
    elif args.command == 'export':
        processor.export_csv(args.category, args.output)
    elif args.command == 'diff':
        processor.diff(args.compare)


if __name__ == '__main__':
    main()
