export type ClipboardCopyStatus = 'success' | 'failed' | 'unavailable' | 'empty';

export interface ClipboardCopyResult {
  status: ClipboardCopyStatus;
  text?: string;
  fallbackAttempted: boolean;
  fallbackFailed: boolean;
}

export interface ClipboardCopyOptions {
  selectFallback?: () => void;
}

function runFallback(selectFallback?: () => void): Pick<ClipboardCopyResult, 'fallbackAttempted' | 'fallbackFailed'> {
  if (!selectFallback) {
    return { fallbackAttempted: false, fallbackFailed: false };
  }
  try {
    selectFallback();
    return { fallbackAttempted: true, fallbackFailed: false };
  } catch {
    return { fallbackAttempted: true, fallbackFailed: true };
  }
}

export async function copyTextToClipboard(
  value: string | null | undefined,
  options: ClipboardCopyOptions = {},
): Promise<ClipboardCopyResult> {
  const text = value?.trim() ?? '';
  if (!text) {
    return { status: 'empty', fallbackAttempted: false, fallbackFailed: false };
  }

  const writeText = navigator.clipboard?.writeText;
  if (!writeText) {
    return {
      status: 'unavailable',
      text,
      ...runFallback(options.selectFallback),
    };
  }

  try {
    await writeText.call(navigator.clipboard, text);
    return { status: 'success', text, fallbackAttempted: false, fallbackFailed: false };
  } catch {
    return {
      status: 'failed',
      text,
      ...runFallback(options.selectFallback),
    };
  }
}
