import { useEffect, useState } from 'react';

import { getErrorMessage } from '@/features/auth/api/auth-api';
import type { TileCategoryAdminItem, TileCategoryTreeNode } from '@/shared/api/generated';

import {
  buildParentOptions,
  createCategory,
  updateCategory,
} from '../api/tile-categories-api';

interface CategoryFormModalProps {
  open: boolean;
  mode: 'create' | 'edit';
  category: TileCategoryAdminItem | null;
  tree: TileCategoryTreeNode[];
  defaultParentId: number | null;
  onClose: () => void;
  onSuccess: (message: string) => void;
}

export function CategoryFormModal({
  open,
  mode,
  category,
  tree,
  defaultParentId,
  onClose,
  onSuccess,
}: CategoryFormModalProps) {
  const [parentId, setParentId] = useState<number | null>(null);
  const [name, setName] = useState('');
  const [sortOrder, setSortOrder] = useState('10');
  const [description, setDescription] = useState('');
  const [enabled, setEnabled] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{
    name?: string;
    sortOrder?: string;
  }>({});

  const parentOptions = buildParentOptions(tree);

  useEffect(() => {
    if (!open) return;
    setError(null);
    setFieldErrors({});
    if (mode === 'edit' && category) {
      setName(category.name);
      setSortOrder(String(category.sort_order));
      setDescription(category.description ?? '');
      setParentId(category.parent_id);
    } else {
      setParentId(defaultParentId);
      setName('');
      setSortOrder('10');
      setDescription('');
      setEnabled(true);
    }
  }, [open, mode, category, defaultParentId]);

  if (!open) return null;

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);
    setFieldErrors({});

    const nextFieldErrors: { name?: string; sortOrder?: string } = {};
    const trimmedName = name.trim();
    const trimmedSortOrder = sortOrder.trim();
    if (!trimmedName) {
      nextFieldErrors.name = '类目名称不能为空';
    } else if (trimmedName.length > 10) {
      nextFieldErrors.name = '类目名称不能超过 10 个字符';
    } else if (!/^[A-Za-z0-9\u4e00-\u9fff]+$/.test(trimmedName)) {
      nextFieldErrors.name = '类目名称只能包含中文、英文和数字';
    }
    if (!/^[1-9]\d*$/.test(trimmedSortOrder)) {
      nextFieldErrors.sortOrder = '排序权重必须为正整数';
    }

    if (nextFieldErrors.name || nextFieldErrors.sortOrder) {
      setFieldErrors(nextFieldErrors);
      setSubmitting(false);
      return;
    }
    const sort = Number.parseInt(trimmedSortOrder, 10);

    try {
      if (mode === 'create') {
        await createCategory({
          parent_id: parentId,
          name: trimmedName,
          sort_order: sort,
          description: description.trim() || null,
          status: enabled ? 'ENABLED' : 'DISABLED',
        });
        onSuccess('类目已创建');
      } else if (category) {
        await updateCategory(category.id, {
          name: trimmedName,
          sort_order: sort,
          description: description.trim() || null,
        });
        onSuccess('类目已更新');
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
      <div
        className="category-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="category-form-title"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <span id="category-form-title" className="modal-title">
            {mode === 'create' ? '新增类目' : '编辑类目'}
          </span>
          <button type="button" className="modal-close" aria-label="关闭" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          {mode === 'create' ? (
            <div className="cat-modal-row">
              <label htmlFor="cat-parent">
                上级类目<span className="required-mark" aria-hidden="true">*</span>
              </label>
              <select
                id="cat-parent"
                className="select"
                value={parentId ?? ''}
                onChange={(e) =>
                  setParentId(e.target.value ? Number(e.target.value) : null)
                }
              >
                {parentOptions.map((opt) => (
                  <option key={opt.label} value={opt.id ?? ''}>
                    {opt.label}
                  </option>
                ))}
              </select>
              <p className="cat-modal-help">
                选择上级类目后自动生成层级；当前最多支持二级类目。类目编码由系统自动生成。
              </p>
            </div>
          ) : null}
          <div className="cat-modal-row">
            <label htmlFor="cat-name">
              类目名称<span className="required-mark" aria-hidden="true">*</span>
            </label>
            <input
              id="cat-name"
              className="input"
              value={name}
              placeholder="例如：岩板"
              aria-invalid={Boolean(fieldErrors.name)}
              aria-describedby={fieldErrors.name ? 'cat-name-error' : undefined}
              onChange={(e) => setName(e.target.value)}
            />
            <p className="cat-modal-help">最多 10 个字符，只能包含中文、英文和数字。</p>
            {fieldErrors.name ? (
              <p id="cat-name-error" className="field-error">
                {fieldErrors.name}
              </p>
            ) : null}
          </div>
          <div className="cat-modal-row">
            <label htmlFor="cat-sort">
              排序权重<span className="required-mark" aria-hidden="true">*</span>
            </label>
            <input
              id="cat-sort"
              className="input"
              value={sortOrder}
              placeholder="数字越小越靠前"
              aria-invalid={Boolean(fieldErrors.sortOrder)}
              aria-describedby={fieldErrors.sortOrder ? 'cat-sort-error' : undefined}
              onChange={(e) => setSortOrder(e.target.value)}
            />
            {fieldErrors.sortOrder ? (
              <p id="cat-sort-error" className="field-error">
                {fieldErrors.sortOrder}
              </p>
            ) : null}
          </div>
          <div className="cat-modal-row">
            <label htmlFor="cat-desc">类目描述</label>
            <textarea
              id="cat-desc"
              className="cat-textarea"
              maxLength={200}
              placeholder="面向运营的类目说明，可选"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          {mode === 'create' ? (
            <div className="cat-modal-row">
              <span className="field-label">状态</span>
              <div className="switch-line">
                <button
                  type="button"
                  className={`switch${enabled ? '' : ' off'}`}
                  aria-pressed={enabled}
                  aria-label="新增后立即启用"
                  onClick={() => setEnabled((v) => !v)}
                />
                新增后立即启用
              </div>
            </div>
          ) : null}
          {error ? <p className="form-error">{error}</p> : null}
        </div>
        <div className="modal-footer">
          <button type="button" className="btn" onClick={onClose} disabled={submitting}>
            取消
          </button>
          <button
            type="button"
            className="btn primary"
            onClick={() => void handleSubmit()}
            disabled={submitting}
          >
            保存类目
          </button>
        </div>
      </div>
    </div>
  );
}
