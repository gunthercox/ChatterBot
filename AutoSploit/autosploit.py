from autosploit.main import main
from lib.output import error


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        error("user aborted session")
