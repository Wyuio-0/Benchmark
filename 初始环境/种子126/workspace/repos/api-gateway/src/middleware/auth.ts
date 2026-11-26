export interface RequestLike {
  path: string;
  headers: Record<string, string | undefined>;
}

export const PUBLIC_PREFIXES: string[] = [
  "/healthz",
  "/readyz",
  "/public/docs",
];

export const PUBLIC_EXACT_PATHS: string[] = [];

export function isPublicRequest(req: RequestLike): boolean {
  if (PUBLIC_EXACT_PATHS.includes(req.path)) {
    return true;
  }
  return PUBLIC_PREFIXES.some((prefix) => req.path.startsWith(prefix));
}

export function requireAuth(req: RequestLike): { allowed: boolean; reason?: string } {
  if (isPublicRequest(req)) {
    return { allowed: true };
  }
  const token = req.headers["authorization"];
  if (!token || !token.startsWith("Bearer ")) {
    return { allowed: false, reason: "missing_bearer_token" };
  }
  return { allowed: true };
}
