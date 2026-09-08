# Security policy

This software is verified for security for official releases and as such we do
not make promises about the quality of the product or any patches delivered
between releases.

## Security boundaries

ML SDK for Vulkan® components do not sandbox untrusted input. Library
components run in the caller's process, so that caller is within their trust
boundary. Data supplied to SDK components are expected to come from trusted
sources. SDK components also rely on trusted behaviour from the operating
system, filesystem, Vulkan® Loader, installable client driver (ICD), and their
callers. Weaknesses originating in those trusted dependencies or in a
compromised caller of an in-process library cannot be addressed by the affected
SDK component.

## Reporting a vulnerability

You can report security vulnerabilities to the Arm® Product Security Incident
Response Team (PSIRT) by sending an email to:
[psirt@arm.com](mailto:psirt@arm.com).

For more information about security vulnerabilities, see:
[Report a Security Vulnerability](https://developer.arm.com/support/arm-security-updates/report-security-vulnerabilities).
