import { appClient, formClient } from '@/lib/axios'
import type {
  Employee,
  PaginatedResponse,
  PaginatedServiceOrder,
  Position,
  ServiceType,
  User,
} from '@/utils/api-types'

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

export const getPosition = async (id: string): Promise<Position> => {
  const res = await appClient.get<Position>(`/positions/${id}`)
  return res.data
}

export const createPosition = async ({
  name,
  description,
}: {
  name: string
  description?: string | null
}) => {
  const res = await appClient.post('/positions', {
    name,
    description,
  })

  return res.data
}

export const editPosition = async ({
  id,
  name,
  description,
}: {
  id: string
  name?: string | null
  description?: string | null
}) => {
  const res = await appClient.put('/positions', {
    id,
    name,
    description,
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

export const getServiceType = async (id: string): Promise<ServiceType> => {
  const res = await appClient.get<ServiceType>(`/service_types/${id}`)
  return res.data
}

export const createServiceType = async ({
  name,
  description,
}: {
  name: string
  description?: string | null
}) => {
  const res = await appClient.post('/service_types', { name, description })
  return res.data
}

export const editServiceType = async ({
  id,
  name,
  description,
}: {
  id: string
  name?: string | null
  description?: string | null
}) => {
  const res = await appClient.put('/service_types', { id, name, description })
  return res.data
}

export const getEmployee = async (id: string): Promise<Employee> => {
  const res = await appClient.get<Employee>(`/employee/${id}`)
  return res.data
}

export const createEmployee = async (data: {
  name: string
  birthday?: string | null
  phone?: string | null
  email?: string | null
  admission_date?: string | null
  status: string
  type: string
  payment_method: string
  payment_value: number
  hourly_rate?: number | null
  hourly_bonus?: number | null
  observations?: string | null
  position_id: string
}) => {
  const res = await appClient.post('/employee', data)
  return res.data
}

export const editEmployee = async (data: {
  id: string
  name?: string | null
  birthday?: string | null
  phone?: string | null
  email?: string | null
  admission_date?: string | null
  status?: string | null
  type?: string | null
  payment_method?: string | null
  payment_value?: number | null
  hourly_rate?: number | null
  hourly_bonus?: number | null
  observations?: string | null
  position_id?: string | null
}) => {
  const res = await appClient.put('/employee', data)
  return res.data
}

export const getUsers = async ({
  page,
  size,
}: {
  page: number
  size: number
}): Promise<PaginatedResponse<User>> => {
  const res = await appClient.get<PaginatedResponse<User>>('/users', {
    params: { page, size },
  })
  return res.data
}

export const getUser = async (id: string): Promise<User> => {
  const res = await appClient.get<User>(`/users/${id}`)
  return res.data
}

export const createUser = async (data: {
  name: string
  email: string
  role: string
  password?: string
}) => {
  const res = await appClient.post('/users', data)
  return res.data
}

export const editUser = async (data: {
  id: string
  name?: string
  email?: string
  role?: string
  password?: string
}) => {
  const res = await appClient.put('/users', data)
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
