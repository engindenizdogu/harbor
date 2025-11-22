---
title: How to Create Your Own CLI
---
# How to Create Your Own CLI
Main approaches and tools for building CLI applications:

**Python CLI Frameworks:**
- **Click** - Decorator-based, very popular and intuitive
- **Typer** - Built on Click, adds type hints for better IDE support
- **argparse** - Built into Python standard library
- **rich** - For beautiful terminal formatting and progress bars
- **textual** - For building full terminal user interfaces

**JavaScript/TypeScript CLI Frameworks:**
- **Commander.js** - Feature-rich, widely used
- **yargs** - Powerful argument parsing
- **oclif** - Professional CLI framework by Heroku
- **Inquirer.js** - For interactive prompts
- **chalk** - For colored output

**Basic Python CLI Example with Click:**
```python
import click

@click.command()
@click.option('--name', prompt='Your name', help='The person to greet')
@click.option('--count', default=1, help='Number of greetings')
def hello(name, count):
    """Simple CLI that greets NAME COUNT times."""
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

**Basic TypeScript CLI Example with Commander:**
```javascript
import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .description('CLI description')
  .version('1.0.0');

program
  .command('greet')
  .description('Greet someone')
  .argument('<name>', 'person to greet')
  .option('-c, --count <number>', 'number of times', '1')
  .action((name, options) => {
    for (let i = 0; i < parseInt(options.count); i++) {
      console.log(`Hello ${name}!`);
    }
  });

program.parse();
```