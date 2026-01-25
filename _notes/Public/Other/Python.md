---
title: Python
---
# Managing Environment Variables
[python-dotenv · PyPI](https://pypi.org/project/python-dotenv/)
# REPL
A **Python REPL environment** is an interactive programming tool where you can write and execute Python code line-by-line and immediately see the results. REPL stands for:
- **Read** - accepts your input (Python code)
- **Eval** - evaluates/executes that code
- **Print** - displays the output
- **Loop** - returns to accept more input

# Class/Method Abstraction
Abstract base classes use Python's **abc** module. This serves as a blueprint for class and method implementations, ensuring consistency across subclasses.
Key reasons for abstraction:
- Interface Enforcement: Abstract methods must be implemented by any concrete subclass, preventing incomplete implementations.
- Polymorphism: Allows treating different class instances uniformly (e.g., calling completion() on any object).
- Maintainability: Centralizes the API, making it easier to add new features or modify behavior across all implementations.
- Type Safety: Provides clear type hints for context (list of strings, string, or dict) and return types, aiding IDE support and reducing errors.

**Example Abstraction Class:**
```python
from abc import ABC, abstractmethod

class RLM(ABC):
    @abstractmethod
    def completion(self, context: list[str] | str | dict[str, str], query: str) -> str:
        pass

    @abstractmethod
    def cost_summary(self) -> dict[str, float]:
        pass  

    @abstractmethod
    def reset(self):
        pass
```
*Code from https://github.com/alexzhang13/rlm.*

# \_\_init\_\_.py
In Python, `__init__.py` is a special file that serves two primary purposes within a package:
- **Marking a Directory as a Package:** 
	When a directory contains an `__init__.py` file, Python treats that directory as a package. This allows you to import modules and subpackages from within that directory using standard import statements. Even an empty `__init__.py` file suffices to declare a directory as a package.

- **Package Initialization and Namespace Management:** 
	The code within `__init__.py` is executed automatically the first time the package or any module within it is imported. This allows for:
	- **Initialization Code:** Running setup or configuration code, such as establishing database connections, loading configuration files, or setting up package-level variables.
    - **Simplifying Imports:** Importing specific modules, functions, or classes from submodules directly into the package's namespace. This allows users to import these elements directly from the package instead of needing to specify the submodule.
    - Defining `__all__`: The `__all__` variable (a list of strings) can be defined in `__init__.py` to control which names are imported when a "star import" (`from package import *`) is used. This allows for explicit control over the package's public API.



# Context Manager Protocol (`with` statement)
**Context managers** provide setup/cleanup guarantees using the `with` statement.
## Execution Order

```python
with expression as variable:
    # body
```

1. `expression.__enter__()` runs → returns value bound to `variable`
2. `body` executes
3. `expression.__exit__()` **always** runs (even if exception occurs)
## Implementation: `@contextmanager` Decorator
Converts a generator function into a context manager:

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup code runs first
    resource = setup()
    try:
        yield resource  # ← Pauses; value goes to 'as' variable
        # Execution jumps to 'with' body
    finally:
        cleanup(resource)  # ← Always runs on exit
```

**Usage:**
```python
with my_context() as resource:
    # Use resource here
    ...
# cleanup() called automatically
```

## Why Use a Context Manager?
- **Fail-safe cleanup**: `finally` block guarantees cleanup even on exceptions. Ensure exit code always runs.
- **No decorator needed**: Manual implementation requires `__enter__` and `__exit__` methods

> Without `@contextmanager`
> A generator alone **cannot** be used in a `with` statement, it crashes. The decorator bridges this gap automatically.

```python
def my_gen():
    yield resource  # Just a generator, NOT a context manager

with my_gen():  # ❌ TypeError: object does not support context manager protocol
    pass
```

