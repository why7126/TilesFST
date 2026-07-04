export function getPaginationWindow(currentPage: number, totalPages: number, maxVisible = 5) {
  const safeTotal = Math.max(1, totalPages);
  const safeCurrent = Math.min(Math.max(1, currentPage), safeTotal);
  const windowSize = Math.max(1, Math.min(maxVisible, safeTotal));
  const half = Math.floor(windowSize / 2);

  let start = safeCurrent - half;
  let end = start + windowSize - 1;

  if (start < 1) {
    start = 1;
    end = windowSize;
  }

  if (end > safeTotal) {
    end = safeTotal;
    start = Math.max(1, end - windowSize + 1);
  }

  return Array.from({ length: end - start + 1 }, (_, index) => start + index);
}
