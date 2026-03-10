"""
Controller
Main orchestration logic for parsing files (single or batch)
"""

import os
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

from lexers import tokenize_c, tokenize_java, tokenize_python
from parsers import parse_c, parse_java, parse_python
from main.error_classifier import ErrorClassifier, classify_parse_errors
from main.utils import (
    read_file, write_json, get_language_from_extension,
    find_files, format_summary_report, ProgressBar
)
from syntax_tree.ast_nodes import Program, ast_to_dict


class ParserController:
    """Main controller for parsing operations"""
    
    def __init__(self):
        self.supported_languages = ['c', 'java', 'python']
        self.language_handlers = {
            'c': (tokenize_c, parse_c),
            'java': (tokenize_java, parse_java),
            'python': (tokenize_python, parse_python)
        }
    
    def parse_file(self, filepath: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse a single file
        
        Args:
            filepath: Path to source file
            language: Language override (auto-detect if None)
        
        Returns:
            Dictionary containing parse results and errors
        """
        # Determine language
        if language is None:
            language = get_language_from_extension(filepath)
        
        if language not in self.supported_languages:
            return {
                'success': False,
                'filepath': filepath,
                'error': f'Unsupported language: {language}'
            }
        
        try:
            # Read source code
            source_code = read_file(filepath)
            
            # Get language handlers
            tokenizer, parser = self.language_handlers[language]
            
            # Tokenize
            tokens = tokenizer(source_code)
            
            # Parse
            ast_tree, errors = parser(tokens)
            
            # Classify errors
            error_summary = classify_parse_errors(language, errors)
            
            # Build result
            result = {
                'success': len(errors) == 0,
                'filepath': filepath,
                'language': language,
                'total_tokens': len(tokens),
                'total_errors': len(errors),
                'error_summary': error_summary,
                'ast': ast_to_dict(ast_tree) if ast_tree else None
            }
            
            return result
        
        except Exception as e:
            return {
                'success': False,
                'filepath': filepath,
                'error': str(e)
            }
    
    def parse_batch(self, directory: str, language: Optional[str] = None,
                   recursive: bool = True, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse multiple files in a directory
        
        Args:
            directory: Directory containing source files
            language: Language filter (None for all)
            recursive: Search subdirectories
            output_dir: Directory to save results (None to skip saving)
        
        Returns:
            Dictionary containing batch parse results
        """
        # Determine file extensions
        if language:
            if language == 'c':
                extensions = ['.c', '.cpp', '.h', '.hpp']
            elif language == 'java':
                extensions = ['.java']
            elif language == 'python':
                extensions = ['.py']
            else:
                extensions = []
        else:
            extensions = ['.c', '.cpp', '.h', '.hpp', '.java', '.py']
        
        # Find files
        if recursive:
            files = find_files(directory, extensions)
        else:
            files = [os.path.join(directory, f) for f in os.listdir(directory)
                    if any(f.endswith(ext) for ext in extensions)]
        
        if not files:
            return {
                'success': False,
                'error': 'No source files found',
                'directory': directory
            }
        
        # Parse each file
        results = []
        summaries = []
        failed_files = []
        
        print(f"\nParsing {len(files)} files...")
        progress = ProgressBar(len(files), prefix="Progress")
        
        for filepath in files:
            try:
                # Parse with timeout protection (track start time)
                import time
                start_time = time.time()
                
                result = self.parse_file(filepath, language)
                
                parse_time = time.time() - start_time
                result['parse_time'] = parse_time
                
                # Warn if parsing took too long (potential issue)
                if parse_time > 5.0:  # 5 seconds is unusually long for simple parsing
                    result['warning'] = f'Parsing took {parse_time:.2f}s (possibly complex or problematic file)'
                
                results.append(result)
                
                if result.get('success') is not None:
                    summaries.append(result.get('error_summary', {}))
                    
            except KeyboardInterrupt:
                # Allow user to cancel batch processing
                print("\n\nBatch processing cancelled by user")
                failed_files.append(filepath)
                break
                
            except Exception as e:
                # Handle unexpected errors gracefully
                error_result = {
                    'success': False,
                    'filepath': filepath,
                    'error': f'Parse failed with exception: {str(e)}',
                    'exception_type': type(e).__name__
                }
                results.append(error_result)
                failed_files.append(filepath)
            
            progress.update()
        
        progress.finish()
        
        # Merge summaries
        merged_summary = ErrorClassifier.merge_summaries(summaries)
        
        # Calculate stats
        total_files = len(files)
        successful_parses = sum(1 for r in results if r.get('success', False))
        failed_parses = sum(1 for r in results if r.get('success', False) is False)
        files_with_errors = sum(1 for r in results if r.get('total_errors', 0) > 0)
        
        batch_result = {
            'success': True,
            'directory': directory,
            'total_files': total_files,
            'successful_parses': successful_parses,
            'failed_parses': failed_parses,
            'files_with_syntax_errors': files_with_errors,
            'file_results': results,
            'error_summary': merged_summary
        }
        
        # Save results if output directory specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save full results
            results_file = os.path.join(output_dir, 'batch_results.json')
            write_json(results_file, batch_result)
            
            # Save summary report
            summary_file = os.path.join(output_dir, 'summary.txt')
            summary_text = format_summary_report(merged_summary)
            with open(summary_file, 'w') as f:
                f.write(summary_text)
            
            print(f"\nResults saved to: {output_dir}")
            print(f"  - {results_file}")
            print(f"  - {summary_file}")
        
        return batch_result
    
    def display_result(self, result: Dict[str, Any]):
        """Display parse result in readable format"""
        print("\n" + "=" * 60)
        
        if result.get('success'):
            print(f"✓ Successfully parsed: {result.get('filepath', 'Unknown')}")
            print(f"  Language: {result.get('language', 'Unknown').upper()}")
            print(f"  Tokens: {result.get('total_tokens', 0)}")
            print(f"  Errors: {result.get('total_errors', 0)}")
        else:
            print(f"✗ Failed to parse: {result.get('filepath', 'Unknown')}")
            
            # Check if we have structured error summary
            if 'error_summary' in result and result.get('total_errors', 0) > 0:
                print(f"  Language: {result.get('language', 'Unknown').upper()}")
                print(f"  Tokens: {result.get('total_tokens', 0)}")
                print(f"  Errors: {result.get('total_errors', 0)}")
                print("\n" + format_summary_report(result.get('error_summary', {})))
            else:
                # Generic error (exception occurred)
                print(f"  Error: {result.get('error', 'Unknown error')}")
        
        print("=" * 60)
    
    def display_batch_summary(self, batch_result: Dict[str, Any]):
        """Display batch processing summary"""
        print("\n" + "=" * 70)
        print("BATCH PROCESSING SUMMARY")
        print("=" * 70)
        
        print(f"\nDirectory: {batch_result.get('directory', 'Unknown')}")
        print(f"Total Files: {batch_result.get('total_files', 0)}")
        print(f"Successful Parses: {batch_result.get('successful_parses', 0)}")
        print(f"Failed Parses: {batch_result.get('failed_parses', 0)}")
        print(f"Files with Syntax Errors: {batch_result.get('files_with_syntax_errors', 0)}")
        
        # Error summary
        if batch_result.get('error_summary'):
            print("\n" + format_summary_report(batch_result['error_summary']))
        
        print("=" * 70)


# Convenience functions
def parse_single_file(filepath: str, language: Optional[str] = None) -> Dict[str, Any]:
    """Parse a single file (convenience function)"""
    controller = ParserController()
    return controller.parse_file(filepath, language)


def parse_directory(directory: str, language: Optional[str] = None, 
                   output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Parse all files in directory (convenience function)"""
    controller = ParserController()
    return controller.parse_batch(directory, language, output_dir=output_dir)
