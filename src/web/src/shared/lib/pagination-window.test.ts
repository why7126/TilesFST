import { describe, expect, it } from 'vitest';

import { getPaginationWindow } from './pagination-window';

describe('getPaginationWindow', () => {
  it('keeps a single page clickable when there is only one page', () => {
    expect(getPaginationWindow(1, 1)).toEqual([1]);
  });

  it('shows every page when total pages are within the visible limit', () => {
    expect(getPaginationWindow(3, 5)).toEqual([1, 2, 3, 4, 5]);
  });

  it('uses a beginning window near the first page', () => {
    expect(getPaginationWindow(1, 6)).toEqual([1, 2, 3, 4, 5]);
    expect(getPaginationWindow(3, 6)).toEqual([1, 2, 3, 4, 5]);
  });

  it('uses a centered window away from boundaries', () => {
    expect(getPaginationWindow(5, 9)).toEqual([3, 4, 5, 6, 7]);
  });

  it('uses an ending window near the final page', () => {
    expect(getPaginationWindow(6, 6)).toEqual([2, 3, 4, 5, 6]);
  });

  it('supports custom maxVisible values when valid', () => {
    expect(getPaginationWindow(5, 9, 3)).toEqual([4, 5, 6]);
  });

  it('normalizes invalid input without throwing', () => {
    expect(getPaginationWindow(0, 0)).toEqual([1]);
    expect(getPaginationWindow(99, 3)).toEqual([1, 2, 3]);
    expect(getPaginationWindow(Number.NaN, Number.NaN)).toEqual([1]);
    expect(getPaginationWindow(2, 10, 0)).toEqual([2]);
  });
});
