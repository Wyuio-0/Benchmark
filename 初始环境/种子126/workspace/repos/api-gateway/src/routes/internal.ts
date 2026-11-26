export interface RouteDef {
  method: "GET" | "POST";
  path: string;
  requiredRole: string;
  handler: string;
}

export const internalRoutes: RouteDef[] = [
  {
    method: "GET",
    path: "/internal/metrics",
    requiredRole: "metrics_reader",
    handler: "collectPrometheusMetrics",
  },
  {
    method: "POST",
    path: "/internal/impersonate-token",
    requiredRole: "super_admin",
    handler: "issueCustomerImpersonationToken",
  },
  {
    method: "GET",
    path: "/internal/export-pii",
    requiredRole: "compliance_officer",
    handler: "exportCustomerRealnameDataset",
  },
];
