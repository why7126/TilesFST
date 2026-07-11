import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ResetPasswordDialog } from './ResetPasswordDialog';

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

describe('ResetPasswordDialog', () => {
  afterEach(() => {
    vi.restoreAllMocks();
    restoreClipboard();
  });

  it('copies the displayed one-time password and shows success feedback', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    setClipboard(writeText);

    render(
      <ResetPasswordDialog open password="InitialPass123!" onClose={vi.fn()} />,
    );

    fireEvent.click(screen.getByRole('button', { name: '复制密码' }));

    await waitFor(() => {
      expect(writeText).toHaveBeenCalledWith('InitialPass123!');
    });
    expect(screen.getByRole('status')).toHaveTextContent('密码已复制');
    expect(screen.getByText(/关闭后不可再次查看/)).toBeInTheDocument();
  });

  it('shows manual copy guidance and selects the password when clipboard write fails', async () => {
    const writeText = vi.fn().mockRejectedValue(new Error('denied'));
    setClipboard(writeText);

    render(
      <ResetPasswordDialog open password="ResetPass456!" onClose={vi.fn()} />,
    );

    const passwordInput = screen.getByLabelText('随机密码') as HTMLInputElement;
    const focusSpy = vi.spyOn(passwordInput, 'focus');
    const selectSpy = vi.spyOn(passwordInput, 'select');

    fireEvent.click(screen.getByRole('button', { name: '复制密码' }));

    await waitFor(() => {
      expect(writeText).toHaveBeenCalledWith('ResetPass456!');
    });
    expect(focusSpy).toHaveBeenCalled();
    expect(selectSpy).toHaveBeenCalled();
    expect(screen.getByRole('status')).toHaveTextContent('自动复制失败');
  });

  it('falls back to manual copy when Clipboard API is unavailable', async () => {
    setClipboard(undefined);

    render(
      <ResetPasswordDialog open password="ManualPass789!" onClose={vi.fn()} />,
    );

    const passwordInput = screen.getByLabelText('随机密码') as HTMLInputElement;
    const focusSpy = vi.spyOn(passwordInput, 'focus');
    const selectSpy = vi.spyOn(passwordInput, 'select');

    fireEvent.click(screen.getByRole('button', { name: '复制密码' }));

    await waitFor(() => {
      expect(focusSpy).toHaveBeenCalled();
      expect(selectSpy).toHaveBeenCalled();
    });
    expect(screen.getByRole('status')).toHaveTextContent('自动复制失败');
  });

  it('does not render when closed or missing a password', () => {
    const { rerender } = render(
      <ResetPasswordDialog open={false} password="HiddenPass123!" onClose={vi.fn()} />,
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

    rerender(<ResetPasswordDialog open password={null} onClose={vi.fn()} />);

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
