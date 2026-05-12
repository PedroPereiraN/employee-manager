import { appClient, formClient } from '@/lib/axios'
import type { PaginatedResponse, Position } from '@/utils/api-types'

export const auth = async ({ email, password }: { email: string; password: string }) =>
  formClient.post('/auth/login', {
    username: email,
    password,
  })

export const getPositions = async ({
  page,
  size,
}: {
  page: number
  size: number
}): Promise<PaginatedResponse<Position>> => {
  const res = await appClient.get<PaginatedResponse<Position>>('/positions', {
    params: { page, size },
  })
  return res.data
}
