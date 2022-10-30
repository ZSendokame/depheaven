from pkg_resources import get_distribution, DistributionNotFound
import os
import ast

import arguing
import classify_imports


class Import(ast.NodeVisitor):

    def __init__(self):
        self.packages = []

    def visit_Import(self, node):
        if node.__class__.__name__ == 'Import':
            package = node.names[0].name

            self.packages.append(package)

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.packages.append(node.module)
        self.generic_visit(node)


def main():
    added = 0
    file = arguing.set('--file', mandatory=True)
    output = arguing.set('--output', default='requirements.txt')

    # Check file.
    if not os.path.exists(file):
        exit(f'- "{file}" does not exists.')

    # Main:
    with open(file, 'r') as file:
        parsed = ast.parse(file.read())

    output_file = open(output, 'w')
    visitor = Import()

    visitor.visit_Import(parsed)

    for package in visitor.packages:
        if classify_imports.classify_base(package) == 'THIRD_PARTY':
            try:
                version = get_distribution(package)
                added += 1

                output_file.write(f'{package}=={version.version}\n')

            except DistributionNotFound:
                pass

    print(f'+ {len(visitor.packages)} packages, {added} added to {output}.')


if __name__ == '__main__':
    main()
