import { z } from 'zod'

// TODO: Implementar schema completo em IAD-11
// Placeholder schema para validar monorepo setup
export const MetaspecSchema = z.object({
  id: z.string(),
  name: z.string(),
  content: z.string(),
})

export type Metaspec = z.infer<typeof MetaspecSchema>
