<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import { getServiceTypes } from '@/services/queries'
import type { ServiceType } from '@/utils/api-types'
import { CREATE_SERVICE_TYPES, VIEW_SERVICE_TYPES } from '@/utils/paths'
import { useRouter } from 'vue-router'

const router = useRouter()

const page = ref(1)
const pageSize = ref(10)
const searchInput = ref('')
const filter = ref('')

const hasActiveFilters = computed(() => filter.value !== '')

function applySearch() {
  filter.value = searchInput.value
  page.value = 1
}

function clearFilters() {
  searchInput.value = ''
  filter.value = ''
  page.value = 1
}

watch(filter, () => { page.value = 1 })

const { data, isFetching, refetch } = useQuery({
  queryKey: computed(() => ['service-types', page.value, pageSize.value, filter.value]),
  queryFn: () => getServiceTypes({ page: page.value, size: pageSize.value, filter: filter.value || undefined }),
})

const columns: Column<ServiceType>[] = [
  { key: 'name', label: 'Name' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: ServiceType) => router.push(VIEW_SERVICE_TYPES(row.id))
const onDelete = (row: ServiceType) => console.log('delete', row)

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

    <!-- Filters -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <form class="flex gap-2" @submit.prevent="applySearch">
        <Input v-model="searchInput" placeholder="Search by name…" class="w-64" />
        <Button type="submit" variant="secondary" icon="lucide:search">Search</Button>
      </form>

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
