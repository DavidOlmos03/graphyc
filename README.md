# MetodoGraficoApp

A small, modular Tkinter application to visualize feasible regions of simple
linear constraints (2 variables). The project is organized to be maintainable
and scalable with clear separation between GUI, business logic and solver code.

> Documentation and inline docstrings are in English. Follow PEP8 for style.

## Project structure

MetodoGraficoApp/
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


## Requirements

This project uses only standard Python libraries plus `numpy` and `matplotlib`.

- Python 3.8+
- numpy
- matplotlib
- tkinter (usually included with Python on many systems)

> You mentioned you do not want to install libraries locally. If `numpy` or
> `matplotlib` are not available on your system, there are two options:
>
> 1. Install them globally or in a virtual environment:
>    ```bash
>    python -m venv .venv
>    source .venv/bin/activate   # Linux/Mac
>    .venv\Scripts\activate      # Windows
>    pip install -r requirements.txt # Install all necessary dependencies
>    ```
>
> 2. Use a Python distribution that already includes scientific packages
>    (for example Anaconda / Miniconda). This avoids installing packages in
>    your project directory.

## How to run

From the project root:

```bash
python main.py

