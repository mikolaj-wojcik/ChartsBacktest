import inspect
class ValidateStrategy:
    """
    Complete validator for user-submitted strategies.
    Checks methods, attributes, signatures, and return types.
    """

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.required_methods = ['onTick', 'setParams', 'calculateIndicators', 'loadPrices']
        self.required_atributes = ['paramsDict']

    def validate(self, strategy_obj) -> bool:
        """
        Run all validation checks.

        Returns:
            True if all validations pass
        """
        self.errors = []
        self.warnings = []

        # Check methods exist
        self._check_required_methods(strategy_obj)

        # Check attributes
        self._check_required_attributes(strategy_obj)

        # Check method signatures
        self._check_method_signatures(strategy_obj)

        # Check return types
        self._check_return_types(strategy_obj)

        return self.errors

    def _check_required_methods(self, obj):
        """Check all required methods exist"""

        for method_name in self.required_methods:
            if not hasattr(obj, method_name):
                self.errors.append(f"Missing required method: {method_name}")
            elif not callable(getattr(obj, method_name)):
                self.errors.append(f"'{method_name}' is not callable")

    def _check_required_attributes(self, obj):
        """Check required attributes exist"""
        for attribute in self.required_atributes:
            if not hasattr(obj, attribute):
                self.errors.append(f"Missing required attribute: {attribute}")
            elif not isinstance(obj.paramsDict, dict):
                self.errors.append(f"{attribute} must be a dictionary")

    def _check_method_signatures(self, obj):
        """Validate method signatures"""

        # Check onTick signature
        if hasattr(obj, 'onTick'):
            try:
                sig = inspect.signature(obj.onTick)
                params = list(sig.parameters.keys())

                if len(params) != 1:  # self + iter
                    self.errors.append("onTick must accept at least 'iter' parameter")
            except Exception as e:
                self.errors.append(f"Error checking onTick: {str(e)}")

        if hasattr(obj, 'loadPrices'):
            try:
                sig = inspect.signature(obj.loadPrices)
                params = list(sig.parameters.keys())

                if len(params) != 1:  # self + iter
                    self.errors.append("loadPrices must accept at least 'prices' parameter")
            except Exception as e:
                self.errors.append(f"Error checking loadPrices: {str(e)}")

        # Check setParams signature
        if hasattr(obj, 'setParams'):
            try:
                sig = inspect.signature(obj.setParams)
                params = list(sig.parameters.keys())

                if len(params) != 1:  # self + params
                    self.errors.append("setParams must accept parameters argument")
            except Exception as e:
                self.errors.append(f"Error checking setParams: {str(e)}")

    def _check_return_types(self, obj):
        """Check method return types (by calling them if possible)"""

        # Test onTick return type
        if hasattr(obj, 'onTick'):
            try:
                # Try to call with dummy data
                result = obj.onTick(0)

                if not isinstance(result, tuple):
                    self.errors.append("onTick must return a tuple")
                elif len(result) != 2:
                    self.errors.append("onTick must return (recommendation, size)")
                else:
                    recommendation, size = result
                    if not isinstance(recommendation, int):
                        self.errors.append("onTick recommendation (first returned value) must be int")
                    if not isinstance(size, (int, float)):
                        self.errors.append("onTick size (second returned value) must be numeric")

            except Exception as e:
                self.warnings.append(f"Could not test onTick: {str(e)}")

def validate_parmsDict(definition, actual):

    for key in actual.keys():
        if key not in definition.keys():
            return False
        if len(actual[key]) != 3:
            return False
        for single_value in actual[key]:
            if type(single_value) != type(definition[key]):
                return False
        if actual[key][0] > actual[key][1]:
            return False
        if actual[key][2] <= 0:
            return False
    return True