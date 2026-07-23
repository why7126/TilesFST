import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const fetchSettingsGroupMock = vi.fn();
const patchSettingsGroupMock = vi.fn();
const resetSettingsGroupMock = vi.fn();
const fetchRecentAuditMock = vi.fn();
const navigateMock = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  return {
    ...actual,
    useNavigate: () => navigateMock,
  };
});

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/admin/api/system-settings-api', () => ({
  fetchSettingsGroup: (...args: unknown[]) => fetchSettingsGroupMock(...args),
  patchSettingsGroup: (...args: unknown[]) => patchSettingsGroupMock(...args),
  resetSettingsGroup: (...args: unknown[]) => resetSettingsGroupMock(...args),
  fetchRecentAudit: (...args: unknown[]) => fetchRecentAuditMock(...args),
}));

import { SystemSettingsPage } from './SystemSettingsPage';

const basicPayload = {
  platform_name: 'TILESFST',
  default_language: 'zh-CN',
  default_timezone: 'Asia/Shanghai',
  data_refresh_minutes: 15,
  support_email: 'support@tilesfst.com',
  maintenance_window: '每周日 02:00-03:00',
  system_announcement: '公告',
  show_dashboard_metrics: true,
  show_maintenance_notice: true,
};

const mediaPayload = {
  max_image_size_mb: 20,
  max_video_size_mb: 500,
  max_file_size_mb: 25,
  allowed_image_types: 'image/jpeg,image/png,image/webp',
  allowed_video_types: 'video/mp4',
  minio_bucket: 'tilesfst',
  object_key_rule: '{prefix}/{tenant}/{resource_type}/{uuid}.{ext}',
};

function renderPage(initialPath = '/admin/settings/basic') {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route path="/admin/settings/:tab" element={<SystemSettingsPage />} />
        <Route path="/admin/settings" element={<SystemSettingsPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

describe('SystemSettingsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(window, 'confirm').mockImplementation(() => {
      throw new Error('window.confirm must not be called');
    });
    fetchSettingsGroupMock.mockImplementation(async (group: string) => {
      if (group === 'media') return mediaPayload;
      return basicPayload;
    });
    fetchRecentAuditMock.mockResolvedValue([]);
    patchSettingsGroupMock.mockImplementation(async (group: string, patch: Record<string, unknown>) => ({
      ...(group === 'media' ? mediaPayload : basicPayload),
      ...patch,
    }));
    resetSettingsGroupMock.mockImplementation(async (group: string) =>
      group === 'media' ? mediaPayload : basicPayload,
    );
  });

  it('renders basic tab and loads settings', async () => {
    renderPage();
    await waitFor(() => {
      expect(screen.getByDisplayValue('TILESFST')).toBeInTheDocument();
    });
    expect(fetchSettingsGroupMock).toHaveBeenCalledWith('basic');
  });

  it('renders eyebrow without V2 suffix', async () => {
    renderPage();
    await waitFor(() => {
      expect(screen.getByText('SYSTEM / SYSTEM SETTINGS')).toBeInTheDocument();
    });
    expect(screen.queryByText(/\/ V2/)).not.toBeInTheDocument();
  });

  it('has a single save button in the footer', async () => {
    renderPage();
    await waitFor(() => {
      expect(screen.getByDisplayValue('TILESFST')).toBeInTheDocument();
    });
    expect(screen.getAllByRole('button', { name: '保存设置' })).toHaveLength(1);
  });

  it('saves basic settings via patch API and shows AdminToast', async () => {
    renderPage();

    await waitFor(() => {
      expect(screen.getByDisplayValue('TILESFST')).toBeInTheDocument();
    });

    const input = screen.getByDisplayValue('TILESFST');
    fireEvent.change(input, { target: { value: 'Tiles Platform' } });

    fireEvent.click(screen.getByRole('button', { name: '保存设置' }));

    await waitFor(() => {
      expect(patchSettingsGroupMock).toHaveBeenCalledWith(
        'basic',
        expect.objectContaining({ platform_name: 'Tiles Platform' }),
      );
    });
    expect(screen.getByRole('status')).toHaveTextContent('设置已保存并立即生效');
    expect(document.querySelector('.settings-save-tip')).toBeNull();
  });

  it('shows modal confirm before reset instead of window.confirm', async () => {
    renderPage();

    await waitFor(() => {
      expect(screen.getByDisplayValue('TILESFST')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '恢复默认' }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('确定恢复该分组为默认配置吗？此操作不可撤销。')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '确认' }));

    await waitFor(() => {
      expect(resetSettingsGroupMock).toHaveBeenCalledWith('basic');
    });
    expect(screen.getByRole('status')).toHaveTextContent('已恢复默认配置');
  });

  it('shows modal confirm when switching tabs with dirty form', async () => {
    renderPage();

    await waitFor(() => {
      expect(screen.getByDisplayValue('TILESFST')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByDisplayValue('TILESFST'), {
      target: { value: 'Dirty Name' },
    });
    fireEvent.click(screen.getByRole('button', { name: /安全策略/ }));

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('有未保存的修改，确定放弃并切换分组吗？')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: '确认' }));

    await waitFor(() => {
      expect(navigateMock).toHaveBeenCalledWith('/admin/settings/security');
    });
  });

  it('loads media tab with extended MIME chip options', async () => {
    renderPage('/admin/settings/media');
    await waitFor(() => {
      expect(screen.getByText('对象存储策略')).toBeInTheDocument();
    });
    expect(fetchSettingsGroupMock).toHaveBeenCalledWith('media');
    expect(screen.getByText('文档最大尺寸 (MB)')).toBeInTheDocument();
    for (const label of ['JPG', 'PNG', 'WebP', 'GIF', 'SVG', 'BMP', 'TIFF', 'HEIC']) {
      expect(screen.getByRole('button', { name: label })).toBeInTheDocument();
    }
    for (const label of ['MP4', 'MOV', 'AVI', 'WebM', 'MKV', 'MPEG', '3GP']) {
      expect(screen.getByRole('button', { name: label })).toBeInTheDocument();
    }
  });
});
