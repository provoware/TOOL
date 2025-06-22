# SongArchiv Release v4.0.3-r3

## Accessibility

This release improves accessibility following common WCAG guidelines:

- High contrast theme with large default fonts.
- All controls are reachable via keyboard.
- Optional speech output is available if `pyttsx3` can initialize.

## Usage

1. Install the dependencies from `requirements.txt` using `pip install -r requirements.txt`.
2. Run `python main.py` to start the GUI. The required databases will be created automatically in the `db` folder on first start.

## Running the tests

Execute `pytest` to run the unit tests contained in the `tests` folder.
