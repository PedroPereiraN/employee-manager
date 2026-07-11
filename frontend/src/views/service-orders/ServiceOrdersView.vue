<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select, { type SelectOption } from '@/components/ui/Select.vue'
import { getServiceOrders } from '@/services/queries'
import type { PaginatedServiceOrder } from '@/utils/api-types'
import { ServiceOrderStatus } from '@/utils/enums'
import {
  CREATE_SERVICE_ORDERS,
  REPORT_SERVICE_ORDER_PROGRESS,
  TIMELINE_SERVICE_ORDER,
  VIEW_SERVICE_ORDERS,
} from '@/utils/paths'
import { useRouter } from 'vue-router'

const router = useRouter()

const page = ref(1)
const pageSize = ref(10)
const searchInput = ref('')
const filter = ref('')
const filterStatus = ref('')

const hasActiveFilters = computed(() => filter.value !== '' || filterStatus.value !== '')

function applySearch() {
  filter.value = searchInput.value
  page.value = 1
}

function clearFilters() {
  searchInput.value = ''
  filter.value = ''
  filterStatus.value = ''
  page.value = 1
}

watch(filterStatus, () => { page.value = 1 })

const { data, isFetching, refetch } = useQuery({
  queryKey: computed(() => ['service-orders', page.value, pageSize.value, filter.value, filterStatus.value]),
  queryFn: () =>
    getServiceOrders({
      page: page.value,
      size: pageSize.value,
      filter: filter.value || undefined,
      filter_status: filterStatus.value || undefined,
    }),
})

const statusOptions: SelectOption[] = [
  { value: '', label: 'All statuses' },
  { value: ServiceOrderStatus.NotStarted, label: 'Not Started' },
  { value: ServiceOrderStatus.Pending, label: 'Pending' },
  { value: ServiceOrderStatus.InProgress, label: 'In Progress' },
  { value: ServiceOrderStatus.Suspended, label: 'Suspended' },
  { value: ServiceOrderStatus.Completed, label: 'Completed' },
  { value: ServiceOrderStatus.Cancelled, label: 'Cancelled' },
]

const columns: Column<PaginatedServiceOrder>[] = [
  { key: 'status', label: 'Status' },
  { key: 'order_number', label: 'Order #' },
  { key: 'service_type', label: 'Service Type' },
  { key: 'work_sessions_quantity', label: 'Sessions' },
  { key: 'created_at', label: 'Created at' },
  { key: 'updated_at', label: 'Last updated' },
  { key: 'actions', label: 'Actions' },
]

const statusConfig: Record<ServiceOrderStatus, { label: string; dot: string; text: string }> = {
  [ServiceOrderStatus.NotStarted]: { label: 'Not Started', dot: 'bg-gray-400', text: 'text-gray-500' },
  [ServiceOrderStatus.Pending]: { label: 'Pending', dot: 'bg-yellow-500', text: 'text-yellow-600' },
  [ServiceOrderStatus.InProgress]: { label: 'In Progress', dot: 'bg-blue-500', text: 'text-blue-600' },
  [ServiceOrderStatus.Suspended]: { label: 'Suspended', dot: 'bg-orange-500', text: 'text-orange-600' },
  [ServiceOrderStatus.Completed]: { label: 'Completed', dot: 'bg-green-500', text: 'text-green-600' },
  [ServiceOrderStatus.Cancelled]: { label: 'Cancelled', dot: 'bg-red-500', text: 'text-red-600' },
}

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: PaginatedServiceOrder) => router.push(VIEW_SERVICE_ORDERS(row.id))
const onDelete = (row: PaginatedServiceOrder) => console.log('delete', row)

const rowActions: RowAction[] = [
  { key: 'view', label: 'View', icon: 'lucide:eye' },
  { key: 'report', label: 'Report Progress', icon: 'lucide:send' },
  { key: 'timeline', label: 'Timeline', icon: 'lucide:git-branch' },
  { key: 'delete', label: 'Delete', icon: 'lucide:trash-2', variant: 'danger' },
]

const onAction = (key: string, row: PaginatedServiceOrder) => {
  if (key === 'view') onView(row)
  else if (key === 'report') router.push(REPORT_SERVICE_ORDER_PROGRESS(row.id))
  else if (key === 'timeline') router.push(TIMELINE_SERVICE_ORDER(row.id))
  else if (key === 'delete') onDelete(row)
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Service Orders</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all service orders in your organization.</p>
      </div>
      <Button :to="CREATE_SERVICE_ORDERS" icon="lucide:plus">New service order</Button>
    </div>

    <!-- Filters -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <form class="flex gap-2" @submit.prevent="applySearch">
        <Input v-model="searchInput" placeholder="Search by order number…" class="w-64" />
        <Button type="submit" variant="secondary" icon="lucide:search">Search</Button>
      </form>

      <Select v-model="filterStatus" :options="statusOptions" placeholder="All statuses" />

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
          <span
            class="inline-block size-2.5 rounded-full"
            :class="statusConfig[value as ServiceOrderStatus]?.dot"
          />
          <span class="text-sm font-medium" :class="statusConfig[value as ServiceOrderStatus]?.text">
            {{ statusConfig[value as ServiceOrderStatus]?.label }}
          </span>
        </div>
      </template>

      <template #service_type="{ value }">
        {{ value ? (value as PaginatedServiceOrder['service_type'])?.name : '—' }}
      </template>

      <template #created_at="{ value }">
        {{ value ? formatDate(value as unknown as string) : '' }}
      </template>

      <template #updated_at="{ value }">
        {{ value ? formatDate(value as unknown as string) : '—' }}
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
