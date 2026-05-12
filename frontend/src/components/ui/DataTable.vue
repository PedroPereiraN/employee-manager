<script setup lang="ts" generic="T extends Record<string, any>">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import {
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
  PaginationRoot,
} from 'reka-ui'
import Select, { type SelectOption } from '@/components/ui/Select.vue'

export type Column<T> = {
  key: (keyof T & string) | string
  label: string
}

const PAGE_SIZE_OPTIONS: SelectOption[] = [
  { value: '5', label: '5' },
  { value: '10', label: '10' },
  { value: '20', label: '20' },
  { value: '50', label: '50' },
]

const props = defineProps<{
  columns: Column<T>[]
  data: T[]
  total: number
}>()

const page = defineModel<number>('page', { default: 1 })
const itemsPerPage = defineModel<number>('itemsPerPage', { default: 10 })

const pageSizeString = computed({
  get: () => String(itemsPerPage.value),
  set: (val: string) => {
    itemsPerPage.value = Number(val)
    page.value = 1
  },
})

const rangeStart = computed(() =>
  props.total === 0 ? 0 : (page.value - 1) * itemsPerPage.value + 1,
)
const rangeEnd = computed(() => Math.min(page.value * itemsPerPage.value, props.total))
const fillerCount = computed(() => Math.max(0, itemsPerPage.value - props.data.length))
</script>

<template>
  <div class="flex flex-col gap-4">
    <!-- Table -->
    <div class="rounded-xl border border-gray-200 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th
              v-for="col in props.columns"
              :key="col.key"
              class="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider"
            >
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr v-if="props.data.length === 0 && fillerCount === 0">
            <td :colspan="props.columns.length" class="px-4 py-10 text-center text-gray-400">
              No records found.
            </td>
          </tr>
          <tr
            v-for="(row, rowIndex) in props.data"
            :key="rowIndex"
            class="hover:bg-gray-50 transition-colors"
          >
            <td v-for="col in props.columns" :key="col.key" class="px-4 py-3 text-gray-700">
              <slot :name="col.key" :value="row[col.key]" :row="row">
                {{ row[col.key] ?? '—' }}
              </slot>
            </td>
          </tr>
          <!-- Filler rows to keep table height consistent -->
          <tr v-for="i in fillerCount" :key="`filler-${i}`" class="pointer-events-none select-none">
            <td v-for="col in props.columns" :key="col.key" class="px-4 py-3">&nbsp;</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between text-sm text-gray-500">
      <span>
        {{
          props.total === 0
            ? 'No results'
            : `Showing ${rangeStart}–${rangeEnd} of ${props.total} result${props.total === 1 ? '' : 's'}`
        }}
      </span>

      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2">
          <span>Rows per page</span>
          <Select v-model="pageSizeString" :options="PAGE_SIZE_OPTIONS" />
        </div>

        <PaginationRoot
          v-model:page="page"
          :total="props.total"
          :items-per-page="itemsPerPage"
          :sibling-count="1"
          show-edges
        >
          <PaginationList v-slot="{ items }" class="flex items-center gap-1">
            <PaginationFirst
              class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
            >
              <Icon icon="lucide:chevrons-left" width="14" height="14" />
            </PaginationFirst>

            <PaginationPrev
              class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
            >
              <Icon icon="lucide:chevron-left" width="14" height="14" />
            </PaginationPrev>

            <template
              v-for="(item, index) in items"
              :key="item.type === 'page' ? item.value : `ellipsis-${index}`"
            >
              <PaginationListItem
                v-if="item.type === 'page'"
                :value="item.value"
                class="w-8 h-8 flex items-center justify-center rounded-lg border text-sm font-medium transition-colors cursor-pointer"
                :class="
                  item.value === page
                    ? 'border-indigo-500 bg-indigo-500 text-white'
                    : 'border-gray-200 text-gray-600 hover:bg-gray-100'
                "
              >
                {{ item.value }}
              </PaginationListItem>

              <PaginationEllipsis
                v-else
                :key="index"
                :index="index"
                class="w-8 h-8 flex items-center justify-center text-gray-400 select-none"
              >
                &#8230;
              </PaginationEllipsis>
            </template>

            <PaginationNext
              class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
            >
              <Icon icon="lucide:chevron-right" width="14" height="14" />
            </PaginationNext>

            <PaginationLast
              class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-100 hover:text-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
            >
              <Icon icon="lucide:chevrons-right" width="14" height="14" />
            </PaginationLast>
          </PaginationList>
        </PaginationRoot>
      </div>
    </div>
  </div>
</template>
