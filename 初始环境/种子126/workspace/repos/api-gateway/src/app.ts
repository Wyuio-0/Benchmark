import { requireAuth } from "./middleware/auth";
import { internalRoutes } from "./routes/internal";

export function listRegisteredInternalPaths(): string[] {
  return internalRoutes.map((r) => `${r.method} ${r.path}`);
}

export { requireAuth };
