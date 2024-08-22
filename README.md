# 💬 Prompt Generator

Welcome to the Prompt Generator! This Streamlit application allows users to generate customized prompts for ChatGPT (GPT-3, GPT-4) and other similar models. The app provides a user-friendly interface to input parameters and generate detailed prompts based on user specifications.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Creators](#creators)

## Features

- Generate custom prompts for ChatGPT.
- Set model parameters such as temperature and maximum length.
- Input fields for persona, task, and format.
- Reset session state to clear inputs.
- Sidebar with model details and creator information.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/WilliamSMendes/prompt-generator.git
    cd prompt-generator
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up your environment variables:**

    Create a `.streamlit/secrets.toml` file in the root directory of your project and add your MISTRAL API key:
    ```toml
    [general]
    MISTRAL_API_KEY = "your_api_key_here"
    ```

## Usage

To start the Streamlit application, run:
```sh
streamlit run main.py
```

This will launch the application in your default web browser.

## Configuration

The application uses the Streamlit secrets management system to securely manage your API key. Ensure your `MISTRAL_API_KEY` is set in the `.streamlit/secrets.toml` file.

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for details on how to get started.

### Reporting Bugs

If you find a bug, please open an issue with the following details:

- A clear and descriptive title.
- A detailed description of the problem.
- Steps to reproduce the issue.
- Any relevant logs, screenshots, or error messages.

### Suggesting Enhancements

If you have an idea for an enhancement, please open an issue with:

- A clear and descriptive title.
- A detailed description of the enhancement.
- The reasons why this enhancement would be useful.
- Any relevant examples or mockups.

### Submitting Pull Requests

If you want to contribute code, please follow these steps:

1. **Fork the repository:**
   Click on the "Fork" button at the top of the repository page to create a copy of the repository in your GitHub account.

2. **Clone your fork:**
    ```sh
    git clone https://github.com/yourusername/prompt-generator.git
    cd prompt-generator
    ```

3. **Create a branch:**
    ```sh
    git checkout -b feature/your-feature-name
    ```

4. **Make changes:**
   Make your changes in the new branch. Ensure your code follows the project's coding standards.

5. **Commit changes:**
    ```sh
    git add .
    git commit -m "Add a concise commit message describing your changes"
    ```

6. **Push changes:**
    ```sh
    git push origin feature/your-feature-name
    ```

7. **Create a Pull Request:** 
   Go to the original repository and click on the "New Pull Request" button. Provide a detailed description of your changes and why they should be merged.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Creators

- 🔬 [Will](https://www.linkedin.com/in/williamsm01010101/)
- 🎨 [Tabs](https://www.linkedin.com/in/t%C3%A1bata-martins-9a5383131/)

Thank you for using the Prompt Generator! We hope it helps you create effective and detailed prompts for your AI tasks. If you have any questions or feedback, please open an issue or contact the creators directly. Happy prompting! 🎉

---

Feel free to customize this `README.md` to better match your project's specific details and requirements.
