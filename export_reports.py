#!/usr/bin/env python3
"""Export various reports from the IMS database."""

import sys
import csv
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from reporting_service import ReportingService


def export_to_csv(data, filename, headers):
    """Export data to CSV file."""
    output_dir = project_root / "reports"
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"  Exported to: {filepath}")
    return filepath


def export_inventory_summary():
    """Export inventory summary report."""
    print("\n1. Exporting Inventory Summary...")
    service = ReportingService()
    data = service.get_inventory_summary()
    
    if data:
        headers = ['product_id', 'product_name', 'quantity', 'uom', 'price', 'category_name', 'status']
        export_to_csv(data, f"inventory_summary_{datetime.now().strftime('%Y%m%d')}.csv", headers)
        print(f"  Total products: {len(data)}")
    else:
        print("  No inventory data found")


def export_warehouse_utilization():
    """Export warehouse utilization report."""
    print("\n2. Exporting Warehouse Utilization...")
    service = ReportingService()
    data = service.get_warehouse_utilization()
    
    if data:
        headers = ['warehouse_id', 'warehouse_name', 'capacity', 'stock_count', 'total_quantity']
        export_to_csv(data, f"warehouse_utilization_{datetime.now().strftime('%Y%m%d')}.csv", headers)
        print(f"  Total warehouses: {len(data)}")
    else:
        print("  No warehouse data found")


def export_requisition_summary():
    """Export requisition summary report."""
    print("\n3. Exporting Requisition Summary...")
    service = ReportingService()
    data = service.get_requisition_summary()
    
    if data:
        headers = ['requisition_id', 'requester_username', 'status', 'created_at', 
                  'submitted_at', 'approved_at', 'project_name']
        export_to_csv(data, f"requisitions_{datetime.now().strftime('%Y%m%d')}.csv", headers)
        print(f"  Total requisitions: {len(data)}")
    else:
        print("  No requisition data found")


def export_low_stock_items():
    """Export low stock items report."""
    print("\n4. Exporting Low Stock Items...")
    service = ReportingService()
    data = service.get_low_stock_items(threshold=20)
    
    if data:
        headers = ['product_id', 'product_name', 'quantity', 'uom', 'status']
        export_to_csv(data, f"low_stock_{datetime.now().strftime('%Y%m%d')}.csv", headers)
        print(f"  Low stock items: {len(data)}")
    else:
        print("  No low stock items found")


def export_user_activity():
    """Export user activity report."""
    print("\n5. Exporting User Activity...")
    service = ReportingService()
    data = service.get_user_activity_summary()
    
    if data:
        headers = ['username', 'role_name', 'status', 'last_login', 'last_logout', 'failed_attempts']
        export_to_csv(data, f"user_activity_{datetime.now().strftime('%Y%m%d')}.csv", headers)
        print(f"  Total users: {len(data)}")
    else:
        print("  No user activity data found")


def main():
    """Export all reports."""
    print("=" * 60)
    print("IMS Report Exporter")
    print("=" * 60)
    
    try:
        export_inventory_summary()
        export_warehouse_utilization()
        export_requisition_summary()
        export_low_stock_items()
        export_user_activity()
        
        print("\n" + "=" * 60)
        print("✓ All reports exported successfully!")
        print(f"Reports saved to: {project_root / 'reports'}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error exporting reports: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
