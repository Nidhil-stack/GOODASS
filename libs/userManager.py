import yaml
import prettytable
import os


def user_print(config = None):
    """Prints a table of users with their emails and associated keys.
     Parameters:
    - config (dict): Configuration dictionary containing user data. If None, it loads from 'config.yaml'.
    """
    if config is None:
        config = load_config()
    users = config.get('users', [])
    user_table = prettytable.PrettyTable()
    user_table.field_names = ["Username", "Email", "Keys"]
    for user in users:
        i = 0
        email = user.get('email', 'N/A')
        username = user.get('name', 'N/A')
        keys_info = user.get('keys', [])
        if not keys_info:
            user_table.add_row([username, email, 'No keys'])
        else:
            for key in keys_info:
                key_type = key.get('type', 'N/A')
                key_value = key.get('key', 'N/A')
                keys = f"{key_type} {key_value[:5]}..."
                if i == 0:
                    user_table.add_row([username, email, keys])
                else:
                    user_table.add_row(['-', '-', keys])
                i += 1
    print(user_table)

def user_add(config, username, email, keys):
    """Adds a new user to the configuration.
    Parameters:
    - config (dict): Configuration dictionary containing user data.
    - username (str): Name of the new user.
    - email (str): Email of the new user.
    - keys (list): List of keys associated with the new user.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    new_user = {
        'name': username,
        'email': email,
        'keys': [{'type': k['type'], 'key': k['key']} for k in keys]
    }
    for user in config.get('users', []):
        if user['email'] == email:
            print(f"User with email {email} already exists.")
            return config
    config.setdefault('users', []).append(new_user)
    print(f"User {username} added successfully.")
    return config

def load_config(path='config.yaml'):
    """Loads the configuration from a YAML file.
    Parameters:
    - path (str): Path to the configuration file.
    Returns:
    - config (dict): Configuration dictionary.
    """
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def save_config(config, path='config.yaml'):
    """Saves the configuration to a YAML file.
    Parameters:
    - config (dict): Configuration dictionary.
    - path (str): Path to the configuration file.
    """
    with open(path, 'w') as f:
        yaml.dump(config, f)

def user_add_cli(config='config.yaml'):
    """CLI for adding a new user.
    Parameters:
    - config (str or dict): Path to the configuration file or configuration dictionary.
    """
    if isinstance(config, str):
        config = load_config(config)
    os.system('cls' if os.name == 'nt' else 'clear')
    user_print(config)
    username = input("Insert new user name: ")
    email = input("Insert new user email: ")
    keys = []
    config = user_add(config, username, email, keys)
    config = user_add_key_cli(config, email=email)
    os.system('cls' if os.name == 'nt' else 'clear')
    user_print(config)
    input("Press Enter to continue...")


def user_add_key(config, email, key):
    """Adds a key to a user in the configuration.
    Parameters:
    - config (dict): Configuration dictionary containing user data.
    - email (str): Email of the user to add the key to.
    - key (str): SSH key string.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    users = config.get('users', [])
    for user in users:
        if user['email'] == email:
            key_type = key.split()[0]
            key_value = key.split()[1]
            key_hostname = key.split()[2] if len(key.split()) > 2 else ''
            key_access = []
            for existing_key in user.get('keys', []):
                if existing_key['key'] == key_value:
                    print(f"Key already exists for user {user['name']}.")
                    return config
            user.setdefault('keys', []).append({'type': key_type, 'key': key_value, 'hostname': key_hostname, 'access': key_access})
            return config
    return config

def user_add_key_cli(config='config.yaml', email=None):
    """CLI for adding keys to a user.
    Parameters:
    - config (str or dict): Path to the configuration file or configuration dictionary.
    - email (str): Email of the user to add keys to.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    if isinstance(config, str):
        config = load_config(config)
    os.system('cls' if os.name == 'nt' else 'clear')
    user_print(config)
    if email is None:
        email = input("Insert user email to add key: ")
    users = config.get('users', [])
    user_exists = False
    for user in users:
        if user['email'] == email:
            user_exists = True
            break
    if not user_exists:
        print(f"User with email {email} does not exist.")
        input("Press Enter to continue...")
        return config    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_print_keys(config, email)
        key = input("Insert key or 'done' to finish: ")
        if key.lower() == 'done':
            break
        try: 
            key_type = key.split()[0]
            key_value = key.split()[1]
            key_hostname = key.split()[2] if len(key.split()) > 2 else ''
            for user in users:
                if user['email'] == email:
                    user.setdefault('keys', []).append({'type': key_type, 'key': key_value, 'hostname': key_hostname})
                    print(f"Key added to user {user['name']}.")
        except IndexError:
            print("Invalid key format. Please enter the key in the format: <type> <key> [hostname]")
    save_config(config)
    return config


def user_remove_key(config, email, key_value):
    """Removes a key from a user in the configuration.
    Parameters:
    - config (dict): Configuration dictionary containing user data.
    - email (str): Email of the user to remove the key from.
    - key_value (str): SSH key string to be removed.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    users = config.get('users', [])
    for user in users:
        if user['email'] == email:
            keys = user.get('keys', [])
            for existing_key in keys:
                if existing_key['key'] == key_value:
                    keys.remove(existing_key)
                    return config
            print(f"Key not found for user {user['name']}.")
            input("Press Enter to continue...")
            return config
    return config

