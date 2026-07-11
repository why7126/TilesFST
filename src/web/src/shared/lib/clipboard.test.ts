import { afterEach, describe, expect, it, vi } from 'vitest';

import { copyTextToClipboard } from './clipboard';

const originalClipboard = navigator.clipboard;

function setClipboard(writeText?: (text: string) => Promise<void>) {
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: writeText ? { writeText } : undefined,
  });
}

function restoreClipboard() {
  Object.defineProperty(navigator, 'clipboard', {
    configurable: true,
    value: originalClipboard,
  });
}

describe('copyTextToClipboard', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    restoreClipboard();
  });

  it('returns success with normalized text when Clipboard API resolves', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    setClipboard(writeText);

    await expect(copyTextToClipboard('  req_123  ')).resolves.toEqual({
      status: 'success',
      text: 'req_123',
      fallbackAttempted: false,
      fallbackFailed: false,
    });
    expect(writeText).toHaveBeenCalledWith('req_123');
  });

  it('returns empty without calling Clipboard API for blank values', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    setClipboard(writeText);

    await expect(copyTextToClipboard('   ')).resolves.toEqual({
      status: 'empty',
      fallbackAttempted: false,
      fallbackFailed: false,
    });
    expect(writeText).not.toHaveBeenCalled();
  });

  it('returns unavailable and invokes fallback when Clipboard API is absent', async () => {
    const selectFallback = vi.fn();
    setClipboard(undefined);

    await expect(copyTextToClipboard('ManualPass789!', { selectFallback })).resolves.toMatchObject({
      status: 'unavailable',
      fallbackAttempted: true,
      fallbackFailed: false,
    });
    expect(selectFallback).toHaveBeenCalledOnce();
  });

  it('returns failed and invokes fallback when write rejects', async () => {
    const writeText = vi.fn().mockRejectedValue(new Error('denied'));
    const selectFallback = vi.fn();
    setClipboard(writeText);

    await expect(copyTextToClipboard('ResetPass456!', { selectFallback })).resolves.toMatchObject({
      status: 'failed',
      fallbackAttempted: true,
      fallbackFailed: false,
    });
    expect(selectFallback).toHaveBeenCalledOnce();
  });

  it('does not throw when fallback selection fails', async () => {
    setClipboard(undefined);

    await expect(
      copyTextToClipboard('value', {
        selectFallback: () => {
          throw new Error('selection failed');
        },
      }),
    ).resolves.toMatchObject({
      status: 'unavailable',
      fallbackAttempted: true,
      fallbackFailed: true,
    });
  });
});
