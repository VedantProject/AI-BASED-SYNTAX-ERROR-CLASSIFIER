"""
Error Classifier
Categorizes and structures syntax errors detected during parsing
"""

from typing import List, Dict, Any
from syntax_tree.ast_nodes import ErrorNode


class ErrorClassifier:
    """Classifies and formats syntax errors"""
    
    # Error category mappings
    ERROR_CATEGORIES = {
        'MISSING_SEMICOLON': 'Missing Delimiter',
        'MISSING_BRACE': 'Missing Delimiter',
        'MISSING_PAREN': 'Missing Delimiter',
        'MISSING_BRACKET': 'Missing Delimiter',
        'MISSING_COLON': 'Missing Delimiter',
        'UNMATCHED_DELIMITER': 'Unmatched Delimiter',
        
        'INVALID_EXPRESSION': 'Malformed Expression',
        'INVALID_DECLARATION': 'Invalid Declaration',
        'INVALID_SYNTAX': 'Invalid Syntax',
        'INVALID_TYPE': 'Invalid Type Specifier',
        'MISSING_RETURN_TYPE': 'Invalid Declaration',
        'MISSING_CLASS_NAME': 'Invalid Declaration',
        'INVALID_FUNCTION_DEF': 'Invalid Declaration',
        'INVALID_CLASS_DEF': 'Invalid Declaration',
        
        'KEYWORD_MISUSE': 'Keyword Misuse',
        'INCOMPLETE_STATEMENT': 'Incomplete Statement',
        
        'INDENTATION_ERROR': 'Indentation Error',
        'INCONSISTENT_INDENTATION': 'Indentation Error',
        
        'INVALID_IMPORT': 'Invalid Import',
        'INVALID_PACKAGE': 'Invalid Package',
        'INVALID_MODIFIER': 'Invalid Modifier',
        'INVALID_PREPROCESSOR': 'Invalid Preprocessor',
        'INVALID_DECORATOR': 'Invalid Decorator',
        
        'SyntaxError': 'Syntax Error',
        'UnexpectedEOF': 'Unexpected End of File',
        'UNDEFINED_NAME': 'Undefined Name (NameError)',
    }
    
    def __init__(self, language: str):
        self.language = language
        self.errors: List[ErrorNode] = []
    
    def add_errors(self, errors: List[ErrorNode]):
        """Add errors to classify"""
        self.errors.extend(errors)
    
    def classify_errors(self) -> List[Dict[str, Any]]:
        """Classify all errors into structured format"""
        classified = []
        
        for error in self.errors:
            classified_error = self.classify_error(error)
            classified.append(classified_error)
        
        return classified
    
    def classify_error(self, error: ErrorNode) -> Dict[str, Any]:
        """Classify a single error"""
        category = self.ERROR_CATEGORIES.get(error.error_type, 'Unknown Error')
        
        return {
            'language': self.language,
            'error_type': error.error_type,
            'category': category,
            'line': error.line,
            'column': error.column,
            'message': error.message,
            'token': error.token
        }
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary statistics of errors"""
        if not self.errors:
            return {
                'language': self.language,
                'total_errors': 0,
                'error_categories': {},
                'error_types': {}
            }
        
        classified = self.classify_errors()
        
        # Count by category
        categories = {}
        error_types = {}
        
        for error in classified:
            category = error['category']
            error_type = error['error_type']
            
            categories[category] = categories.get(category, 0) + 1
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            'language': self.language,
            'total_errors': len(self.errors),
            'error_categories': categories,
            'error_types': error_types,
            'errors': classified
        }
    
    def format_error_for_display(self, error_dict: Dict[str, Any]) -> str:
        """Format error for human-readable display"""
        return (
            f"{error_dict['language']} {error_dict['error_type']} "
            f"at line {error_dict['line']}, column {error_dict['column']}: "
            f"{error_dict['message']}"
        )
    
    @staticmethod
    def merge_summaries(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple error summaries (for batch processing)"""
        if not summaries:
            return {
                'total_files': 0,
                'total_errors': 0,
                'by_language': {},
                'by_category': {},
                'by_error_type': {}
            }
        
        merged = {
            'total_files': len(summaries),
            'total_errors': 0,
            'by_language': {},
            'by_category': {},
            'by_error_type': {}
        }
        
        for summary in summaries:
            language = summary.get('language', 'Unknown')
            total_errors = summary.get('total_errors', 0)
            
            merged['total_errors'] += total_errors
            
            # By language
            if language not in merged['by_language']:
                merged['by_language'][language] = {
                    'files': 0,
                    'errors': 0,
                    'categories': {},
                    'types': {}
                }
            
            merged['by_language'][language]['files'] += 1
            merged['by_language'][language]['errors'] += total_errors
            
            # By category
            for category, count in summary.get('error_categories', {}).items():
                merged['by_category'][category] = merged['by_category'].get(category, 0) + count
                merged['by_language'][language]['categories'][category] = \
                    merged['by_language'][language]['categories'].get(category, 0) + count
            
            # By error type
            for error_type, count in summary.get('error_types', {}).items():
                merged['by_error_type'][error_type] = merged['by_error_type'].get(error_type, 0) + count
                merged['by_language'][language]['types'][error_type] = \
                    merged['by_language'][language]['types'].get(error_type, 0) + count
        
        return merged


def classify_parse_errors(language: str, errors: List[ErrorNode]) -> Dict[str, Any]:
    """Convenience function to classify parsing errors"""
    classifier = ErrorClassifier(language)
    classifier.add_errors(errors)
    return classifier.get_error_summary()


def format_error_json(error_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Format error for JSON output (as specified in requirements)"""
    return {
        'language': error_dict.get('language', 'Unknown'),
        'error_type': error_dict.get('error_type', 'Unknown'),
        'line': error_dict.get('line', 0),
        'message': error_dict.get('message', '')
    }
