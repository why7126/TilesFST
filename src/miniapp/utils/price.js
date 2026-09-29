// Price display only: preserve valid formatted values; never calculate a quote.
function pricePresentation(value, available = true) {
  if (!available) return { text: '暂不可查看', state: 'unavailable' };
  const text = typeof value === 'string' ? value.trim() : '';
  const missing = ['', 'null', 'undefined', '暂无', '暂无参考价', '价格待维护'];
  if (missing.includes(text)) return { text: '暂无', state: 'empty' };
  // Accept the existing currency/decimal format, including grouped thousands.
  const match = text.match(/^[¥￥]?\s*(-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?)$/);
  const amount = match ? Number(match[1].replace(/,/g, '')) : NaN;
  if (Number.isFinite(amount) && amount <= 0) return { text: '暂无', state: 'empty' };
  return { text, state: Number.isFinite(amount) && amount > 0 ? 'valid' : 'empty' };
}

module.exports = { pricePresentation };
