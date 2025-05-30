# Tetrika Test Task

This repository contains the solution for the Tetrika test task.

## Task 1
Implement a decorator `@strict`.  
The decorator must verify that the types of arguments passed to the function match the types declared in the function's prototype.  
*(Hint: Argument type annotations can be accessed via the function's `func.__annotations__` attribute or the `inspect` module.)*  
If a type mismatch is detected, raise a `TypeError`.  

**Guaranteed conditions:**  
1. Parameters in decorated functions will only be of these types: `bool`, `int`, `float`, `str`.  
2. Decorated functions will **not** have default parameter values.

### Example Usage:
```python
def strict(func):
    ...


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
```

## Task 2
Implement a script that retrieves a list of all animals from the Russian Wikipedia page 'Категория:Животные_по_алфавиту' (https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту) and writes to a file named `beasts.csv` the count of animals for each letter of the alphabet. The content of the resulting file should be:

```
А,642
Б,412
В,...
```

Note:

No text analysis is required; every entry in the category counts (an entry may not only be an animal name but also, for example, a genus).

## Task 3
When a user opens the lesson page, we save the time they entered. When the user leaves the lesson (or closes the tab, the browser—in general, in any way breaks the connection to the server), we record the time they exited the lesson. The time each user spends on the lesson is stored by us as intervals. The function receives a dictionary containing three lists of timestamps (time in seconds):

* **lesson** – start and end of the lesson
* **pupil** – intervals of the pupil’s presence
* **tutor** – intervals of the tutor’s presence

Intervals are structured as follows: they are always a list with an even number of elements. At even indices (starting from 0) is the time of entering the lesson; at odd indices is the time of exiting the lesson.

You need to write a function `appearance` that takes as input a dictionary of intervals and returns the total time (in seconds) that the pupil and the tutor were both present in the lesson.

```python
def appearance(intervals: dict[str, list[int]]) -> int:
    pass

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
```

## Setup and Running

1. **Clone the repository**
   ```bash
   git clone https://github.com/NatsionalnoeDostoyanie/tetrika_test_task.git
   cd tetrika_test_task
   ```

   **Rename [`.env.template`](.env.template)** to `.env`, configure it if you want.

2. **Install dependencies**

    **If you use `uv`:**
    ```bash
    make install-base

    # Or:
    uv sync --no-dev
    ```

    **If you use `pip`:**
    ```bash
    # Create a virtual environment:
    python -m venv .venv

    # Linux:
    source .venv/bin/activate
    # Windows:
    .venv\Scripts\activate

    # Install dependencies:
    pip install aiohttp==3.12.4 python-dotenv==1.1.0 wikipedia-api==0.8.1
    ```

3. **Run solutions**

   **If you use `uv`:**
    ```bash
    make run-task1
    make run-task2
    make run-task3

    # Or:
    cd src/task1 && uv run --no-sync python solution.py
    cd src/task2 && uv run --no-sync python solution.py
    cd src/task3 && uv run --no-sync python solution.py
    ```

    **If you use `pip`:**
    ```bash
    python src/task1/solution.py
    python src/task2/solution.py
    python src/task3/solution.py
    ```
