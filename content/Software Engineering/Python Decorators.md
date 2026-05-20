---
title: Python Decorators
tags: [software-engineering, python, decorators, functional-programming]
draft: false
---
A decorator is a **higher-order function** that takes another function as input and returns a new function with extended or modified behavior — without altering the original function's source code. The `@decorator` syntax is syntactic sugar for `func = decorator(func)`.

Decorators are built on two fundamental Python concepts:
- **First-class functions** — functions can be assigned to variables, passed as arguments, and returned from other functions.
- **Higher-order functions** — functions that take or return other functions.

*Source: [Decorators in Python – GeeksforGeeks](https://www.geeksforgeeks.org/python/decorators-in-python/)*

---

## Anatomy of a Decorator

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # --- behavior before ---
        result = func(*args, **kwargs)
        # --- behavior after ---
        return result
    return wrapper

@decorator
def my_function():
    pass
# Equivalent to: my_function = decorator(my_function)
```

`*args` and `**kwargs` make `wrapper` generic so it can decorate any function regardless of its signature.

---

## Types of Decorators

### 1. Function Decorators
Wrap and enhance plain functions. The most common form.

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(2, 3)
# Calling add
# Finished add
```

### 2. Method Decorators
Work like function decorators but must forward the `self` parameter for instance methods.

```python
def method_decorator(func):
    def wrapper(self, *args, **kwargs):
        print("Before method execution")
        result = func(self, *args, **kwargs)
        print("After method execution")
        return result
    return wrapper

class MyClass:
    @method_decorator
    def say_hello(self):
        print("Hello!")
```

### 3. Class Decorators
Applied to an entire class definition. Receive the class as argument and return a (modified) class.

```python
def add_class_name(cls):
    cls.class_name = cls.__name__
    return cls

@add_class_name
class Person:
    pass

print(Person.class_name)  # Person
```

---

## Built-in Python Decorators

| Decorator | Purpose |
|---|---|
| `@staticmethod` | Defines a method with no access to `self` or `cls`; callable on the class directly. |
| `@classmethod` | Receives `cls` instead of `self`; can read/modify class-level state. |
| `@property` | Exposes a method as a read-only attribute; pair with `@<name>.setter` for write access. |
| `@abstractmethod` | (from `abc`) Forces subclasses to implement the method. See [[Python#Class/Method Abstraction]]. |
| `@contextmanager` | (from `contextlib`) Converts a generator into a context manager. See [[Python#Context Manager Protocol]]. |
| `functools.lru_cache` | Caches return values for pure functions (memoization). |
| `functools.wraps` | Preserves the wrapped function's `__name__`, `__doc__`, etc. (best practice inside decorators). |

### @staticmethod example

```python
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y

MathOperations.add(5, 3)  # 8 — no instance needed
```

### @classmethod example

```python
class Employee:
    raise_amount = 1.05

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

Employee.set_raise_amount(1.10)
print(Employee.raise_amount)  # 1.1
```

### @property example

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius cannot be negative")

    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

---

## Chaining Decorators

Multiple decorators are applied **bottom-up** (innermost first), but execute **top-down** at call time.

```python
def decor1(func):       # squares result
    def inner():
        return func() ** 2
    return inner

def decor2(func):       # doubles result
    def inner():
        return func() * 2
    return inner

@decor1
@decor2
def num():
    return 10

# Equivalent to: decor1(decor2(num))
# decor2 runs first → 20, then decor1 squares → 400
print(num())  # 400
```

Order matters: `@A @B` means `A(B(func))`.

---

## Best Practice: functools.wraps

Without `functools.wraps`, the wrapper replaces the decorated function's metadata (`__name__`, `__doc__`).

```python
import functools

def decorator(func):
    @functools.wraps(func)   # preserves func.__name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## Real-World Use Cases

| Pattern | Description |
|---|---|
| **Logging** | Trace function calls, arguments, and return values automatically. |
| **Authentication** | Gate access in web frameworks (Flask `@login_required`, Django). |
| **Caching / Memoization** | `@functools.lru_cache` stores results of expensive pure functions. |
| **Rate Limiting** | Count and throttle API calls per user. |
| **Retry Logic** | Wrap network calls to retry on transient failures (e.g., `tenacity` library). |
| **Timing / Profiling** | Measure and log execution time of functions. |
| **Validation** | Check argument types or values before a function runs. |

---

## Connections
- [[Python]] — first-class functions, `@abstractmethod`, `@contextmanager`
- [[Python#Context Manager Protocol]] — `@contextmanager` is itself a decorator
- [[Closures]] — decorators rely on closures to capture `func` in `wrapper`
