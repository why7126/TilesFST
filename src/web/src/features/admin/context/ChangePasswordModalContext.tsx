import { createContext, useContext } from 'react';

interface ChangePasswordModalContextValue {
  openChangePasswordModal: () => void;
}

export const ChangePasswordModalContext =
  createContext<ChangePasswordModalContextValue | null>(null);

export function useChangePasswordModal(): ChangePasswordModalContextValue {
  const context = useContext(ChangePasswordModalContext);
  if (!context) {
    return { openChangePasswordModal: () => undefined };
  }
  return context;
}
