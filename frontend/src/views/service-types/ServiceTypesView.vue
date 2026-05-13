<script setup lang="ts">
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import { getServiceTypes } from '@/services/queries'
import type { ServiceType } from '@/utils/api-types'
import { CREATE_SERVICE_TYPES } from '@/utils/paths'

const page = ref(1)
const pageSize = ref(10)

const { data, isLoading } = useQuery({
  queryKey: ['service-types', page, pageSize],
  queryFn: () => getServiceTypes({ page: page.value, size: pageSize.value }),
})

const columns: Column<ServiceType>[] = [
  { key: 'name', label: 'Name' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: ServiceType) => {
  console.log('view', row)
}

const onDelete = (row: ServiceType) => {
  console.log('delete', row)
}

const rowActions: RowAction[] = [
  { key: 'view', label: 'View', icon: 'lucide:eye' },
  { key: 'delete', label: 'Delete', icon: 'lucide:trash-2', variant: 'danger' },
]

const onAction = (key: string, row: ServiceType) => {
  if (key === 'view') onView(row)
  else if (key === 'delete') onDelete(row)
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Service Types</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all service types in your organization.</p>
      </div>

      <Button :to="CREATE_SERVICE_TYPES" icon="lucide:plus">New service type</Button>
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
