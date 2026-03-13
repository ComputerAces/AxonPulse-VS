# 🧩 Security Nodes

This document covers nodes within the **Security** core category.

## 📂 Actions

### Add Group

**Version**: `2.3.0`

Creates a new security group within the connected Security Provider's database.
Groups are used to organize users for bulk permission management.

Inputs:
- Flow: Trigger the creation of the group.
- Group Name: The unique name for the new group.

Outputs:
- Flow: Triggered after the operation is attempted.
- Success: True if the group was successfully created, False if it already exists or an error occurred.

---

### Add Role

**Version**: `2.3.0`

Defines a new security role with specific permissions in the Security Provider's database.
Roles represent sets of capabilities that can be assigned to users or groups.

Inputs:
- Flow: Trigger the creation of the role.
- Role Name: The unique identifier for the role.
- Permissions: A list of permission strings (e.g., ["read", "write"]) to associate with this role.

Outputs:
- Flow: Triggered after the operation is attempted.
- Success: True if the role was successfully created.

---

### Add User

**Version**: `2.3.0`

Registers a new user account in the connected Security Provider's database.
This creates the primary identity record used for authentication and authorization.

Inputs:
- Flow: Trigger the user creation process.
- Username: The unique login name for the user.
- Password: The user's secret password (should be hashed before storage if possible).
- Groups: An optional list of groups to immediately assign the user to.

Outputs:
- Flow: Triggered after the account creation attempt.
- Success: True if the user was successfully registered.

---

### Assign Group to Role

**Version**: `2.3.0`

Links a security group to a specific role, granting all group members the role's permissions.
This is the primary method for bulk authorization management.

Inputs:
- Flow: Trigger the assignment.
- Group Name: The target group name.
- Role Name: The role to be assigned to the group.

Outputs:
- Flow: Triggered after the assignment is attempted.
- Success: True if the relationship was successfully recorded.

---

### Assign User to Group

**Version**: `2.3.0`

Adds an individual user to a security group.
The user will inherit all roles and permissions associated with that group.

Inputs:
- Flow: Trigger the group assignment.
- Username: The target user's name.
- Group Name: The name of the group to join.

Outputs:
- Flow: Triggered after the operation is attempted.
- Success: True if the user was successfully added to the group.

---

### Log In

**Version**: `2.3.0`

Authenticates a user against the Security Provider's database.
If successful, it establishes a user session and updates the active User Provider.

Inputs:
- Flow: Trigger the authentication process.
- Username: The user's login name.
- Password: The secret password to verify.

Outputs:
- Flow: Standard execution trigger (executed ONLY upon successful authentication).
- Error Flow: Pulse triggered if authentication fails or an error occurs.
- Authenticated: Boolean status of the login attempt.

---

### Log Out

**Version**: `2.3.0`

Terminates the current user session and clears authentication tokens.
Used to securely exit an application scope.

Inputs:
- Flow: Trigger the logout process.

Outputs:
- Flow: Triggered after session data has been cleared.

---

### Register

**Version**: `2.3.0`

Handles self-service user registration with password confirmation.
Checks for existing usernames before creating a new record.

Inputs:
- Flow: Trigger the registration workflow.
- Username: The desired login name.
- Password: The primary password entry.
- Confirm Password: Must match the Password input to succeed.

Outputs:
- Flow: Triggered after the registration attempt.
- Success: True if the account was created successfully.

---

### Remove User

**Version**: `2.3.0`

Permanently deletes a user account from the connected Security Provider's database.

Inputs:
- Flow: Trigger the deletion.
- Username: The name of the user account to remove.

Outputs:
- Flow: Triggered after the deletion is attempted.
- Success: True if the user was successfully removed.

---

### Set Password

**Version**: `2.3.0`

Manually hashes a plaintext string into a secure SHA-256 password hash.
Useful for preparing password data before passing it to 'Add User' or 'Update User'.

Inputs:
- Flow: Trigger the hashing process.
- Plaintext: The raw string to be hashed.

Outputs:
- Flow: Triggered after hashing.
- Password: The resulting hexadecimal hash string.

---

### Update User

**Version**: `2.3.0`

Modifies existing user data in the Security Provider's database using a dictionary of updates.

Inputs:
- Flow: Trigger the update process.
- Username: The target user account to update.
- Data: A dictionary containing the fields and new values (e.g., {"Password": "new_hash"}).

Outputs:
- Flow: Triggered after the update attempt.

---

## 📂 Providers

### Basic Security Provider

**Version**: `2.3.0`

Provides standard database-backed security services including authentication and authorization.
Connects to a Database Provider to store and retrieve user, group, and role information.

Inputs:
- Flow: Trigger to enter the security scope.
- Table Name: The database table used for storing user data (default: 'Users').
- Use Verify: If True, enables stricter session verification.

Outputs:
- Done: Triggered upon exiting the security scope.
- Provider Flow: Active while inside the security context.

---

### OS Security Provider

**Version**: `2.3.0`

Security provider that leverages OS-level security features and restrictions.
Integrated with system permissions and environment security barriers.

Inputs:
- Flow: Start the OS security provider service.

Outputs:
- Provider Flow: Active while the provider service is running.
- Flow: Triggered when the service is stopped.

---

### User Provider

**Version**: `2.3.0`

Service provider for user identity and permission management.
Handles user state, roles, groups, and permission category checks.

Inputs:
- Flow: Start the user provider service.

Outputs:
- Provider Flow: Active while the provider service is running.
- Flow: Triggered when the service is stopped.

---

[Back to Node Index](Index.md)
