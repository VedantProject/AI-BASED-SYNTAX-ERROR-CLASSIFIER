"""
Main Entry Point for Multi-Language Parser Framework
Provides CLI interface for parsing single files or batch processing
"""

import argparse
import sys
from main.controller import ParserController
from main.utils import format_summary_report


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Multi-Language Parser Framework - Syntax Error Classification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse a single C file
  python main.py --file test.c --language c
  
  # Parse a single Java file (language auto-detected)
  python main.py --file Test.java
  
  # Batch process all files in a directory
  python main.py --batch datasets/c/ --language c
  
  # Batch process with output saved
  python main.py --batch datasets/python/ --output results/
  
  # Generate datasets first
  python dataset_generator.py --language all --valid 500 --invalid 500
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', 
                            help='Parse a single file')
    input_group.add_argument('--batch', '-b', 
                            help='Parse all files in directory')
    
    # Language option
    parser.add_argument('--language', '-l', 
                       choices=['c', 'java', 'python'],
                       help='Programming language (auto-detect if not specified)')
    
    # Output option
    parser.add_argument('--output', '-o',
                       help='Output directory for results (batch mode only)')
    
    # Verbosity
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    
    args = parser.parse_args()
    
    # Create controller
    controller = ParserController()
    
    try:
        if args.file:
            # Single file mode
            print(f"\nParsing file: {args.file}")
            result = controller.parse_file(args.file, args.language)
            
            if args.json:
                import json
                print(json.dumps(result, indent=2))
            else:
                controller.display_result(result)
            
            # Exit with error code if parsing failed
            sys.exit(0 if result.get('success') else 1)
        
        elif args.batch:
            # Batch mode
            print(f"\nBatch processing directory: {args.batch}")
            result = controller.parse_batch(
                args.batch, 
                args.language,
                output_dir=args.output
            )
            
            if args.json:
                import json
                # Don't include full file results in JSON (too large)
                summary_result = {
                    'directory': result['directory'],
                    'total_files': result['total_files'],
                    'successful_parses': result['successful_parses'],
                    'failed_parses': result['failed_parses'],
                    'files_with_syntax_errors': result['files_with_syntax_errors'],
                    'error_summary': result['error_summary']
                }
                print(json.dumps(summary_result, indent=2))
            else:
                controller.display_batch_summary(result)
            
            # Show example errors if verbose
            if args.verbose and result.get('file_results'):
                print("\n" + "=" * 70)
                print("SAMPLE ERROR DETAILS (first 5 files with errors)")
                print("=" * 70)
                
                shown = 0
                for file_result in result['file_results']:
                    if file_result.get('total_errors', 0) > 0 and shown < 5:
                        print(f"\nFile: {file_result['filepath']}")
                        print(f"Errors: {file_result['total_errors']}")
                        
                        if file_result.get('error_summary', {}).get('errors'):
                            for i, error in enumerate(file_result['error_summary']['errors'][:3], 1):
                                print(f"  {i}. Line {error['line']}: {error['message']}")
                        
                        shown += 1
            
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
