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
        package = package.split('.')
        name = package[0]
        classification = classify_imports.classify_base(name)

        if classification == 'THIRD_PARTY' and len(package) == 1:
            try:
                version = get_distribution(name)

                output_file.write(f'{name}=={version.version}\n')

            except DistributionNotFound:
                output_file.write(f'{name}\n')

            added += 1

    print(f'+ {len(visitor.packages)} packages, {added} added to {output}.')


if __name__ == '__main__':
    main()
