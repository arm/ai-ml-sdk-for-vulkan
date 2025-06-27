.. include:: ../../generated/CONTRIBUTING.md
   :parser: myst_parser.sphinx_

Secure coding practices
-----------------------

General coding best practices are:

- Use tested and approved managed code rather than creating new unmanaged code
  for common tasks.

- Utilize locking to prevent multiple simultaneous requests for use a
  synchronization mechanism to prevent race conditions.

- Protect shared variables and resources from inappropriate concurrent access.

- Explicitly initialize all your variables and other data stores, either during
  declaration or just before the first usage.

- In cases where the application must run with elevated privileges, raise
  privileges as late as possible, and drop them as soon as possible.

- Avoid calculation errors by understanding your programming language's
  underlying representation and how it interacts with numeric calculation. Pay
  close attention to byte size discrepancies, precision, signed/unsigned
  distinctions, truncation, conversion and casting between types, "not-a-number"
  calculations, and how your language handles numbers that are too large or too
  small for its underlying representation.

- Restrict users from generating new code or altering existing code.

- For common tasks, use tested and approved managed code rather than creating new
  unmanaged code.

- Utilize locking to prevent multiple simultaneous requests and use a synchronization
  mechanism to prevent race conditions.

- Protect shared variables and resources from inappropriate concurrent access.

- Explicitly initialize all your variables and other data stores, either during
  declaration or just before the first usage.

- In cases where the application must run with elevated privileges, raise
  privileges as late as possible. Then drop privileges as soon as possible.

- Avoid calculation errors by understanding the underlying representation of
  your programming language and how it interacts with numeric calculation, especially:

    - Byte size discrepancies
    - Precision
    - Signed and unsigned distinctions
    - Truncation
    - Conversion and casting between types
    - Not-a-number calculations and how your language handles numbers that are
      too large or too small for its underlying representation.

- Restrict users from generating new code or altering existing code.


Secure coding best practices are:

- Validate input from all untrusted data sources. Proper input validation can
  eliminate most software vulnerabilities. Be suspicious of most external data
  sources, including:

  - Command line arguments
  - Network interfaces
  - Environmental variables
  - User controlled files

- Be aware of compiler warnings. Compile code using the default compiler flags
  that exist in the CMakeLists file.

- Use static analysis tools to detect and eliminate additional security flaws.

- Keep the design as simple and small as possible. Complex designs increase the
  likelihood that errors will be made in their implementation, configuration, and
  use. Additionally, the effort required to achieve an appropriate level of assurance
  increases dramatically as security mechanisms become more complex.

- Base access decisions on permission rather than exclusion. This means that, by
  default, access is denied and the protection scheme identifies conditions under
  which access is permitted.

- Adhere to the principle of least privilege. Every process should execute with
  the least set of privileges necessary to complete the job. Any elevated permission
  should only be accessed for the least amount of time required to complete the
  privileged task. This approach reduces the opportunities an attacker has to
  execute arbitrary code with elevated privileges.

- Sanitize all data passed to complex subsystems, for example:

    - Command shells
    - Relational databases
    - Commercial off-the-shelf (COTS) components

  Attackers may be able to invoke unused functionality in these components using
  various injection attacks. This is not necessarily an input validation problem
  because the complex subsystem being invoked does not understand the context in
  which the call is made. Because the calling process understands the context, it
  is responsible for sanitizing the data before invoking the subsystem.

- Manage risk with multiple defensive strategies. For example, if one layer of
  defense turns out to be inadequate, another layer of defense can:

  - Prevent a security flaw from becoming an exploitable vulnerability.
  - Limit the consequences of a successful exploit. For example, by combining
    secure programming techniques with secure runtime environments. This should
    reduce the likelihood that vulnerabilities remaining in the code at deployment
    time can be exploited in the operational environment.


Inclusive language guidelines
-----------------------------

Arm® values inclusive communities. Arm® recognizes that we and our industry have
used language that can be offensive. Arm® strives to lead the industry and create
change.

We believe that this document contains no offensive language. To report offensive
language in this document, email terms@arm.com.
