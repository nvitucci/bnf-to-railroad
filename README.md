# BNF to Railroad Diagrams

This command-line tool is intended to process BNF-based grammar files to both make them publishable as Asciidoc file and to generate SVG railroad diagrams from them.

## Prepare the environment

```shell
python -m venv venv

source venv/bin/activate

python -m pip install -r requirements.txt
```

## Format of the customization file

The customization file contains:

1. A `links` array where each element has a `symbol` (the grammar symbol to add a link to) and a `link` (the link to associate to the symbol).

```json
{
  "links": [
    {"symbol": "<identifier>", "link": "https://www.example.com/identifier"},
    {"symbol": "<path pattern>", "link": "https://www.example.com/identifier/#pattern"}
  ]
}
```

## Run the program

### Create the processed grammar snippet

```shell
python cli.py process /path/to/source/file.bnf /path/to/asciidoc/examples/file.bnf
```

With a customization file:

```shell
python cli.py process /path/to/source/file.bnf /path/to/asciidoc/examples/file.bnf --customization-file customization.json
```

### Create the railroad diagram

```shell
python cli.py gen-diagrams /path/to/source/file.bnf /path/to/railroad/diagram.svg
```

You can run this with a customization file as for the `process` command, but if you want to use links you need to add `--allow-links` as well.

There are two reasons for this:
1. External links within an SVG file are not useful if the file is not included as an interactive image.
2. Even if links are included, their behaviour on click might not be ideal.

### Check the diff between two grammar files

```shell
python cli.py diff /path/to/source/file.bnf /path/to/asciidoc/examples/file.bnf
```

With a customization file:

```shell
python cli.py diff /path/to/source/file.bnf /path/to/asciidoc/examples/file.bnf --customization-file customization.json
```

It is important to add customizations on both the source and the destination file for the diff to make sense.
