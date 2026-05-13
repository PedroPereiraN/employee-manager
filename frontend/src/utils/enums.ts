export enum EmployeeStatus {
  Active = 'active',
  Inactive = 'inactive',
  OnVacation = 'on_vacation',
  SickLeave = 'sick_leave',
}

export enum EmployeeType {
  Independent = 'independent',
  Employee = 'employee',
}

export enum PaymentMethod {
  Monthly = 'monthly',
  Weekly = 'weekly',
  Daily = 'daily',
}

export enum UserRole {
  Admin = 'admin',
  Supervisor = 'supervisor',
  Member = 'member',
}

export enum ServiceOrderStatus {
  InProgress = 'in_progress',
  Pending = 'pending',
  NotStarted = 'not_started',
  Suspended = 'suspended',
  Completed = 'completed',
  Cancelled = 'cancelled',
}

export enum WorkSessionStatus {
  Started = 'started',
  Paused = 'paused',
  Resumed = 'resumed',
  Completed = 'completed',
  Stopped = 'stopped',
}
