import { z } from 'zod'

// TODO: Implementar schema completo em IAD-11
// Placeholder schema para validar monorepo setup
export const DemandSchema = z.object({
  id: z.string(),
  title: z.string().min(5).max(200),
  description: z.string().min(10),
})

export type Demand = z.infer<typeof DemandSchema>
