from typing import Dict, List

class PermissionService:
    def __init__(self):
        # A simple in-memory store for user roles and permissions
        self.user_roles: Dict[str, str] = {}  # Maps user_id to role
        self.role_permissions: Dict[str, List[str]] = {
            "admin": ["add_document", "update_document", "delete_document", "get_document"],
            "user": ["add_document", "get_document"]
        }

    def assign_role(self, user_id: str, role: str):
        """Assign a role to a user."""
        if role not in self.role_permissions:
            raise ValueError(f"Role {role} does not exist.")
        self.user_roles[user_id] = role

    def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if a user has a specific permission."""
        role = self.user_roles.get(user_id)
        if not role:
            return False
        return permission in self.role_permissions.get(role, [])

    def add_role(self, role: str, permissions: List[str]):
        """Add a new role with specific permissions."""
        if role in self.role_permissions:
            raise ValueError(f"Role {role} already exists.")
        self.role_permissions[role] = permissions

    def get_user_role(self, user_id: str) -> str:
        """Get the role of a user."""
        return self.user_roles.get(user_id, "user")  # Default to 'user' role
