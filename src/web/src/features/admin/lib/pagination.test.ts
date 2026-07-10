import { describe, expect, it } from 'vitest';

import { getPaginationWindow } from './pagination';

describe('getPaginationWindow', () => {
  it('keeps a single page clickable when there is only one page', () => {
    expect(getPaginationWindow(1, 1)).toEqual([1]);
  });

  it('shows every page when total pages are within the visible limit', () => {
    expect(getPaginationWindow(3, 5)).toEqual([1, 2, 3, 4, 5]);
  });

  it('limits clickable page numbers to five around the current page', () => {
    expect(getPaginationWindow(1, 6)).toEqual([1, 2, 3, 4, 5]);
    expect(getPaginationWindow(3, 6)).toEqual([1, 2, 3, 4, 5]);
    expect(getPaginationWindow(4, 6)).toEqual([2, 3, 4, 5, 6]);
    expect(getPaginationWindow(6, 6)).toEqual([2, 3, 4, 5, 6]);
  });

  it('keeps the old admin import path compatible with invalid input handling', () => {
    expect(getPaginationWindow(0, 0)).toEqual([1]);
    expect(getPaginationWindow(99, 3)).toEqual([1, 2, 3]);
    expect(getPaginationWindow(2, 10, 0)).toEqual([2]);
  });
});
