# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in Arduino Skills, please report it responsibly.

### Do Not

❌ **Do not** open a public GitHub issue for security vulnerabilities  
❌ **Do not** post security details on forums or social media  
❌ **Do not** mention the vulnerability in pull request descriptions

### Do

✅ **Report privately** via email to the project maintainer  
✅ **Include proof-of-concept** code or detailed reproduction steps  
✅ **Allow 30 days** for a response and patch before public disclosure  
✅ **Reference CVE** if one is assigned (after fix is published)

### Reporting Process

1. **Send email to:** `[maintainer email - add your email here]`
   - Subject: `[SECURITY] Vulnerability Report: [Brief Description]`
   - Include:
     - Description of vulnerability
     - Steps to reproduce
     - Affected versions (e.g., v0.5.0+)
     - Affected platforms (UNO, ESP32, RP2040)
     - Impact assessment (High/Medium/Low)
     - Suggested fix (if you have one)

2. **We will:**
   - Acknowledge receipt within 2 business days
   - Investigate and verify the vulnerability
   - Develop and test a fix
   - Create a patched release
   - Credit you in the release notes (with your permission)

3. **Timeline:**
   - We aim to patch critical vulnerabilities within 7 days
   - Medium priority vulnerabilities: within 14 days
   - Low priority vulnerabilities: within 30 days

## Scope

### What We Consider Security Issues

- Buffer overflows or memory corruption
- Integer overflow bugs in timing calculations
- Privilege escalation (if applicable to embedded systems)
- Authentication/authorization flaws
- Cryptographic weaknesses
- Injection vulnerabilities
- Denial-of-service vectors
- Hardware-specific security issues (e.g., power analysis, side channels)

### What We Don't Consider Security Issues

- Non-critical documentation improvements
- Feature requests or enhancement suggestions
- Performance optimization opportunities
- Code style or quality issues
- Missing error handling (unless exploitable)
- Compilation warnings without security impact

## Supported Versions

Security updates are provided for:

| Version | Status | Support Ends |
|---------|--------|--------------|
| 0.7.x | Current | Latest version |
| 0.6.x | Maintenance | 3 months from 0.8.0 release |
| 0.5.x | Limited | 1 month from 0.6.0 release |
| < 0.5.0 | Unsupported | No updates |

## Known Security Limitations

### Memory Safety on UNO

Arduino UNO has only 2 KB of SRAM. While we follow bounds-checking best practices, it's possible for:
- Buffer overflows if developers ignore size constraints
- Stack overflow if arrays are too large
- Integer overflow in timing calculations (mitigated with `unsigned long`)

**Recommendation:** Use ESP32 or RP2040 for mission-critical applications.

### Serial Communication

Serial communication (115200 baud) is unencrypted by default. For sensitive data:
- Implement encryption at application level
- Use WiFi with TLS (ESP32/RP2040 only)
- Isolate serial interface on trusted networks

### WiFi Security (ESP32)

WiFi examples use WPA2/WPA3 encryption. However:
- Always use strong SSID/password
- Disable WPS if possible
- Keep WiFi firmware updated
- Do not hardcode credentials (use secure storage)

## Code Quality Standards

All code follows these security best practices:

### Timing-Safe Code
```cpp
// ✅ Safe: Uses unsigned long to prevent overflow
unsigned long lastTime = 0;
const unsigned long INTERVAL = 1000; // ms

if (millis() - lastTime >= INTERVAL) {
    lastTime = millis();
    // Safe timing logic
}

// ❌ Unsafe: Integer overflow risk
int lastTime = 0;
if (millis() - lastTime >= INTERVAL) {  // Overflow after ~49 days
```

### Memory-Safe Code
```cpp
// ✅ Safe: Bounds checking
const int BUFFER_SIZE = 100;
char buffer[BUFFER_SIZE];

void addToBuffer(const char* data, int len) {
    if (len > BUFFER_SIZE - 1) len = BUFFER_SIZE - 1;
    strncpy(buffer, data, len);
    buffer[len] = '\0';
}

// ❌ Unsafe: No bounds checking
void addToBuffer(const char* data) {
    strcpy(buffer, data);  // Overflow risk!
}
```

### Hardware Abstraction
```cpp
// ✅ Safe: Pin definitions in config.h
#include "config.h"
digitalWrite(LED_PIN, HIGH);

// ❌ Unsafe: Hardcoded pins
digitalWrite(13, HIGH);  // Might not exist on other boards
```

## Dependencies

All code dependencies use:

- **PEP 723 inline dependencies** for Python (no external requirements.txt)
- **Arduino built-in libraries** (no external package managers)
- **Standard C++ libraries** (no third-party frameworks)

### Third-Party Libraries

If a skill uses external Arduino libraries (e.g., Adafruit), it must:
1. Document the library in SKILL.md
2. Specify version constraints
3. Explain why it's necessary
4. Document security assumptions

## Compliance

Arduino Skills follows:
- **OWASP Secure Coding Practices** for application code
- **Arduino Safety Guidelines** for hardware interaction
- **CERT C++ Coding Standards** for embedded systems

## Security Checklist

For every commit, verify:

- [ ] No hardcoded credentials (passwords, API keys, WiFi SSIDs)
- [ ] No debug code left in production (verbose logging, backdoors)
- [ ] No integer overflow bugs (use unsigned long for millis)
- [ ] No buffer overflow bugs (bounds checking on arrays)
- [ ] No null pointer dereferences
- [ ] Dependencies are documented and version-pinned
- [ ] Third-party code is from trusted sources
- [ ] Code compiles without warnings

## Questions?

- **Security question:** Email maintainer privately
- **General question:** Use GitHub [discussions](../../discussions)
- **Bug report:** Use GitHub [issues](../../issues)

---

**Thank you for helping keep Arduino Skills secure!** 🔒
