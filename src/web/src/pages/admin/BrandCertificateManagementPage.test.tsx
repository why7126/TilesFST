import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const fetchBrandCertificatesMock = vi.hoisted(() => vi.fn());
const createBrandCertificateMock = vi.hoisted(() => vi.fn());
const updateBrandCertificateMock = vi.hoisted(() => vi.fn());
const showBrandCertificateMock = vi.hoisted(() => vi.fn());
const hideBrandCertificateMock = vi.hoisted(() => vi.fn());
const deleteBrandCertificateMock = vi.hoisted(() => vi.fn());
const uploadBrandCertificateFileMock = vi.hoisted(() => vi.fn());
const fetchBrandsMock = vi.hoisted(() => vi.fn());
const fetchSettingsGroupMock = vi.hoisted(() => vi.fn());

vi.mock('@/features/auth/api/auth-api', () => ({
  getErrorMessage: (_err: unknown, fallback: string) => fallback,
}));

vi.mock('@/features/auth/store/auth-store', () => ({
  useAuthStore: (selector: (state: unknown) => unknown) =>
    selector({ user: { id: 'admin', role: 'admin', display_name: '管理员' } }),
}));

vi.mock('@/features/admin/api/brand-certificates-api', () => ({
  createBrandCertificate: (...args: unknown[]) => createBrandCertificateMock(...args),
  deleteBrandCertificate: (...args: unknown[]) => deleteBrandCertificateMock(...args),
  fetchBrandCertificates: (...args: unknown[]) => fetchBrandCertificatesMock(...args),
  hideBrandCertificate: (...args: unknown[]) => hideBrandCertificateMock(...args),
  showBrandCertificate: (...args: unknown[]) => showBrandCertificateMock(...args),
  updateBrandCertificate: (...args: unknown[]) => updateBrandCertificateMock(...args),
  uploadBrandCertificateFile: (...args: unknown[]) => uploadBrandCertificateFileMock(...args),
}));

vi.mock('@/features/admin/api/brands-api', () => ({
  fetchBrands: (...args: unknown[]) => fetchBrandsMock(...args),
}));

vi.mock('@/features/admin/api/system-settings-api', () => ({
  fetchSettingsGroup: (...args: unknown[]) => fetchSettingsGroupMock(...args),
}));

import { BrandCertificateManagementPage } from './BrandCertificateManagementPage';

const brandPayload = {
  items: [
    { id: 1, name: '岩板品牌', sort_order: 10, sku_count: 0, status: 'ENABLED' },
  ],
  total: 1,
  page: 1,
  page_size: 20,
  summary: { total: 1, enabled_count: 1, disabled_count: 0, unlinked_sku_count: 0 },
};

const certificatePayload = {
  items: [
    {
      id: 7,
      brand_id: 1,
      brand_name: '岩板品牌',
      name: 'ISO 9001 质量管理体系认证',
      sort_order: 10,
      type: 'QUALITY',
      certificate_no: 'ISO-001',
      issuer: '认证机构',
      file_url: '/media/files/default/brand-certificates/iso.pdf',
      file_key: 'files/default/brand-certificates/iso.pdf',
      file_name: 'iso.pdf',
      file_mime_type: 'application/pdf',
      file_size_bytes: 128,
      images: [
        {
          file_url: '/media/files/default/brand-certificates/cover.webp',
          file_key: 'files/default/brand-certificates/cover.webp',
          file_name: 'cover.webp',
          file_mime_type: 'image/webp',
          file_size_bytes: 256,
          is_main: true,
          sort_order: 0,
        },
      ],
      main_image: {
        file_url: '/media/files/default/brand-certificates/cover.webp',
        file_key: 'files/default/brand-certificates/cover.webp',
        file_name: 'cover.webp',
        file_mime_type: 'image/webp',
        file_size_bytes: 256,
        is_main: true,
        sort_order: 0,
      },
      is_permanent: false,
      effective_date: '2026-01-01',
      expiry_date: '2026-12-31',
      validity_status: 'VALID',
      is_visible: true,
      display_status: 'VISIBLE',
      remark: null,
      created_at: '2026-07-15T00:00:00Z',
      updated_at: '2026-07-15T00:00:00Z',
    },
  ],
  total: 1,
  page: 1,
  page_size: 20,
  summary: {
    total: 1,
    valid_count: 1,
    expiring_soon_count: 0,
    expired_count: 0,
  },
};

