import argparse
import yaml
import os
import sys


def create_yaml(file_path):
    if os.path.exists(file_path):
        print(f"File {file_path} already exists.")
        sys.exit(1)
    parent_dir = os.path.dirname(file_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    with open(file_path, 'w') as f:
        yaml.dump({}, f)
    print(f"Created YAML file: {file_path}")

def remove_yaml(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed YAML file: {file_path}")
    else:
        print(f"File {file_path} does not exist.")


from datetime import datetime

def load_yaml(file_path):
    changelog = []
    data = {}
    if not os.path.exists(file_path):
        return changelog, data
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                changelog.append(line.rstrip())
            else:
                break
        yaml_text = ''.join([line for line in lines if not line.startswith('#')])
        data = yaml.safe_load(yaml_text) or {}
    return changelog, data


def save_yaml(data, file_path, changelog):
    with open(file_path, 'w') as f:
        for entry in changelog:
            f.write(entry + '\n')
        yaml.dump(data, f)

def set_property(data, prop, value):
    # If value contains commas, treat as list
    if ',' in value:
        data[prop] = [v.strip() for v in value.split(',')]
    else:
        data[prop] = value
    return data

def remove_property(data, prop):
    if prop in data:
        del data[prop]
    return data


import shutil

def backup_yaml(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)
    backup_path = file_path + ".bak"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")


def main():
    parser = argparse.ArgumentParser(description="Manage YAML files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new YAML file")
    create_parser.add_argument("--file", required=True, help="Path to YAML file")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a YAML file")
    remove_parser.add_argument("--file", required=True, help="Path to YAML file")

    # edit command
    edit_parser = subparsers.add_parser("edit", help="Edit a YAML file")
    edit_parser.add_argument("--file", required=True, help="Path to YAML file")
    edit_parser.add_argument("--action", choices=["set", "remove"], required=True, help="Edit action")
    edit_parser.add_argument("--property", required=True, help="Property name")
    edit_parser.add_argument("--value", help="Value to set (comma separated for arrays)")

    # backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup of a YAML file")
    backup_parser.add_argument("--file", required=True, help="Path to YAML file")

    args = parser.parse_args()

    if args.command == "create":
        create_yaml(args.file)
    elif args.command == "remove":
        remove_yaml(args.file)
    elif args.command == "edit":
        changelog, data = load_yaml(args.file)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if args.action == "set":
            if args.value is None:
                print("Value required for set action")
                sys.exit(1)
            old_value = data.get(args.property, None)
            data = set_property(data, args.property, args.value)
            if old_value is not None:
                changelog.insert(0, f"# [{timestamp}] set {args.property} {old_value} -> {data[args.property]}")
            else:
                changelog.insert(0, f"# [{timestamp}] set {args.property} {data[args.property]}")
            save_yaml(data, args.file, changelog)
            print(f"Set {args.property} to {data[args.property]} in {args.file}")
        elif args.action == "remove":
            old_value = data.get(args.property, None)
            data = remove_property(data, args.property)
            changelog.insert(0, f"# [{timestamp}] remove {args.property}{' ' + str(old_value) if old_value is not None else ''}")
            save_yaml(data, args.file, changelog)
            print(f"Removed {args.property} from {args.file}")
    elif args.command == "backup":
        backup_yaml(args.file)

if __name__ == "__main__":
    main()
