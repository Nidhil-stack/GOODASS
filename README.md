## 🔐 Global Oversight Of Deployed Authorized SSH Settings

This document provides installation instructions and operational guidelines for managing SSH authorized keys across multiple hosts.

-----

## ⚙️ Installation and First Configuration

### 📥 Installation

Install the package using **pip** from the provided Wheel file:

```bash
pip install download_directory/dist/goodass[...].whl
```

### 🛠️ Configuration File Setup

The primary configuration requires creating a **`settings.yaml`** file containing the path to your SSH private key.

| Operating System | Absolute Configuration Path |
| :--- | :--- |
| **Linux/Unix** | `~/.config/goodass/settings.yaml` |
| **Windows** | `%APPDATA%\goodass\settings.yaml` |
| **macOS** | `~/Library/Application Support/goodass/settings.yaml` |

The content of the `settings.yaml` file must be:

```yaml
ssh_private_key_path: /absolute/path/to/your/key
```

> **Note:** Replace `/absolute/path/to/your/key` with the actual, absolute path of your SSH private key file.

### 📝 Optional Configuration

You can optionally provide a full configuration file, **`config.yaml`**, in the same directory to skip the initial setup wizard. An example file will be provided in future releases.

-----

## 🚀 Typical Workflow

1.  **Verify Connectivity:** Ensure SSH connectivity is working for all target hosts.
2.  **Run Program:** Execute the main command:
    ```bash
    goodass
    ```
3.  **Initial Setup (Wizard):** Use the interactive wizard to add **hosts**, **users**, and associated **keys**.
4.  **Launch Key Fix Utility:** Use the wizard to launch the **"fix keys" utility**, which synchronizes your configured keys to the `authorized_keys` file on all added hosts.

-----

## 🔑 Key Management Notes

  * **Private Keys:** **Do not** commit private keys to the source code repository. Store them in a secure location.
  * **Permissions:** Restrict access to private keys using strict file permissions (e.g., `chmod 600 /path/to/private/key`).
  * **Public Keys:** Public keys can be safely included in the **`config.yaml`** for distribution.

-----

## 🛡️ Security Best Practices

  * **Sensitive Data:** **Never** include passwords or private keys directly in **`config.yaml`** or commit them to source control.
  * **Agent Usage:** Utilize an **SSH agent** or rely on the local file paths with restrictive permissions defined in **`settings.yaml`** to prevent accidental exposure.
  * **Pre-Distribution Checks:** Before mass-distributing keys, verify the remote user permissions and the existing SSH policies (`sshd_config`) on the destination servers.

-----

## 🧑‍💻 Development & Testing

  * **Execution:** To run the program during development, launch the entry point script directly:
    ```bash
    python src/goodass/cli.py
    ```
  * **Local Testing:** Test the program locally using a configuration that targets dedicated **test VMs** or **containers** to avoid impacting production systems.

-----

## 🤝 Contributing

  * **Bug Reporting:** Report bugs by opening an issue on **GitHub** and providing clear steps to reproduce the problem.
  * **Improvements:** Submit improvements via **pull requests**. Ensure changes are focused, clearly described, and include tests for new functionality where possible.

-----

## 🗺️ Roadmap / TODO

  * Implement a **non-interactive mode** for automated scripting.
  * Consider adding a small **Text User Interface (TUI)** for quick configuration.
  * Add functionality to synchronize **`config.yaml`** with a remote server via **SFTP**, enabling configuration collaboration among multiple users.

-----

## ⚖️ License

This project is released under the license included in the repository. See the **`LICENSE`** file for details.

-----

## 📧 Contact

  * **Author:** `Nidhil-stack`
  * **Contributors:** 
  <a href="https://github.com/EddyDevProject"><img src="https://github.com/EddyDevProject.png" width="60px"/><br /></a>
