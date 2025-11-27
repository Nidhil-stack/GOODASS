# Global Oversight Of Deployed Authorized SSH Settings

# Install and first configuration
To install the package use pip (e.g. "pip install download_directory/dist/goodass[...].whl
The only thing to add is a yaml file called "settings.yaml" in the folder "goodass" that's found in ~/.config on Unix systems, appdata in Windows and somewhere else in MacOs, with the content "ssh_private_key_path: [your key path]"
Optionally you can provide your own config file, to skip setting it up from the wizard, in the same folder. An example file will be provided in future releases.

Typical workflow
- verify ssh connectivity to each host
- run 'goodass'
- use the wizard to add hosts, users and keys
- use the wizard to launch the "fix keys" utility, that will sync your configuration to all added hosts

Key management notes
- Do not commit private keys to the repository.
- Store private keys in a secure location and restrict permissions (`chmod 600`).
- Public keys can be included in the configuration for distribution.

Security
- Never include passwords or private keys in `config.yaml` or commit them to source control.
- Use an SSH agent or local file paths with restrictive permissions to prevent accidental exposure.
- Verify remote user permissions and the SSH policies on destination servers before mass-distribution.

Development & testing
- To test the program in developement you can launch "cli.py" from the src/goodass/ directory
- Test locally using a config that targets test VMs or containers.

Contributing
- Report bugs by opening an issue on GitHub with reproduction steps.
- Submit improvements via pull requests with focused changes and a clear description.
- Keep changes minimal and include tests for new functionality where possible.

Roadmap / TODO
- Add non interactive mode for automation
- Add a small TUI for quick configuration (?)
- Add the possibility to sync config.yaml with a remote server via sftp, to allow multiple users to edit it

License
This project is released under the license included in the repository (see `LICENSE`).

Contact
- **Author:** `Nidhil-stack`
- **Contributors:**

  <a href="https://github.com/EddyDevProject"><img src="https://github.com/EddyDevProject.png" width="60px"/><br /></a>

---
