<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select, { type SelectOption } from '@/components/ui/Select.vue'
import { getEmployees } from '@/services/queries'
import type { Employee } from '@/utils/api-types'
import { EmployeeStatus, EmployeeType } from '@/utils/enums'
import { CREATE_EMPLOYEES, VIEW_EMPLOYEES } from '@/utils/paths'
import { useRouter } from 'vue-router'

const router = useRouter()

const page = ref(1)
const pageSize = ref(10)
const searchInput = ref('')
const filter = ref('')
const filterStatus = ref('_all')
const filterType = ref('_all')

const hasActiveFilters = computed(
  () => filter.value !== '' || filterStatus.value !== '_all' || filterType.value !== '_all',
)

function applySearch() {
  filter.value = searchInput.value
  page.value = 1
}

function clearFilters() {
  searchInput.value = ''
  filter.value = ''
  filterStatus.value = '_all'
  filterType.value = '_all'
  page.value = 1
}

watch([filterStatus, filterType], () => { page.value = 1 })

const { data, isFetching, refetch } = useQuery({
  queryKey: computed(() => ['employees', page.value, pageSize.value, filter.value, filterStatus.value, filterType.value]),
  queryFn: () =>
    getEmployees({
      page: page.value,
      size: pageSize.value,
      filter: filter.value || undefined,
      filter_status: filterStatus.value !== '_all' ? filterStatus.value : undefined,
      filter_type: filterType.value !== '_all' ? filterType.value : undefined,
    }),
})

const statusOptions: SelectOption[] = [
  { value: '_all', label: 'All statuses' },
  { value: EmployeeStatus.Active, label: 'Active' },
  { value: EmployeeStatus.Inactive, label: 'Inactive' },
  { value: EmployeeStatus.OnVacation, label: 'On Vacation' },
  { value: EmployeeStatus.SickLeave, label: 'Sick Leave' },
]

const typeOptions: SelectOption[] = [
  { value: '_all', label: 'All types' },
  { value: EmployeeType.Independent, label: 'Independent' },
  { value: EmployeeType.Employee, label: 'Employee' },
]

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

const onView = (row: Employee) => router.push(VIEW_EMPLOYEES(row.id))
const onDelete = (row: Employee) => console.log('delete', row)

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
      <Button :to="CREATE_EMPLOYEES" icon="lucide:plus">New employee</Button>
    </div>

    <!-- Filters -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <form class="flex gap-2" @submit.prevent="applySearch">
        <Input v-model="searchInput" placeholder="Search by name…" class="w-64" />
        <Button type="submit" variant="secondary" icon="lucide:search">Search</Button>
      </form>

      <Select v-model="filterStatus" :options="statusOptions" placeholder="All statuses" />
      <Select v-model="filterType" :options="typeOptions" placeholder="All types" />

      <Button v-if="hasActiveFilters" variant="ghost" icon="lucide:x" @click="clearFilters">
        Clear filters
      </Button>

      <button
        type="button"
        class="ml-auto flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer"
        @click="() => refetch()"
      >
        <Icon icon="lucide:refresh-cw" width="16" height="16" :class="{ 'animate-spin': isFetching }" />
        Reload
      </button>
    </div>

    <DataTable
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
