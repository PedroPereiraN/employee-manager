export type Position = {
  id: string
  name: string
  description: string | null
  created_at: string
  updated_at: string | null
  deleted_at: string | null
}

export type PaginatedResponse<T> = {
  items: T[]
  total: number
  page: number
  size: number
}