def user_remove_key_cli(config='config.yaml', email=None):
    """CLI for removing keys from a user.
    Parameters:
    - config (str or dict): Path to the configuration file or configuration dictionary.
    - email (str): Email of the user to remove keys from.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    if isinstance(config, str):
        config = load_config(config)
    os.system('cls' if os.name == 'nt' else 'clear')
    if email is None:
        user_print(config)
        email = input("Insert user email to remove key: ")
        os.system('cls' if os.name == 'nt' else 'clear')
    users = config.get('users', [])
    user_exists = False
    for user in users:
        if user['email'] == email:
            user_exists = True
            break
    if not user_exists:
        print(f"User with email {email} does not exist.")
        input("Press Enter to continue...")
        return config
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_print_keys(config, email)
        key_number = input("Insert key number to remove or 'done' to finish: ")
        try:
            key_index = int(key_number) - 1
            users = config.get('users', [])
            for user in users:
                if user['email'] == email:
                    keys = user.get('keys', [])
                    if 0 <= key_index < len(keys):
                        key_value = keys[key_index]['key']
                    else:
                        print("Invalid key number.")
                        continue
        except ValueError:
            if key_number.lower() == 'done':
                break
            print("Invalid input. Please enter a valid key number or 'done'.")
            input("Press Enter to continue...")
            continue
        for user in users:
            if user['email'] == email:
                keys = user.get('keys', [])
                for existing_key in keys:
                    if existing_key['key'] == key_value:
                        keys.remove(existing_key)
                        break
                else:
                    print(f"Key not found for user {user['name']}.")
                    input("Press Enter to continue...")
    save_config(config)


def user_print_keys(config, email):
    """Prints a table of keys for a specific user.
    Parameters:
    - config (dict): Configuration dictionary containing user data.
    - email (str): Email of the user whose keys are to be printed.
    """
    users = config.get('users', [])
    for user in users:
        if user['email'] == email:
            key_table = prettytable.PrettyTable()
            key_table.field_names = ["Number", "Type", "Key", "Hostname"]
            for i, key in enumerate(user.get('keys', []), start=1):
                key_type = key.get('type', 'N/A')
                key_value = key.get('key', 'N/A')
                key_hostname = key.get('hostname', 'N/A')
                key_table.add_row([i, key_type, key_value, key_hostname])
            print(f"Keys for user {user['name']}:")
            print(key_table)
            return
    print(f"User with email {email} does not exist.")


def user_remove(config, email):
    """Removes a user from the configuration.
    Parameters:
    - config (dict): Configuration dictionary containing user data.
    - email (str): Email of the user to remove.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    users = config.get('users', [])
    for user in users:
        if user['email'] == email:
            users.remove(user)
            return config
    return config

def user_remove_cli(config='config.yaml', email=None):
    """CLI for removing a user.
    Parameters:
    - config (str or dict): Path to the configuration file or configuration dictionary.
    - email (str): Email of the user to remove.
    Returns:
    - config (dict): Updated configuration dictionary.
    """
    if isinstance(config, str):
        config = load_config(config)
    if email is None:
        user_print(config)
        email = input("Insert user email to remove: ")
        os.system('cls' if os.name == 'nt' else 'clear')
    users = config.get('users', [])
    user_exists = False
    for user in users:
        if user['email'] == email:
            user_exists = True
            break
    if not user_exists:
        print(f"User with email {email} does not exist.")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        return config
    config = user_remove(config, email)
    user_print(config)
    print(f"User with email {email} removed successfully.")
    save_config(config)
    input("Press Enter to continue...")
    return config
