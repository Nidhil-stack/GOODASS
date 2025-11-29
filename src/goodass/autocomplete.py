"""Autocomplete utilities for goodass CLI.

This module provides tab-completion functionality for various input types
including file paths, host selections, and user selections.
"""

import os
import glob

# Try to import readline, which is not available on Windows by default
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False


def setup_readline():
    """Initialize readline with tab completion settings.
    
    On Windows without readline, this function does nothing.
    """
    if not READLINE_AVAILABLE:
        return
    # Enable tab completion
    readline.parse_and_bind("tab: complete")
    # Set completer delimiters (don't break on these characters)
    readline.set_completer_delims(' \t\n;')


def path_completer(text, state):
    """Complete file system paths.
    
    Parameters:
    - text (str): The current text being completed.
    - state (int): The state of completion (0 for first match, increments for each subsequent match).
    
    Returns:
    - str or None: The next matching path, or None if no more matches.
    """
    # Expand ~ to home directory
    if text.startswith('~'):
        text = os.path.expanduser(text)
    
    # Handle empty input or current directory
    if not text:
        text = './'
    
    # Get matching paths
    if os.path.isdir(text) and not text.endswith('/'):
        # If text is a directory without trailing slash, add it
        pattern = text + '/*'
    else:
        pattern = text + '*'
    
    matches = glob.glob(pattern)
    
    # Add trailing slash for directories
    matches = [m + '/' if os.path.isdir(m) else m for m in matches]
    
    # Sort matches
    matches.sort()
    
    try:
        return matches[state]
    except IndexError:
        return None


def create_list_completer(options):
    """Create a completer function for a list of options.
    
    Parameters:
    - options (list): List of string options to complete from.
    
    Returns:
    - function: A completer function that matches against the provided options.
    """
    def completer(text, state):
        """Complete from the list of options.
        
        Parameters:
        - text (str): The current text being completed.
        - state (int): The state of completion.
        
        Returns:
        - str or None: The next matching option, or None if no more matches.
        """
        # Filter options that start with the current text (case-insensitive)
        text_lower = text.lower()
        matches = [opt for opt in options if opt.lower().startswith(text_lower)]
        matches.sort()
        
        try:
            return matches[state]
        except IndexError:
            return None
    
    return completer


def input_with_path_completion(prompt):
    """Get user input with file path tab completion.
    
    Parameters:
    - prompt (str): The prompt to display to the user.
    
    Returns:
    - str: The user's input.
    
    Note:
        On Windows without readline, falls back to standard input without completion.
    """
    if not READLINE_AVAILABLE:
        user_input = input(prompt)
        if user_input.startswith('~'):
            user_input = os.path.expanduser(user_input)
        return user_input
    
    setup_readline()
    old_completer = readline.get_completer()
    readline.set_completer(path_completer)
    
    try:
        user_input = input(prompt)
        # Expand ~ in the result
        if user_input.startswith('~'):
            user_input = os.path.expanduser(user_input)
        return user_input
    finally:
        readline.set_completer(old_completer)


def input_with_list_completion(prompt, options):
    """Get user input with tab completion from a list of options.
    
    Parameters:
    - prompt (str): The prompt to display to the user.
    - options (list): List of string options for tab completion.
    
    Returns:
    - str: The user's input.
    
    Note:
        On Windows without readline, falls back to standard input without completion.
    """
    if not READLINE_AVAILABLE:
        return input(prompt)
    
    setup_readline()
    old_completer = readline.get_completer()
    completer = create_list_completer(options)
    readline.set_completer(completer)
    
    try:
        return input(prompt)
    finally:
        readline.set_completer(old_completer)


def disable_completion():
    """Disable tab completion.
    
    On Windows without readline, this function does nothing.
    """
    if READLINE_AVAILABLE:
        readline.set_completer(None)
