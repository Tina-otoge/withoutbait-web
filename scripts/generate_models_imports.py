#!/usr/bin/env python

"""
This script allows the generation of the __init__.py file for the models module,
as it only consists of importing each model from each file for cleaner import
statements and proper type-hinting in code editors, writing it by hand can be
tedious and repetitive
"""

from pathlib import Path


path = Path('./app/db/models/')
target = path / '__init__.py'

def main():
    target.unlink(missing_ok=True)

    files = {}
    for file in path.rglob('*.py'):
        classes = set()
        for line in file.read_text().splitlines():
            if line.startswith('class'):
                classes.add(line.split()[1].split('(')[0])
        if classes:
            files[file.stem] = classes
    print('Detected', files)

    text = '\n'.join(
        f'from .{file} import {", ".join(classes)}'
        for file, classes in files.items()
    )
    n = target.write_text(text)
    print('Wrote', n, 'bytes to', target)


if __name__ == '__main__':
    main()
