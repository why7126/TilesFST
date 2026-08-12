export function getUserInitials(displayName?: string | null, username?: string | null): string {
  const name = displayName?.trim() || username?.trim() || 'AU';
  const parts = name.split(/\s+/).filter(Boolean);

  if (parts.length >= 2) {
    return `${parts[0]![0] ?? ''}${parts[1]![0] ?? ''}`.toUpperCase();
  }

  return name.slice(0, 2).toUpperCase();
}

export function getUserDisplayName(displayName?: string | null, username?: string | null): string {
  return displayName?.trim() || username?.trim() || 'Admin User';
}
