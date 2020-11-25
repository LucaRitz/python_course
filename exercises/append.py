from typing import List, Dict


def append(file_one: str, file_two: str, file_target: str) -> None:
    with File([file_one, file_two], file_target) as handle:
        value_1: str = handle.read(file_one)
        value_2: str = handle.read(file_two)
        handle.write(value_1 + value_2)


def read(file: str) -> str:
    val: str
    with File([file]) as handle:
        val = handle.read(file)
    return val


class File:

    class FileHandle:

        def __init__(self, files: Dict[str, any], target_file=None) -> None:
            self.files = files
            self.target_file = target_file

        def read(self, inx: str) -> str:
            return self.files[inx].read()

        def write(self, value: str) -> None:
            if self.target_file is not None:
                self.target_file.write(value)

        def close(self):
            for file in self.files.values():
                file.close()
            if self.target_file is not None:
                self.target_file.close()

    def __init__(self, files_str: List[str], target_file: str=None) -> None:
        files = {f: open(f, 'r') for f in files_str}

        self.current_file_handle = File.FileHandle(files, open(target_file, 'w') if target_file is not None else None)

    def __enter__(self) -> FileHandle:
        return self.current_file_handle

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.current_file_handle.close()
