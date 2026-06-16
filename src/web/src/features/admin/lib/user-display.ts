export function getUserInitials(displayName?: string | null, username?: string | null): string {
  const name = (displayName || username || 'AU').trim();
  const parts = name.split(/\s+/).filter(Boolean);

  if (parts.length >= 2) {
    return `${parts[0]![0] ?? ''}${parts[1]![0] ?? ''}`.toUpperCase();
  }

  return name.slice(0, 2).toUpperCase();
}

export function getUserDisplayName(displayName?: string | null, username?: string | null): string {
  return displayName || username || 'Admin User';
}

export function getUserEmail(username?: string | null): string {
  if (!username) {
    return 'admin@tilesfst.com';
  }

  return `${username}@tilesfst.com`;
}
