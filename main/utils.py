"""
Utility Functions
Common utilities for file handling, JSON operations, and formatting
"""

import os
import json
from typing import Dict, Any, List
from pathlib import Path


def ensure_dir(directory: str):
    """Create directory if it doesn't exist"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def read_file(filepath: str) -> str:
    """Read file contents"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Error reading file {filepath}: {str(e)}")


def write_file(filepath: str, content: str):
    """Write content to file"""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def write_json(filepath: str, data: Any, indent: int = 2):
    """Write JSON data to file"""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def read_json(filepath: str) -> Any:
    """Read JSON data from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_language_from_extension(filepath: str) -> str:
    """Determine language from file extension"""
    ext = os.path.splitext(filepath)[1].lower()
    
    extension_map = {
        '.c': 'c',
        '.cpp': 'c',
        '.cc': 'c',
        '.cxx': 'c',
        '.h': 'c',
        '.hpp': 'c',
        '.java': 'java',
        '.py': 'python'
    }
    
    return extension_map.get(ext, 'unknown')


def find_files(directory: str, extensions: List[str]) -> List[str]:
    """Find all files with given extensions in directory"""
    files = []
    
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    
    return files


def format_summary_report(summary: Dict[str, Any]) -> str:
    """Format error summary as readable text report"""
    lines = []
    lines.append("=" * 60)
    lines.append("PARSING SUMMARY REPORT")
    lines.append("=" * 60)
    
    if 'total_files' in summary:
        # Batch summary
        lines.append(f"\nTotal Files Processed: {summary['total_files']}")
        lines.append(f"Total Errors Found: {summary['total_errors']}")
        
        if summary['by_language']:
            lines.append("\n--- By Language ---")
            for lang, stats in summary['by_language'].items():
                lines.append(f"\n{lang.upper()}:")
                lines.append(f"  Files: {stats['files']}")
                lines.append(f"  Errors: {stats['errors']}")
                
                if stats['categories']:
                    lines.append("  Error Categories:")
                    for category, count in sorted(stats['categories'].items()):
                        lines.append(f"    - {category}: {count}")
        
        if summary['by_category']:
            lines.append("\n--- Overall Error Categories ---")
            for category, count in sorted(summary['by_category'].items(), 
                                         key=lambda x: x[1], reverse=True):
                lines.append(f"  {category}: {count}")
    
    else:
        # Single file summary
        lines.append(f"\nLanguage: {summary.get('language', 'Unknown')}")
        lines.append(f"Total Errors: {summary.get('total_errors', 0)}")
        
        if summary.get('error_categories'):
            lines.append("\nError Categories:")
            for category, count in sorted(summary['error_categories'].items()):
                lines.append(f"  - {category}: {count}")
        
        if summary.get('errors'):
            lines.append(f"\nDetailed Errors ({len(summary['errors'])}):")
            for i, error in enumerate(summary['errors'][:20], 1):  # Show first 20
                lines.append(f"  {i}. Line {error['line']}: {error['message']}")
            
            if len(summary['errors']) > 20:
                lines.append(f"  ... and {len(summary['errors']) - 20} more")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Format data as ASCII table"""
    if not rows:
        return ""
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build table
    lines = []
    
    # Header
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    lines.append(header_line)
    lines.append("-" * len(header_line))
    
    # Rows
    for row in rows:
        row_line = " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
        lines.append(row_line)
    
    return "\n".join(lines)


def get_file_stats(filepath: str) -> Dict[str, Any]:
    """Get basic file statistics"""
    content = read_file(filepath)
    lines = content.split('\n')
    
    return {
        'path': filepath,
        'size_bytes': len(content),
        'total_lines': len(lines),
        'non_empty_lines': len([l for l in lines if l.strip()]),
        'language': get_language_from_extension(filepath)
    }


def truncate_string(s: str, max_length: int = 100) -> str:
    """Truncate string to maximum length"""
    if len(s) <= max_length:
        return s
    return s[:max_length-3] + '...'


class ProgressBar:
    """Simple progress bar for batch operations"""
    
    def __init__(self, total: int, prefix: str = "Progress", width: int = 50):
        self.total = total
        self.prefix = prefix
        self.width = width
        self.current = 0
    
    def update(self, count: int = 1):
        """Update progress bar"""
        self.current += count
        self.display()
    
    def display(self):
        """Display current progress"""
        if self.total == 0:
            percent = 100
        else:
            percent = int(100 * self.current / self.total)
        
        filled = int(self.width * self.current / self.total) if self.total > 0 else self.width
        bar = '#' * filled + '-' * (self.width - filled)
        
        print(f'\r{self.prefix}: |{bar}| {percent}% ({self.current}/{self.total})', end='', flush=True)
    
    def finish(self):
        """Finish progress bar"""
        self.current = self.total
        self.display()
        print()  # New line
