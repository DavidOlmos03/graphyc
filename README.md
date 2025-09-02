# Graphyc App

A small, modular Tkinter application to visualize feasible regions of simple
linear constraints (2 variables). The project is organized to be maintainable
and scalable with clear separation between GUI, business logic and solver code.

# Clone this repo
```bash
    git clone https://github.com/DavidOlmos03/graphyc.git
```
## Project structure
```bash
Graphyc/
│── main.py
│── README.md
│── gui/
│ ├── init.py
│ ├── app_window.py
│ └── styles.py
│── core/
│ ├── init.py
│ ├── restrictions.py
│ └── solver.py
```

## Requirements

This project uses only standard Python libraries plus `numpy` and `matplotlib`.

- Python 3.8+
- numpy
- matplotlib
- tkinter (usually included with Python on many systems)

> 1. Install them globally or in a virtual environment:
>    ```bash
>    python -m venv .venv
>    source .venv/bin/activate   # Linux/Mac
>    .venv\Scripts\activate      # Windows
>    pip install -r requirements.txt # Install all necessary dependencies
>    ```

## How to run

From the project root:

```bash
python main.py
or 
python3 main.py
