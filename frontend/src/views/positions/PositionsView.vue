<script setup lang="ts">
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import {
  PopoverArrow,
  PopoverContent,
  PopoverPortal,
  PopoverRoot,
  PopoverTrigger,
} from 'reka-ui'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import { getPositions } from '@/services/queries'
import type { Position } from '@/utils/api-types'

const PAGE_SIZE = 10

const page = ref(1)

const { data, isLoading } = useQuery({
  queryKey: ['positions', page],
  queryFn: () => getPositions({ page: page.value, size: PAGE_SIZE }),
})

const columns: Column<Position>[] = [
  { key: 'name', label: 'Name' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: Position) => {
  console.log('view', row)
}

const onDelete = (row: Position) => {
  console.log('delete', row)
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Positions</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all job positions in your organization.</p>
      </div>

      <button
        type="button"
        class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white text-sm font-semibold rounded-lg transition-colors cursor-pointer"
      >
        <Icon icon="lucide:plus" width="16" height="16" />
        New position
      </button>
    </div>

    <div v-if="isLoading" class="flex items-center justify-center py-20 text-gray-400 text-sm">
      Loading...
    </div>

    <DataTable
      v-else
      v-model:page="page"
      :columns="columns"
      :data="data?.items ?? []"
      :total="data?.total ?? 0"
      :items-per-page="PAGE_SIZE"
    >
      <template #created_at="{ value }">
        {{ value ? formatDate(value) : '' }}
      </template>

      <template #actions="{ row }">
        <PopoverRoot v-if="row">
          <PopoverTrigger
            class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors cursor-pointer"
          >
            <Icon icon="lucide:ellipsis" width="16" height="16" />
          </PopoverTrigger>

          <PopoverPortal>
            <PopoverContent
              side="left"
              :side-offset="6"
              class="z-50 w-40 rounded-xl bg-white shadow-lg border border-gray-200 p-1 text-sm outline-none"
            >
              <PopoverArrow class="fill-white" />

              <button
                class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors cursor-pointer"
                @click="onView(row)"
              >
                <Icon icon="lucide:eye" width="15" height="15" />
                View
              </button>

              <button
                class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-red-500 hover:bg-red-50 transition-colors cursor-pointer"
                @click="onDelete(row)"
              >
                <Icon icon="lucide:trash-2" width="15" height="15" />
                Delete
              </button>
            </PopoverContent>
          </PopoverPortal>
        </PopoverRoot>
      </template>
    </DataTable>
  </div>
</template>
