# yaml_manager

A Python CLI tool to create, edit, and remove YAML files using PyYAML.

## Features

- Create a new YAML file
- Remove a YAML file
- Edit YAML file properties (set or remove)
- Supports array values (comma separated)

## Usage

Create a new YAML file:

```bash
python cli.py create --file path/to/file.yaml
```

Remove a YAML file:

```bash
python cli.py remove --file path/to/file.yaml
```

Create a backup of a YAML file:

```bash
python cli.py backup --file path/to/file.yaml
```

Set a property:

```bash
python cli.py edit --file path/to/file.yaml --action set --property foo --value bar
```

Set an array property:

```bash
python cli.py edit --file path/to/file.yaml --action set --property arr --value a,b,c
```

Remove a property:

```bash
python cli.py edit --file path/to/file.yaml --action remove --property foo
```

## Requirements

- Python 3.8+
- PyYAML (installed automatically with uv)

## License

MIT
