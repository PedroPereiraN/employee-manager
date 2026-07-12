<script setup lang="ts" generic="T extends Record<string, any>">
import { computed, ref, useSlots } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import type { PaginatedResponse } from '@/utils/api-types'

interface Props {
  columns: Column<T>[]
  queryKey: string[]
  queryFn: (params: { page: number; size: number; filter?: string }) => Promise<PaginatedResponse<T>>
  displayValue?: string
  placeholder?: string
  getLabel?: (item: T) => string
  getValue?: (item: T) => string
  disabled?: boolean
  searchPlaceholder?: string
  modalTitle?: string
}

const props = defineProps<Props>()
const slots = useSlots()

const model = defineModel<string>()

const isOpen = ref(false)
const selectedLabel = ref<string | undefined>(undefined)

// Show the last selected label, or the display value from parent (for edit pre-fill), or placeholder
const displayText = computed(() => {
  if (selectedLabel.value !== undefined) return selectedLabel.value
  if (props.displayValue) return props.displayValue
  return null
})

// Modal table state
const page = ref(1)
const pageSize = ref(10)
const searchInput = ref('')
const filter = ref('')

function applySearch() {
  filter.value = searchInput.value
  page.value = 1
}

const { data, isFetching, refetch } = useQuery({
  queryKey: computed(() => [...props.queryKey, '__selector__', page.value, pageSize.value, filter.value]),
  queryFn: () =>
    props.queryFn({ page: page.value, size: pageSize.value, filter: filter.value || undefined }),
  enabled: computed(() => isOpen.value),
})

const internalColumns = computed<Column<T>[]>(() => [
  ...props.columns,
  { key: '__select__' as keyof T & string, label: '' },
])

function getItemLabel(item: T): string {
  return props.getLabel?.(item) ?? (item as any).name ?? String((item as any).id ?? '')
}

function getItemValue(item: T): string {
  return props.getValue?.(item) ?? String((item as any).id ?? '')
}

function open() {
  if (props.disabled) return
  isOpen.value = true
}

function close() {
  isOpen.value = false
  searchInput.value = ''
  filter.value = ''
  page.value = 1
}

function selectItem(item: T) {
  model.value = getItemValue(item)
  selectedLabel.value = getItemLabel(item)
  close()
}
</script>

<template>
  <!-- Trigger button — matches Select component styling -->
  <button
    type="button"
    class="flex items-center justify-between w-full gap-2 px-3 py-1.5 rounded-lg border border-gray-200 bg-white text-sm transition-colors cursor-pointer"
    :class="
      disabled
        ? 'bg-gray-50 text-gray-400 border-gray-300 cursor-not-allowed select-none'
        : 'hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 ' +
          (displayText ? 'text-gray-700' : 'text-gray-400')
    "
    :disabled="disabled"
    @click="open"
  >
    <span>{{ displayText ?? placeholder ?? 'Select…' }}</span>
    <Icon icon="lucide:table-2" width="14" height="14" class="text-gray-400 shrink-0" />
  </button>

  <!-- Modal -->
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
        @click.self="close"
      >
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-3xl flex flex-col max-h-[80vh]">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 shrink-0">
            <h2 class="text-lg font-bold text-gray-900">{{ modalTitle ?? 'Select a record' }}</h2>
            <button
              type="button"
              class="text-gray-400 hover:text-gray-600 transition-colors cursor-pointer"
              @click="close"
            >
              <Icon icon="lucide:x" width="18" height="18" />
            </button>
          </div>

          <!-- Filter bar -->
          <div class="px-6 py-3 border-b border-gray-100 flex items-center gap-3 shrink-0">
            <form class="flex gap-2 flex-1" @submit.prevent="applySearch">
              <Input
                v-model="searchInput"
                :placeholder="searchPlaceholder ?? 'Search…'"
                class="flex-1"
              />
              <Button type="submit" variant="secondary" icon="lucide:search">Search</Button>
            </form>
            <button
              type="button"
              class="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer shrink-0"
              @click="() => refetch()"
            >
              <Icon
                icon="lucide:refresh-cw"
                width="16"
                height="16"
                :class="{ 'animate-spin': isFetching }"
              />
              Reload
            </button>
          </div>

          <!-- Table -->
          <div class="flex-1 overflow-y-auto px-6 py-4">
            <DataTable
              v-model:page="page"
              v-model:items-per-page="pageSize"
              :columns="internalColumns"
              :data="data?.items ?? []"
              :total="data?.total ?? 0"
            >
              <!-- Pass through custom column slots from parent, with default fallback -->
              <template v-for="col in columns" :key="col.key" #[col.key]="slotProps">
                <slot v-if="slots[col.key]" :name="col.key" v-bind="slotProps" />
                <template v-else>{{ (slotProps.value as any) ?? '—' }}</template>
              </template>

              <!-- Select action column -->
              <template #__select__="{ row }">
                <Button
                  v-if="row"
                  type="button"
                  variant="secondary"
                  icon="lucide:check"
                  @click="selectItem(row)"
                >
                  Select
                </Button>
              </template>
            </DataTable>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
