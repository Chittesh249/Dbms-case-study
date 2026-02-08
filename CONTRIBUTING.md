# Contributing to Milvus Vector Database Implementation

First off, thank you for considering contributing to this project! Your efforts help make this project better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guides](#style-guides)
- [Community](#community)

## 📖 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [maintainer-email@example.com].

## 🚀 How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible.
- **Provide specific examples to demonstrate the steps**.
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see instead and why.**

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Provide specific examples to demonstrate the steps**.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
- **Explain why this enhancement would be useful** to most users.

### Your First Code Contribution

Unsure where to begin contributing to this project? You can start by looking through these `beginner` and `help-wanted` issues:

- [Beginner issues](link-to-beginner-issues) - issues which should only require a small amount of code, and a test or two.
- [Help wanted issues](link-to-help-wanted-issues) - issues which should be a bit more involved than `beginner` issues.

### Pull Requests

When you submit a pull request, please follow these guidelines:

- Include screenshots and animated GIFs in your pull request whenever possible.
- Follow the [style guides](#style-guides) below.
- After you submit your pull request, verify that all status checks are passing.

## ⚙️ Development Setup

### Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** installed
- **OpenAI API Key** (recommended for full functionality)
- **Git** for version control

### Getting Started

1. **Fork the repository** on GitHub.

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/milvus-implementation.git
   cd milvus-implementation
   ```

3. **Set up the backend**:
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

4. **Set up the frontend**:
   ```bash
   cd ../  # Back to project root
   npm install
   ```

5. **Configure environment variables**:
   ```bash
   # In the Backend directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

6. **Run the application**:
   ```bash
   # Terminal 1 - Backend
   cd Backend
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001
   
   # Terminal 2 - Frontend
   cd milvus-implementation
   npm run dev
   ```

## 🔄 Pull Request Process

1. **Ensure your fork is up-to-date** with the main repository:
   ```bash
   git remote add upstream https://github.com/username/milvus-implementation.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit them following our commit message conventions.

4. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a pull request** from your fork to the main repository.

6. **Wait for review** and address any feedback from maintainers.

## 📝 Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused on a single task

### JavaScript/React Style Guide

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Keep components small and focused on a single responsibility
- Use descriptive variable and function names
- Add PropTypes or TypeScript for component prop validation

### Documentation Style Guide

- Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
- Write in American English
- Use clear and concise language
- Include examples wherever possible

## 🐛 Issue Report Process

1. **Search for duplicate issues** before creating a new one
2. **Check if the issue has been fixed** in the latest version
3. **Create a new issue** with a descriptive title and clear description
4. **Include reproduction steps** if applicable
5. **Tag the issue** with appropriate labels

## 🧪 Testing

### Backend Tests
```bash
cd Backend
pytest
```

### Frontend Tests
```bash
npm test
```

### Integration Tests
All PRs must pass the continuous integration pipeline before merging.

## 🤝 Community

- Join our discussions on GitHub Issues
- Share your ideas and feedback
- Help others in the community
- Contribute to documentation and examples

## 🙏 Thank You

Thank you for taking the time to contribute to this project! Your contributions help make this project better for everyone.

---

<div align="center">

Made with ❤️ by the community

[Back to top ↑](#contributing-to-milvus-vector-database-implementation)

</div>