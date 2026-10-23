class Calculator:
    """
    A simple calculator class to perform basic arithmetic operations:
    addition, subtraction, multiplication, and division.
    """

    def add(self, a, b):
        """
        Returns the sum of a and b.
        """
        return a + b

    def subtract(self, a, b):
        """
        Returns the difference of a and b.
        """
        return a - b

    def multiply(self, a, b):
        """
        Returns the product of a and b.
        """
        return a * b

    def divide(self, a, b):
        """
        Returns the quotient of a and b.
        Raises ValueError if b is zero.
        """
        if b == 0:
            raise ValueError('Division by zero is undefined.')
        return a / b

# Example usage:
# calculator = Calculator()
# print(calculator.add(5, 3))  # Output: 8
# print(calculator.subtract(5, 3))  # Output: 2
# print(calculator.multiply(5, 3))  # Output: 15
# print(calculator.divide(5, 3))  # Output: 1.6667