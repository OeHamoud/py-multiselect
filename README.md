# Py-Multiselect

A lightweight, dependency-free terminal multiselect menu for Python with keyboard navigation and checkbox-style selection.

## Features

* Arrow key and vim-style navigation (`j/k`)
* Toggle selections with space
* Select all / toggle all support
* Optional selection limits
* Mutually exclusive option groups
* No external dependencies

## Usage

```python
from multiselect import multiselect

options = ["Apple", "Banana", "Cherry", "Date"]

selected = multiselect(options)

print(selected)
```

## Controls

* `↑ / k` : move up
* `↓ / j` : move down
* `space` : toggle selection
* `a` : select/deselect all
* `enter` : confirm selection
* `q` : quit (returns empty list)

## Function Signature

```python
multiselect(
    options,
    preselected=None,
    max_select=0,
    groups=None
)
```

### Parameters

* `options` (list[str]) – Items to display
* `preselected` (list[int]) – Indices pre-checked
* `max_select` (int) – Max selectable items (0 = unlimited)
* `groups` (list[list[int]]) – Mutually exclusive index groups

## Example

```python
options = ["Option A", "Option B", "Option C", "Option D"]

selected = multiselect(
    options,
    preselected=[1],
    max_select=2,
    groups=[[0, 1]]
)

print(selected)
```

## Notes

* Works only in terminal environments
* Uses ANSI escape sequences for rendering
* Designed for Unix-like systems (Linux/macOS)
