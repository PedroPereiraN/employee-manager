export const POSITIONS = '/positions'
export const CREATE_POSITIONS = '/positions/new'
export const VIEW_POSITIONS = (id: string) => `/positions/${id}`

export const SERVICE_TYPES = '/service-types'
export const CREATE_SERVICE_TYPES = '/service-types/new'
export const VIEW_SERVICE_TYPES = (id: string) => `/service-types/${id}`

export const USERS = '/users'
export const CREATE_USERS = '/users/new'
export const VIEW_USERS = (id: string) => `/users/${id}`

export const EMPLOYEES = '/employees'
export const CREATE_EMPLOYEES = '/employees/new'
export const VIEW_EMPLOYEES = (id: string) => `/employees/${id}`

export const SERVICE_ORDERS = '/service-orders'
export const CREATE_SERVICE_ORDERS = '/service-orders/new'
export const VIEW_SERVICE_ORDERS = (id: string) => `/service-orders/${id}`
export const REPORT_SERVICE_ORDER_PROGRESS = (id: string) => `/service-orders/${id}/report-progress`
export const TIMELINE_SERVICE_ORDER = (id: string) => `/service-orders/${id}/timeline`
