# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of the `finetune` package seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email security@example.com with details about the vulnerability**
3. Include the following information:
   - Type of vulnerability
   - Full path to the file(s) containing the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if possible)

## Security Measures

This project implements the following security measures:

### Code Quality and Security

- Static code analysis with ruff for detecting common security issues
- Dependencies are scanned for vulnerabilities with dependabot
- All dependencies are pinned to specific versions in uv.lock
- Comprehensive test suite including security-focused tests

### Docker Security

- Multi-stage builds for smaller attack surface
- Running as non-root user
- Official base images with regular security updates
- Container healthchecks for reliability

### Development Practices

- All code changes are reviewed before merging
- CI/CD pipeline includes security checks
- Regular dependency updates
- No secrets or credentials are stored in the repository

## For Contributors

When contributing to this project, please keep security in mind:

- Never commit secrets, credentials, or sensitive information
- Install pre-commit hooks to catch security issues early
- Follow secure coding practices
- Keep dependencies up to date
