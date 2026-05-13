import type {
  EmployeeStatus,
  EmployeeType,
  PaymentMethod,
  UserRole,
  ServiceOrderStatus,
  WorkSessionStatus,
} from './enums'

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

export type Employee = {
  id: string
  name: string
  birthday: string | null
  phone: string | null
  email: string | null
  admission_date: string | null
  status: EmployeeStatus
  type: EmployeeType
  payment_method: PaymentMethod
  payment_value: number
  hourly_rate: number | null
  hourly_bonus: number | null
  observations: string | null
  position: Position
  created_at: string
  updated_at: string | null
  deleted_at: string | null
}

export type ServiceType = {
  id: string
  name: string
  description: string | null
  created_at: string
  updated_at: string | null
  deleted_at: string | null
}

export type User = {
  id: string
  name: string
  email: string
  role: UserRole
  created_at: string
  updated_at: string | null
  deleted_at: string | null
}

export type PaginatedServiceOrder = {
  id: string
  order_number: string
  status: ServiceOrderStatus
  description: string | null
  started_at: string | null
  finished_at: string | null
  total_hours: number | null
  service_type: ServiceType | null
  created_at: string
  updated_at: string | null
  deleted_at: string | null
  work_sessions_quantity: number
}

export type ServiceOrderStatusHistory = {
  id: string
  service_order_id: string
  reason: string | null
  status: ServiceOrderStatus
  created_at: string
}

export type WorkSessionHistory = {
  id: string
  work_session_id: string
  status: WorkSessionStatus
  observations: string | null
  occurred_at: string
  created_at: string
}

export type WorkSession = {
  id: string
  service_order_id: string
  employee: Employee
  created_at: string
  updated_at: string | null
  deleted_at: string | null
  histories: WorkSessionHistory[]
}

export type ServiceOrder = {
  id: string
  order_number: string
  status: ServiceOrderStatus
  description: string | null
  started_at: string | null
  finished_at: string | null
  total_hours: number | null
  service_type: ServiceType | null
  created_at: string
  updated_at: string | null
  deleted_at: string | null
  work_sessions: WorkSession[]
  status_histories: ServiceOrderStatusHistory[]
}
