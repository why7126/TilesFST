import { api } from '@/features/auth/api/auth-api';
import type {
  GetLogObservabilityApiV1AdminLogsObservabilityGetParams,
  LogDetailData,
  LogListData,
  LogObservabilityData,
  ListLogsApiV1AdminLogsGetParams,
} from '@/shared/api/generated';

export type LogQuery = ListLogsApiV1AdminLogsGetParams;
export type LogObservabilityQuery = GetLogObservabilityApiV1AdminLogsObservabilityGetParams;

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

export async function fetchLogObservability(params: LogObservabilityQuery): Promise<LogObservabilityData> {
  const response = await api.getLogObservabilityApiV1AdminLogsObservabilityGet(params);
  if (!response.data.data) {
    throw new Error(response.data.message || '日志观测数据为空');
  }
  return response.data.data;
}
