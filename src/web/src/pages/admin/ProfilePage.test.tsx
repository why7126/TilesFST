import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Outlet, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ProfilePage } from './ProfilePage';

const profile = {
  id: '1',
  username: 'admin',
  display_name: 'Admin User',
  role: 'admin',
  status: 'active',
  email: 'admin@tilesfst.com',
  phone: '138 0000 2026',
  remark: '负责资料维护',
  avatar_object_key: null,
  avatar_url: null,
  last_login_at: '2026-06-16T10:24:00+08:00',
  updated_at: '2026-06-16T10:24:00+08:00',
};

const activities = [
  {
    id: 'a1',
    action_type: 'profile_update',
    summary: '修改昵称与备注',
    created_at: '2026-06-16T10:24:00+08:00',
  },
];

vi.mock('@/features/admin/api/profile-api', () => ({
  fetchProfileMe: vi.fn(),
  fetchProfileActivities: vi.fn(),
  patchProfileMe: vi.fn(),
  uploadAvatar: vi.fn(),
}));

describe('ProfilePage', () => {
  function renderProfilePage() {
    return render(
      <MemoryRouter initialEntries={['/admin/profile']}>
        <Routes>
          <Route
            element={<Outlet context={{ onOpenPasswordChange: vi.fn() }} />}
          >
            <Route path="/admin/profile" element={<ProfilePage />} />
          </Route>
        </Routes>
      </MemoryRouter>,
    );
  }

  beforeEach(async () => {
    const api = await import('@/features/admin/api/profile-api');
    vi.mocked(api.fetchProfileMe).mockResolvedValue(profile);
    vi.mocked(api.fetchProfileActivities).mockResolvedValue(activities);
    vi.mocked(api.patchProfileMe).mockImplementation(async (payload) => ({
      ...profile,
      ...payload,
      display_name: payload.display_name ?? profile.display_name,
      email: payload.email ?? profile.email,
      phone: payload.phone ?? profile.phone,
      remark: payload.remark ?? profile.remark,
      updated_at: '2026-06-16T11:00:00+08:00',
    }));
  });

  it('renders profile form and timeline', async () => {
    renderProfilePage();

    expect(await screen.findByText('个人资料')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Admin User')).toBeInTheDocument();
    expect(screen.getByText('资料更新')).toBeInTheDocument();
  });

  it('does not show role or status fields in the profile form grid', async () => {
    renderProfilePage();

    await screen.findByDisplayValue('Admin User');
    const formGrid = document.querySelector('.profile-form-grid');
    expect(formGrid).toBeTruthy();
    expect(formGrid?.querySelector('#profile-role')).toBeNull();
    expect(formGrid?.querySelector('#profile-status')).toBeNull();
    expect(screen.queryByLabelText('所属角色')).toBeNull();
    expect(screen.queryByLabelText('账号状态')).toBeNull();
    expect(screen.getByText('所属角色')).toBeInTheDocument();
    expect(screen.getByText('账号状态')).toBeInTheDocument();
  });

  it('validates nickname length before save', async () => {
    renderProfilePage();

    await screen.findByDisplayValue('Admin User');
    fireEvent.change(screen.getByLabelText('昵称 *'), { target: { value: 'A' } });
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    expect(await screen.findByText('昵称长度须为 2–32 个字符')).toBeInTheDocument();
  });

  it('resets form to loaded snapshot', async () => {
    renderProfilePage();

    await screen.findByDisplayValue('Admin User');
    fireEvent.change(screen.getByLabelText('昵称 *'), { target: { value: 'Changed Name' } });
    fireEvent.click(screen.getByRole('button', { name: '重置' }));

    expect(screen.getByDisplayValue('Admin User')).toBeInTheDocument();
  });

  it('shows inline save tip after successful save', async () => {
    const api = await import('@/features/admin/api/profile-api');

    renderProfilePage();

    await screen.findByDisplayValue('Admin User');
    fireEvent.click(screen.getByRole('button', { name: '保存修改' }));

    await waitFor(() => {
      expect(api.patchProfileMe).toHaveBeenCalled();
    });
    expect(await screen.findByText(/资料已更新/)).toBeInTheDocument();
  });

  it('renders at most five timeline items from activities API', async () => {
    const api = await import('@/features/admin/api/profile-api');
    const manyActivities = Array.from({ length: 5 }, (_, index) => ({
      id: `a${index}`,
      action_type: 'profile_update',
      summary: `update ${index}`,
      created_at: `2026-06-16T10:${String(index).padStart(2, '0')}:00+08:00`,
    }));
    vi.mocked(api.fetchProfileActivities).mockResolvedValue(manyActivities);

    renderProfilePage();

    await screen.findByText('个人资料');
    expect(document.querySelectorAll('.timeline-item')).toHaveLength(5);
  });

  it('exposes a single save button in the form actions area', async () => {
    renderProfilePage();

    await screen.findByDisplayValue('Admin User');
    expect(screen.getAllByRole('button', { name: '保存修改' })).toHaveLength(1);
    expect(document.querySelector('.profile-page-head .btn.primary')).toBeNull();
  });
});
