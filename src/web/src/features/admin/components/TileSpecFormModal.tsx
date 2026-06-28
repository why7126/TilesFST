import { useEffect, useMemo, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { TileSpecAdminItem } from '@/shared/api/generated';

import {
  buildDisplayName,
  createTileSpec,
  updateTileSpec,
} from '../api/tile-specs-api';

interface TileSpecFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  spec: TileSpecAdminItem | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

export function TileSpecFormModal({
  open,
  mode,
  spec,
  onClose,
  onSuccess,
}: TileSpecFormModalProps) {
  const [widthMm, setWidthMm] = useState('600');
  const [lengthMm, setLengthMm] = useState('1200');
  const [thicknessMm, setThicknessMm] = useState('');
  const [sortOrder, setSortOrder] = useState('10');
  const [remark, setRemark] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setError(null);
    if (mode === 'edit' && spec) {
      setWidthMm(String(spec.width_mm));
      setLengthMm(String(spec.length_mm));
      setThicknessMm(spec.thickness_mm != null ? String(spec.thickness_mm) : '');
      setSortOrder(String(spec.sort_order));
      setRemark(spec.remark ?? '');
    } else {
      setWidthMm('600');
      setLengthMm('1200');
      setThicknessMm('');
      setSortOrder('10');
      setRemark('');
    }
  }, [open, mode, spec]);

  const previewName = useMemo(() => {
    const width = Number.parseInt(widthMm, 10);
    const length = Number.parseInt(lengthMm, 10);
    if (!Number.isFinite(width) || !Number.isFinite(length) || width < 1 || length < 1) {
      return '—';
    }
    return buildDisplayName(width, length);
  }, [widthMm, lengthMm]);

  if (!open) return null;

  const handleSubmit = async () => {
    const width = Number.parseInt(widthMm, 10);
    const length = Number.parseInt(lengthMm, 10);
    const sort = Number.parseInt(sortOrder, 10);
    const thickness =
      thicknessMm.trim() === '' ? null : Number.parseFloat(Number(thicknessMm).toFixed(1));

    if (!Number.isFinite(width) || width < 1 || width > 9999) {
      setError('宽度必须为 1–9999 的正整数');
      return;
    }
    if (!Number.isFinite(length) || length < 1 || length > 9999) {
      setError('长度必须为 1–9999 的正整数');
      return;
    }
    if (!Number.isFinite(sort) || sort < 1) {
      setError('排序必须为正整数');
      return;
    }
    if (thickness != null && (!Number.isFinite(thickness) || thickness <= 0)) {
      setError('厚度必须为正数');
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      const payload = {
        width_mm: width,
        length_mm: length,
        thickness_mm: thickness,
        sort_order: sort,
        remark: remark.trim() || null,
      };
      if (mode === 'edit' && spec) {
        await updateTileSpec(spec.id, payload);
        onSuccess('规格已更新');
      } else {
        await createTileSpec(payload);
        onSuccess('规格已创建');
      }
      onClose();
    } catch (err) {
      setError(getErrorMessage(err, '保存失败'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <section
        className="modal-card tile-spec-modal-card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="tile-spec-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="modal-head">
          <div>
            <h2 id="tile-spec-modal-title" className="modal-title">
              {mode === 'edit' ? '编辑瓷砖规格' : '新增瓷砖规格'}
            </h2>
            <p className="modal-subtitle">尺寸名称由系统根据宽长自动生成</p>
          </div>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </header>
        <div className="modal-body">
          {error ? (
            <p className="form-error" role="alert">
              {error}
            </p>
          ) : null}
          <div className="tile-spec-form-grid">
            <div className="brand-form-item">
              <label>
                宽度 (mm) <span className="req">*</span>
              </label>
              <input
                className="input"
                type="number"
                min={1}
                max={9999}
                value={widthMm}
                onChange={(e) => setWidthMm(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label>
                长度 (mm) <span className="req">*</span>
              </label>
              <input
                className="input"
                type="number"
                min={1}
                max={9999}
                value={lengthMm}
                onChange={(e) => setLengthMm(e.target.value)}
              />
            </div>
            <div className="brand-form-item form-full">
              <label>尺寸名称（只读）</label>
              <div className="tile-spec-readonly">{previewName}</div>
            </div>
            <div className="brand-form-item">
              <label>厚度 (mm)</label>
              <input
                className="input"
                type="number"
                step="0.1"
                min={0}
                value={thicknessMm}
                onChange={(e) => setThicknessMm(e.target.value)}
              />
            </div>
            <div className="brand-form-item">
              <label>
                排序 <span className="req">*</span>
              </label>
              <input
                className="input"
                type="number"
                min={1}
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
              />
            </div>
            <div className="brand-form-item form-full">
              <label>备注</label>
              <textarea
                className="textarea"
                maxLength={200}
                value={remark}
                onChange={(e) => setRemark(e.target.value)}
              />
            </div>
          </div>
        </div>
        <footer className="modal-footer">
          <button type="button" className="btn" onClick={onClose} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            disabled={submitting}
            onClick={() => void handleSubmit()}
          >
            保存
          </button>
        </footer>
      </section>
    </div>
  );
}