describe('BrandCertificateManagementPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    fetchBrandsMock.mockResolvedValue(brandPayload);
    fetchSettingsGroupMock.mockResolvedValue({ max_file_size_mb: 50 });
    fetchBrandCertificatesMock.mockResolvedValue(certificatePayload);
    createBrandCertificateMock.mockResolvedValue(certificatePayload.items[0]);
    updateBrandCertificateMock.mockResolvedValue(certificatePayload.items[0]);
    hideBrandCertificateMock.mockResolvedValue({ ...certificatePayload.items[0], is_visible: false });
    uploadBrandCertificateFileMock.mockResolvedValue({
      object_key: 'files/default/brand-certificates/new.pdf',
      url: '/media/files/default/brand-certificates/new.pdf',
      file_key: 'files/default/brand-certificates/new.pdf',
      file_url: '/media/files/default/brand-certificates/new.pdf',
      file_name: 'new.pdf',
      mime_type: 'application/pdf',
      size: 256,
    });
  });

  it('renders list filters metrics and pagination structure', async () => {
    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates?brand_id=1']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenCalledWith(
        expect.objectContaining({ brand_id: 1, page: 1, page_size: 20 }),
      );
    });

    expect(screen.getByRole('heading', { name: '品牌证书' })).toBeInTheDocument();
    expect(screen.getByText('证书总数')).toBeInTheDocument();
    expect(screen.getByLabelText('关键词')).toHaveAttribute(
      'placeholder',
      '搜索证书名称 / 编号 / 发证机构',
    );
    await waitFor(() => {
      expect(screen.getByLabelText('所属品牌')).toHaveTextContent('岩板品牌');
    });
    expect(screen.getByText('ISO 9001 质量管理体系认证')).toBeInTheDocument();
    expect(document.querySelector('img[src="/media/files/default/brand-certificates/cover.webp"]')).toBeInTheDocument();
    expect(screen.queryByText('iso.pdf')).not.toBeInTheDocument();
    expect(screen.queryByText('cover.webp')).not.toBeInTheDocument();
    expect(screen.queryByText('files/default/brand-certificates/iso.pdf')).not.toBeInTheDocument();
    expect(screen.queryByText('/media/files/default/brand-certificates/iso.pdf')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '预览' })).not.toBeInTheDocument();
    expect(screen.getByText('共 1 条证书')).toBeInTheDocument();
    const pagination = screen.getByText('共 1 条证书').closest('.pagination');
    expect(pagination?.querySelector('.page-summary')).toBeInTheDocument();
    expect(pagination?.querySelector('.page-right')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: '查询' })).not.toBeInTheDocument();
  });

  it('applies the unified admin filter dropdown to certificate filters', async () => {
    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenCalledWith(
        expect.objectContaining({
          brand_id: undefined,
          type: undefined,
          validity_status: undefined,
          display_status: undefined,
        }),
      );
    });

    const brandTrigger = await screen.findByLabelText('所属品牌');
    const typeTrigger = screen.getByLabelText('证书类型');
    const validityTrigger = screen.getByLabelText('有效状态');
    const displayTrigger = screen.getByLabelText('展示状态');

    [brandTrigger, typeTrigger, validityTrigger, displayTrigger].forEach((trigger) => {
      expect(trigger).toHaveClass('select');
      expect(trigger).toHaveClass('admin-filter-dropdown-trigger');
    });

    fireEvent.click(brandTrigger);
    expect(screen.getByRole('listbox', { name: '证书品牌选项' })).toHaveClass(
      'admin-filter-dropdown-menu',
    );
    fireEvent.click(screen.getByRole('option', { name: '岩板品牌' }));

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenLastCalledWith(
        expect.objectContaining({ page: 1, brand_id: 1 }),
      );
    });

    fireEvent.click(typeTrigger);
    expect(screen.getByRole('listbox', { name: '证书类型选项' })).toHaveClass(
      'admin-filter-dropdown-menu',
    );
    fireEvent.click(screen.getByRole('option', { name: '质量体系' }));

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenLastCalledWith(
        expect.objectContaining({ page: 1, brand_id: 1, type: 'QUALITY' }),
      );
    });

    fireEvent.click(validityTrigger);
    expect(screen.getByRole('listbox', { name: '证书有效状态选项' })).toHaveClass(
      'admin-filter-dropdown-menu',
    );
    fireEvent.click(screen.getByRole('option', { name: '有效' }));

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenLastCalledWith(
        expect.objectContaining({
          page: 1,
          brand_id: 1,
          type: 'QUALITY',
          validity_status: 'VALID',
        }),
      );
    });

    fireEvent.click(displayTrigger);
    expect(screen.getByRole('listbox', { name: '证书展示状态选项' })).toHaveClass(
      'admin-filter-dropdown-menu',
    );
    fireEvent.click(screen.getByRole('option', { name: '前台隐藏' }));

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenLastCalledWith(
        expect.objectContaining({
          page: 1,
          brand_id: 1,
          type: 'QUALITY',
          validity_status: 'VALID',
          display_status: 'HIDDEN',
        }),
      );
    });

    fireEvent.click(screen.getByRole('button', { name: '重置' }));

    await waitFor(() => {
      expect(fetchBrandCertificatesMock).toHaveBeenLastCalledWith(
        expect.objectContaining({
          page: 1,
          brand_id: undefined,
          type: undefined,
          validity_status: undefined,
          display_status: undefined,
        }),
      );
    });
  });

  it('keeps modal input, disables dates for permanent certificates, and uploads pdf files', async () => {
    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '＋ 新增证书' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '＋ 新增证书' }));
    const dialog = screen.getByRole('dialog', { name: '新增证书' });
    await waitFor(() => {
      expect(within(dialog).getByText('支持 JPG / PNG / WebP / PDF，单文件最大 50MB')).toBeInTheDocument();
    });
    fireEvent.change(within(dialog).getByLabelText('所属品牌 *'), { target: { value: '1' } });
    fireEvent.change(within(dialog).getByLabelText('证书名称 *'), {
      target: { value: '绿色建材证书' },
    });
    fireEvent.click(within(dialog).getByLabelText('长期有效'));
    expect(within(dialog).getByLabelText('生效日期')).toBeDisabled();
    expect(within(dialog).getByLabelText('到期日期')).toBeDisabled();

    const input = dialog.querySelectorAll('input[type="file"]')[1] as HTMLInputElement;
    const file = new File(['pdf'], 'new.pdf', { type: 'application/pdf' });
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(uploadBrandCertificateFileMock).toHaveBeenCalledWith(file, expect.any(Function));
    });
    expect(within(dialog).getByText('new.pdf')).toBeInTheDocument();
    expect(within(dialog).getByText('证书文件已就绪')).toBeInTheDocument();

    fireEvent.click(within(dialog).getByRole('button', { name: '保存证书' }));

    await waitFor(() => {
      expect(createBrandCertificateMock).toHaveBeenCalledWith(
        expect.objectContaining({
          brand_id: 1,
          name: '绿色建材证书',
          file: expect.objectContaining({ file_name: 'new.pdf' }),
          is_permanent: true,
          effective_date: null,
          expiry_date: null,
        }),
      );
    });
  });

  it('opens existing certificate with file fallback hidden and image information visible', async () => {
    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText('ISO 9001 质量管理体系认证')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '编辑' }));
    const dialog = screen.getByRole('dialog', { name: '编辑证书' });

    expect(within(dialog).getByText('iso.pdf')).toBeInTheDocument();
    expect(within(dialog).queryByText('证书文件已就绪')).not.toBeInTheDocument();
    expect(
      dialog.querySelector('img[src="/media/files/default/brand-certificates/cover.webp"]'),
    ).toBeInTheDocument();
    expect(within(dialog).getByText('主图')).toBeInTheDocument();
    expect(within(dialog).getByRole('button', { name: '移除图片 1' })).toBeInTheDocument();
    expect(within(dialog).queryByText('cover.webp')).not.toBeInTheDocument();
    expect(
      within(dialog).queryByText('files/default/brand-certificates/cover.webp'),
    ).not.toBeInTheDocument();
  });

  it('renders date validation message below the expiry date field', async () => {
    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '＋ 新增证书' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '＋ 新增证书' }));
    const dialog = screen.getByRole('dialog', { name: '新增证书' });
    fireEvent.change(within(dialog).getByLabelText('所属品牌 *'), { target: { value: '1' } });
    fireEvent.change(within(dialog).getByLabelText('证书名称 *'), {
      target: { value: '日期校验证书' },
    });
    fireEvent.change(within(dialog).getByLabelText('生效日期'), {
      target: { value: '2026-12-31' },
    });
    fireEvent.change(within(dialog).getByLabelText('到期日期 *'), {
      target: { value: '2026-01-01' },
    });
    const input = dialog.querySelectorAll('input[type="file"]')[1] as HTMLInputElement;
    fireEvent.change(input, {
      target: { files: [new File(['pdf'], 'new.pdf', { type: 'application/pdf' })] },
    });

    await waitFor(() => {
      expect(uploadBrandCertificateFileMock).toHaveBeenCalled();
    });

    fireEvent.click(within(dialog).getByRole('button', { name: '保存证书' }));

    const expiryField = within(dialog).getByLabelText('到期日期 *').closest('.brand-form-item');
    expect(within(expiryField as HTMLElement).getByText('到期日期不能早于生效日期')).toBeInTheDocument();
    expect(dialog.querySelector('.certificate-modal-body > .form-error')).not.toBeInTheDocument();
  });

  it('uploads images and moves selected main image first', async () => {
    uploadBrandCertificateFileMock
      .mockResolvedValueOnce({
        object_key: 'files/default/brand-certificates/page-1.webp',
        url: '/media/files/default/brand-certificates/page-1.webp',
        file_key: 'files/default/brand-certificates/page-1.webp',
        file_url: '/media/files/default/brand-certificates/page-1.webp',
        file_name: 'page-1.webp',
        mime_type: 'image/webp',
        size: 256,
      })
      .mockResolvedValueOnce({
        object_key: 'files/default/brand-certificates/page-2.webp',
        url: '/media/files/default/brand-certificates/page-2.webp',
        file_key: 'files/default/brand-certificates/page-2.webp',
        file_url: '/media/files/default/brand-certificates/page-2.webp',
        file_name: 'page-2.webp',
        mime_type: 'image/webp',
        size: 256,
      });

    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '＋ 新增证书' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '＋ 新增证书' }));
    const dialog = screen.getByRole('dialog', { name: '新增证书' });
    fireEvent.change(within(dialog).getByLabelText('所属品牌 *'), { target: { value: '1' } });
    fireEvent.change(within(dialog).getByLabelText('证书名称 *'), {
      target: { value: '多图证书' },
    });
    fireEvent.click(within(dialog).getByLabelText('长期有效'));

    const imageInput = dialog.querySelectorAll('input[type="file"]')[0] as HTMLInputElement;
    fireEvent.change(imageInput, {
      target: { files: [new File(['img1'], 'page-1.webp', { type: 'image/webp' })] },
    });
    await waitFor(() => {
      expect(
        dialog.querySelector('img[src="/media/files/default/brand-certificates/page-1.webp"]'),
      ).toBeInTheDocument();
    });
    expect(within(dialog).queryByText('page-1.webp')).not.toBeInTheDocument();
    expect(within(dialog).getByText('主图')).toBeInTheDocument();

    fireEvent.change(imageInput, {
      target: { files: [new File(['img2'], 'page-2.webp', { type: 'image/webp' })] },
    });
    await waitFor(() => {
      expect(
        dialog.querySelector('img[src="/media/files/default/brand-certificates/page-2.webp"]'),
      ).toBeInTheDocument();
    });
    expect(within(dialog).queryByText('page-2.webp')).not.toBeInTheDocument();

    fireEvent.click(within(dialog).getByRole('button', { name: '设为主图' }));
    fireEvent.click(within(dialog).getByRole('button', { name: '保存证书' }));

    await waitFor(() => {
      expect(createBrandCertificateMock).toHaveBeenCalledWith(
        expect.objectContaining({
          file: null,
          images: [
            expect.objectContaining({ file_name: 'page-2.webp', is_main: true, sort_order: 0 }),
            expect.objectContaining({ file_name: 'page-1.webp', is_main: false, sort_order: 1 }),
          ],
        }),
      );
    });
  });

  it('uses confirm dialog for hide action without window.confirm', async () => {
    const confirmSpy = vi.spyOn(window, 'confirm');

    render(
      <MemoryRouter initialEntries={['/admin/brand-certificates']}>
        <BrandCertificateManagementPage />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: '隐藏' })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: '隐藏' }));
    const dialog = screen.getByRole('dialog', { name: '隐藏证书' });
    expect(within(dialog).getByText('确认隐藏证书「ISO 9001 质量管理体系认证」？隐藏后前台不再展示。')).toBeInTheDocument();
    expect(confirmSpy).not.toHaveBeenCalled();

    fireEvent.click(within(dialog).getByRole('button', { name: '确认隐藏' }));

    await waitFor(() => {
      expect(hideBrandCertificateMock).toHaveBeenCalledWith(7);
    });
    confirmSpy.mockRestore();
  });
});
