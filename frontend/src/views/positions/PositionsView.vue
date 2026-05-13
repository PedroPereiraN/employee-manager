<script setup lang="ts">
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import { getPositions } from '@/services/queries'
import type { Position } from '@/utils/api-types'
import { useRouter } from 'vue-router'

const router = useRouter()

const page = ref(1)
const pageSize = ref(10)

const { data, isLoading } = useQuery({
  queryKey: ['positions', page, pageSize],
  queryFn: () => getPositions({ page: page.value, size: pageSize.value }),
})

const columns: Column<Position>[] = [
  { key: 'name', label: 'Name' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: Position) => {
  router.push(`/positions/${row.id}`)
}

const onDelete = (row: Position) => {
  console.log('delete', row)
}

const rowActions: RowAction[] = [
  { key: 'view', label: 'View', icon: 'lucide:eye' },
  { key: 'delete', label: 'Delete', icon: 'lucide:trash-2', variant: 'danger' },
]

const onAction = (key: string, row: Position) => {
  if (key === 'view') onView(row)
  else if (key === 'delete') onDelete(row)
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Positions</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all job positions in your organization.</p>
      </div>

      <Button to="positions/new" icon="lucide:plus">New position</Button>
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
