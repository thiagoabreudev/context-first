import { z } from 'zod'

// TODO: Implementar schema completo em IAD-11
// Placeholder schema para validar monorepo setup
export const ProjectSchema = z.object({
  id: z.string(),
  name: z.string().min(3).max(100),
  userId: z.string(),
})

export type Project = z.infer<typeof ProjectSchema>
