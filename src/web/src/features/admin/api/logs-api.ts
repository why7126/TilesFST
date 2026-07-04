import { api } from '@/features/auth/api/auth-api';
import type { LogDetailData, LogListData, ListLogsApiV1AdminLogsGetParams } from '@/shared/api/generated';

export type LogQuery = ListLogsApiV1AdminLogsGetParams;

export async function fetchLogs(params: LogQuery): Promise<LogListData> {
  const response = await api.listLogsApiV1AdminLogsGet(params);
  if (!response.data.data) {
    throw new Error(response.data.message || '日志列表数据为空');
  }
  return response.data.data;
}

export async function fetchLogDetail(logId: string): Promise<LogDetailData> {
  const response = await api.getLogDetailApiV1AdminLogsLogIdGet(logId);
  if (!response.data.data) {
    throw new Error(response.data.message || '日志详情数据为空');
  }
  return response.data.data;
}
