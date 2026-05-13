import { appClient, formClient } from '@/lib/axios'
import type { Employee, PaginatedResponse, PaginatedServiceOrder, Position, ServiceType } from '@/utils/api-types'

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

export const getEmployees = async ({
  page,
  size,
}: {
  page: number
  size: number
}): Promise<PaginatedResponse<Employee>> => {
  const res = await appClient.get<PaginatedResponse<Employee>>('/employee', {
    params: { page, size },
  })
  return res.data
}

export const getServiceTypes = async ({
  page,
  size,
}: {
  page: number
  size: number
}): Promise<PaginatedResponse<ServiceType>> => {
  const res = await appClient.get<PaginatedResponse<ServiceType>>('/service_types', {
    params: { page, size },
  })
  return res.data
}

export const getServiceOrders = async ({
  page,
  size,
}: {
  page: number
  size: number
}): Promise<PaginatedResponse<PaginatedServiceOrder>> => {
  const res = await appClient.get<PaginatedResponse<PaginatedServiceOrder>>('/service_orders', {
    params: { page, size },
  })
  return res.data
}
