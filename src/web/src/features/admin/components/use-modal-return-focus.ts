import { useLayoutEffect } from 'react';

/** Return keyboard focus to the trigger when a media editing modal closes. */
export function useModalReturnFocus(open: boolean) {
  useLayoutEffect(() => {
    if (!open) return;
    const trigger = document.activeElement;
    return () => {
      if (trigger instanceof HTMLElement && trigger.isConnected) trigger.focus({ preventScroll: true });
    };
  }, [open]);
}
