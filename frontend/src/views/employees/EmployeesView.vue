<script setup lang="ts">
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import { getEmployees } from '@/services/queries'
import type { Employee } from '@/utils/api-types'
import { EmployeeStatus } from '@/utils/enums'

const page = ref(1)
const pageSize = ref(10)

const { data, isLoading } = useQuery({
  queryKey: ['employees', page, pageSize],
  queryFn: () => getEmployees({ page: page.value, size: pageSize.value }),
})

const columns: Column<Employee>[] = [
  { key: 'status', label: 'Status' },
  { key: 'name', label: 'Name' },
  { key: 'type', label: 'Type' },
  { key: 'position', label: 'Position' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const statusConfig: Record<EmployeeStatus, { label: string; dot: string; text: string }> = {
  [EmployeeStatus.Active]: { label: 'Active', dot: 'bg-green-500', text: 'text-green-600' },
  [EmployeeStatus.Inactive]: { label: 'Inactive', dot: 'bg-gray-400', text: 'text-gray-500' },
  [EmployeeStatus.OnVacation]: { label: 'On Vacation', dot: 'bg-blue-500', text: 'text-blue-600' },
  [EmployeeStatus.SickLeave]: { label: 'Sick Leave', dot: 'bg-yellow-500', text: 'text-yellow-600' },
}

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const formatType = (type: string) =>
  type.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())

const onView = (row: Employee) => {
  console.log('view', row)
}

const onDelete = (row: Employee) => {
  console.log('delete', row)
}

const rowActions: RowAction[] = [
  { key: 'view', label: 'View', icon: 'lucide:eye' },
  { key: 'delete', label: 'Delete', icon: 'lucide:trash-2', variant: 'danger' },
]

const onAction = (key: string, row: Employee) => {
  if (key === 'view') onView(row)
  else if (key === 'delete') onDelete(row)
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Employees</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all employees in your organization.</p>
      </div>

      <Button to="employees/new" icon="lucide:plus">New employee</Button>
    </div>

<div v-if="isLoading" class="flex items-center justify-center py-20 text-gray-400 text-sm">
      Loading...
    </div>

    <DataTable
      v-else
      v-model:page="page"
      v-model:items-per-page="pageSize"
      :columns="columns"
      :data="data?.items ?? []"
      :total="data?.total ?? 0"
    >
      <template #status="{ value }">
        <div v-if="value" class="flex items-center gap-2">
          <span class="inline-block size-2.5 rounded-full" :class="statusConfig[value as EmployeeStatus]?.dot" />
          <span class="text-sm font-medium" :class="statusConfig[value as EmployeeStatus]?.text">
            {{ statusConfig[value as EmployeeStatus]?.label }}
          </span>
        </div>
      </template>

      <template #type="{ value }">
        {{ value ? formatType(value as string) : '' }}
      </template>

      <template #position="{ value }">
        {{ value ? (value as Employee['position']).name : '' }}
      </template>

      <template #created_at="{ value }">
        {{ value ? formatDate(value as unknown as string) : '' }}
      </template>

      <template #actions="{ row }">
        <RowActionsPopover
          v-if="row"
          :actions="rowActions"
          @action="(key: string) => onAction(key, row)"
        />
      </template>
    </DataTable>
  </div>
</template>
