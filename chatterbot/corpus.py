import io
from pathlib import Path
from dataclasses import dataclass
from typing import List, Generator

from chatterbot.exceptions import OptionalDependencyImportError

# Try to import ChatterBot corpus data directory
try:
    from chatterbot_corpus.corpus import DATA_DIRECTORY
except (ImportError, ModuleNotFoundError):
    # Default to home directory if corpus package not installed
    DATA_DIRECTORY = Path.home() / 'chatterbot_corpus' / 'data'

# Only support YAML formats for now
CORPUS_EXTENSIONS = ['yml', 'yaml']

# Simple cache for loaded corpus files
_corpus_cache = {}


@dataclass
class CorpusData:
    conversations: List[List[str]]
    categories: List[str]
    file_path: str


def get_file_path(dotted_path: str, extensions: List[str] = CORPUS_EXTENSIONS) -> Path:
    """
    Convert a dotted path or filesystem path into an actual file path.
    Raises FileNotFoundError if the file does not exist.
    """
    path = Path(dotted_path)

    # If path already exists, return it
    if path.exists():
        return path

    # Split dotted path
    parts = dotted_path.split('.')
    if parts[0] == 'chatterbot':
        parts[0] = str(DATA_DIRECTORY)

    base_path = Path(*parts)

    # Check for file existence with supported extensions
    for ext in extensions:
        candidate = base_path.with_suffix(f'.{ext}')
        if candidate.exists():
            return candidate

    # If directory exists, return it
    if base_path.is_dir():
        return base_path

    raise FileNotFoundError(f"Corpus file or directory not found for: {dotted_path}")


def read_corpus(file_path: Path) -> dict:
    """
    Read a YAML corpus file and return its contents.
    Caches results for repeated access.
    """
    if file_path in _corpus_cache:
        return _corpus_cache[file_path]

    try:
        import yaml
    except ImportError:
        message = (
            'Unable to import "yaml".\n'
            'Please install "pyyaml" to enable chatterbot corpus functionality:\n'
            'pip install pyyaml'
        )
        raise OptionalDependencyImportError(message)

    try:
        with io.open(file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read corpus file {file_path}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError(f"Corpus file {file_path} did not return a dictionary.")

    _corpus_cache[file_path] = data
    return data


def list_corpus_files(dotted_path: str) -> List[Path]:
    """
    Return a sorted list of all corpus files (with supported extensions)
    in the given dotted path or directory.
    """
    path = get_file_path(dotted_path)
    files: List[Path] = []

    if path.is_dir():
        for ext in CORPUS_EXTENSIONS:
            files.extend(path.rglob(f'*.{ext}'))
    else:
        files.append(path)

    return sorted(files)


def load_corpus(*data_file_paths: str) -> Generator[CorpusData, None, None]:
    """
    Yield CorpusData objects for each specified corpus file.
    """
    for file_path_str in data_file_paths:
        path = get_file_path(file_path_str)
        if path.is_dir():
            files = list_corpus_files(path)
        else:
            files = [path]

        for file in files:
            corpus_data = read_corpus(file)
            conversations = corpus_data.get('conversations', [])
            categories = corpus_data.get('categories', [])
            yield CorpusData(conversations, categories, str(file))
