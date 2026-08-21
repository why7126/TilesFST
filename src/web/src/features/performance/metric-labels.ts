export const performanceMetricOptions = [
  { value: 'first_content_ready', label: '首屏可用' },
  { value: 'full_load', label: '完整加载' },
  { value: 'first_api_done', label: '首个接口完成' },
  { value: 'dom_content_loaded', label: 'DOM 加载完成' },
  { value: 'app_launch_ready', label: '小程序启动就绪' },
  { value: 'api_duration', label: '接口请求耗时' },
  { value: 'api_failed_duration', label: '接口失败耗时' },
] as const;

const performanceMetricLabels = Object.fromEntries(
  performanceMetricOptions.map((option) => [option.value, option.label]),
) as Record<string, string>;

export function performanceMetricLabel(value: string): string {
  return performanceMetricLabels[value] ?? value;
}
