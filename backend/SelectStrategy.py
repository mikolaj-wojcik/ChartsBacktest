import importlib
import importlib.util
import sys
import os
import ast
import tempfile
from logging import exception
from pathlib import Path
from typing import Optional, Union
from abc import ABC
from warnings import catch_warnings


class StrategyLoader:


    strat_path = "Strategies"
    ALLOWED_IMPORTS = {
        'pandas', 'pd',
        'numpy', 'np',
        'ta', 'ta.trend', 'ta.momentum', 'ta.volatility',
        'math',
        'datetime',
        'typing',
        'Strategies.Strategy',
        'Strategies'
    }

    FORBIDDEN_CALLS = {
        'eval', 'exec', 'compile', '__import__',
        'open', 'file', 'input',
        'os.system', 'subprocess',
    }

    def __init__(self, strategy_base_class=None):
        """
        Initialize strategy loader.

        Args:
            strategy_base_class: Base class that strategies must inherit from
        """
        self.strategy = strategy_base_class
        self._loaded_modules = {}

    def load_predef_strategy(self, strategy_name):
            # Import from Strategies package
            try:
                module_path = f'{self.strat_path}.{strategy_name}'
                module = importlib.import_module(module_path)

                # Get the class with same name as module
                strategy_class = getattr(module, strategy_name)

                # Instantiate and return
                return 0, strategy_class()
            except Exception as e:

                return -1, f'Error loading strategy: {str(e)}'

    def load_from_file(self, file_path: str, strategy_class_name: Optional[str] = None):
        """
        Load strategy from a Python file.

        Args:
            file_path: Path to the .py file
            strategy_class_name: Name of the strategy class (auto-detect if None)

        Returns:
            Strategy instance or 0 if failed
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                return -1, f'File {file_path} not found'

            # Read file content
            with open(file_path, 'r') as f:
                code = f.read()

            # Validate code security
            is_valid, message = self._validate_code(code)
            if not is_valid:

                return -1, f'Security validation failed: {message}'

            # Load the module
            module_name = Path(file_path).stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)

            if spec is None or spec.loader is None:

                return -1, f'Could not load module from file'

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            ret = spec.loader.exec_module(module)

            # Find strategy class
            if strategy_class_name:
                strategy_class = getattr(module, strategy_class_name, None)
            else:
                # Auto-detect: find first class that inherits from Strategy
                strategy_class = self._find_strategy_class(module)

            if strategy_class is None:

                return -1, f'No valid strategy class found in file'

            # Instantiate and return
            return 0, strategy_class()

        except Exception as e:
            #print(f'Error loading strategy from file: {str(e)}')
            import traceback
            traceback.print_exc()
            return -1, f'Error loading strategy: {str(e)}'

    def load_from_string(self, code: str, strategy_class_name: str):
        """
        Load strategy from code string.

        Args:
            code: Python code as string
            strategy_class_name: Name of the strategy class

        Returns:
            Strategy instance or 0 if failed
        """
        try:
            # Validate code security
            is_valid, message = self._validate_code(code)
            if not is_valid:
                #print(f'Security validation failed: {message}')
                return -1, f'Security validation failed: {message}'

            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_path = f.name

            try:
                # Load from temporary file
                return self.load_from_file(temp_path, strategy_class_name)
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass

        except Exception as e:
           # print(f'Error loading strategy from string: {str(e)}')
            return -1, f'Error loading strategy: {str(e)}'

    def _validate_code(self, code):
        """
        Validate strategy code for security issues.

        Args:
            code: Python code to validate

        Returns:
            (is_valid, message)
        """
        try:
            # Parse into AST
            tree = ast.parse(code)

            # Check imports
            for node in ast.walk(tree):
                # Check 'import x' statements
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split('.')[0]
                        if module not in self.ALLOWED_IMPORTS:
                            return False, f"Import not allowed: {alias.name}"

                # Check 'from x import y' statements
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split('.')[0]
                        if module not in self.ALLOWED_IMPORTS:
                            return False, f"Import not allowed: {node.module}"

                # Check function calls
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.FORBIDDEN_CALLS:
                            return False, f"Forbidden function: {node.func.id}"
                    elif isinstance(node.func, ast.Attribute):
                        func_name = f"{node.func.value.id if isinstance(node.func.value, ast.Name) else ''}.{node.func.attr}"
                        if func_name in self.FORBIDDEN_CALLS:
                            return False, f"Forbidden function: {func_name}"

            return True, "Validation passed"

        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def _find_strategy_class(self, module):
        """
        Find strategy class in module by checking inheritance.

        Args:
            module: Python module object

        Returns:
            Strategy class or None
        """
        import inspect

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                # Check if it's defined in this module (not imported)
                if obj.__module__ == module.__name__:
                    # Check if it has required attributes/methods
                    if hasattr(obj, 'onTick') and hasattr(obj, 'paramsDict'):
                        return obj

        return None

    def ListDefaultStrategies(self):
        strategies_lst = []
        strategy_path = Path(self.strat_path)

        if strategy_path.exists():
            for file in strategy_path.glob('*.py'):
                if file.stem !='Strategy':
                    strategies_lst.append(file.stem)

        return strategies_lst




# ============================================================================
# Updated SelectStrategy function (backward compatible)
# ============================================================================

def SelectStrategy(strategy_identifier: Union[str, dict]):
    """
    Load strategy from built-in folder, file path, or code string.

    Args:
        strategy_identifier: Can be:
            - str: Name of built-in strategy OR path to .py file
            - dict: {'code': '...', 'class_name': '...'} for code string
        strategy_loader: Optional StrategyLoader instance

    Returns:
        Strategy instance or 0 if failed

    Examples:
        # Load built-in strategy
        strategy = SelectStrategy("SMAcross")

        # Load from file
        strategy = SelectStrategy("/path/to/my_strategy.py")

        # Load from code string
        strategy = SelectStrategy({
            'code': 'class MyStrategy: ...',
            'class_name': 'MyStrategy'
        })
    """

    strategy_loader = StrategyLoader()

    # Handle different input types
    if isinstance(strategy_identifier, dict):
        # Load from code string
        code = strategy_identifier.get('code', '')
        class_name = strategy_identifier.get('class_name', '')

        #if not code or not class_name:
        #    return -1,'Dictionary must contain "code" and "class_name" keys'

        return strategy_loader.load_from_string(code, class_name)

    elif isinstance(strategy_identifier, str):
        return strategy_loader.load_predef_strategy(strategy_identifier)

    else:
        return -1 , f'Invalid strategy identifier type: {type(strategy_identifier)}'

def GetParamsDictOfStrategy(strategy):
    if strategy is not None:
        try:
            return strategy.paramsDict
        except AttributeError:
            return  "Strategy has no paramsDict"

    return "Strategy is not loaded"
