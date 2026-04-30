export type ExportPayload = {
  filename: string;
  content_type: string;
  content: string;
  record_count: number | null;
};

export type ExportDateRange = {
  date?: string;
  start_date?: string;
  end_date?: string;
};

export function buildExportQuery(params?: ExportDateRange): string {
  if (!params) {
    return "";
  }
  const query = new URLSearchParams();
  if (params.date) {
    query.set("date", params.date);
  }
  if (params.start_date) {
    query.set("start_date", params.start_date);
  }
  if (params.end_date) {
    query.set("end_date", params.end_date);
  }
  const value = query.toString();
  return value ? `?${value}` : "";
}

export function triggerExportDownload(payload: ExportPayload): void {
  const blob = new Blob([payload.content], { type: payload.content_type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = payload.filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

