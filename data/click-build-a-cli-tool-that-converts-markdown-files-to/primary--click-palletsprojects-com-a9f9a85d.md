---
library: "click"
query: "Build a CLI tool that converts markdown files to styled PDFs with a table of contents. Use markdown for the markdown parser. Use weasyprint for the pdf generator. Use click for the cli framework."
url: "https://click.palletsprojects.com/"
resolved_url: "https://click.palletsprojects.com/en/stable/"
role: "primary"
rank: 0
fetched_at: "2026-08-21T07:20:24.982519+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "bc4c06368c38f0cec9814b2691ad20c67801b3e516bd229a108b9166c3539024"
---

# Welcome to Click

 [![_images/click-name.svg](_images/click-name.svg)](_images/click-name.svg)

Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary. It’s the “Command Line Interface Creation Kit”. It’s highly configurable but comes with sensible defaults out of the box.

It aims to make the process of writing command line tools quick and fun while also preventing any frustration caused by the inability to implement an intended CLI API.

Click in three points:

* arbitrary nesting of commands
* automatic help page generation
* supports lazy loading of subcommands at runtime

What does it look like? Here is an example of a simple Click program:

```
import click

@click.command()@click.option('--count', default=1, help='Number of greetings.')@click.option('--name', prompt='Your name',
              help='The person to greet.')def hello(count, name):    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    hello()
```

And what it looks like when run:

```
$ python hello.py --count=3Your name: JohnHello John!Hello John!Hello John!
```

It automatically generates nicely formatted help pages:

```
$ python hello.py --helpUsage: hello.py [OPTIONS]

  Simple program that greets NAME for a total of COUNT times.

Options:  --count INTEGER  Number of greetings.  --name TEXT      The person to greet.  --help           Show this message and exit.
```

You can get the library directly from PyPI:

```
pip install click
```

# Documentation

## Tutorials

## How to Guides

## Conceptual Guides

## General Reference

## API Reference

# About Project

* This documentation is structured according to [Diataxis](https://diataxis.fr/) and written with [MyST](https://myst-parser.readthedocs.io/en/latest/)
* [Version Policy](https://palletsprojects.com/versions)
* [Donate](https://palletsprojects.com/donate)
