from pathlib import Path

# Address of the daemon
host, port = address = ('localhost', 1337)

# Whether to enable Anki integration
anki_integration = True
anki_save_location = Path('~').expanduser()

# Whether to show confirmation after adding words to Anki
show_confirmation = False
