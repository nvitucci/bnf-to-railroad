import json
import re
import sys
from difflib import unified_diff

import click

import diagrams


@click.group()
def cli():
    pass


@cli.command(help="Check the diff between two files")
@click.argument("source-file", type=click.File("r"))
@click.argument("dest-file", type=click.File("r"))
@click.option("--customization-file", type=click.File("r"))
def diff(source_file, dest_file, customization_file):
    source = source_file.read()
    dest = dest_file.read()

    if customization_file is not None:
        customizations = json.load(customization_file)
        for link in customizations["links"]:
            source = source.replace(f'{link["symbol"]}', f'link:{link["link"]}[{link["symbol"]}]')

    num_changes = 0

    for change in unified_diff(source.split("\n"), dest.split("\n")):
        change = change.strip("\n")
        num_changes += 1

        if change.startswith("-") and not change.startswith("---"):
            click.echo(click.style(change, fg="red"))
        elif change.startswith("+") and not change.startswith("+++"):
            click.echo(click.style(change, fg="green"))
        else:
            click.echo(change)

    if num_changes > 0:
        sys.exit(1)
    else:
        sys.exit(0)


@cli.command(help="Generate railroad diagrams from a grammar file")
@click.argument("grammar-file", type=click.File("r"))
@click.argument("result-svg", type=click.File("w"))
@click.option("--customization-file", type=click.File("r"))
@click.option("--allow-links", is_flag=True)
@click.option("--check", is_flag=True)
def gen_diagrams(grammar_file, result_svg, customization_file, allow_links):
    bnf = grammar_file.read()
    links = {}

    if customization_file is not None:
        customizations = json.load(customization_file)

        if allow_links:
            links = {link["symbol"].strip("<").strip(">"): link["link"] for link in customizations["links"]}
        else:
            click.echo(click.style("Links are not allowed in the railroad diagram.\nUse --allow-links if you want to allow them.", fg="yellow"))

    diag = diagrams.Diagrams(bnf, links)
    svg = diag.get_svg()

    result_svg.write(svg)


@cli.command(help="Process a grammar file for Asciidoc rendering")
@click.argument("grammar-file", type=click.File("r"))
@click.argument("processed-grammar-file", type=click.File("w"))
@click.option("--customization-file", type=click.File("r"))
def process(grammar_file, processed_grammar_file, customization_file):
    grammar = grammar_file.read()

    # Remove Markdown-style heading
    grammar = re.sub("^# .+?\n\n?", "", grammar)

    if customization_file is not None:
        customizations = json.load(customization_file)
        for link in customizations["links"]:
            grammar = grammar.replace(f'{link["symbol"]}', f'link:{link["link"]}[{link["symbol"]}]')

    processed_grammar_file.write(grammar)

if __name__ == "__main__":
    cli()
