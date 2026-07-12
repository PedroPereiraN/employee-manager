<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Select, { type SelectOption } from '@/components/ui/Select.vue'
import { getUsers } from '@/services/queries'
import type { User } from '@/utils/api-types'
import { UserRole } from '@/utils/enums'
import { CREATE_USERS, VIEW_USERS } from '@/utils/paths'
import { useRouter } from 'vue-router'

const router = useRouter()

const page = ref(1)
const pageSize = ref(10)
const searchInput = ref('')
const filter = ref('')
const filterRole = ref('_all')

const hasActiveFilters = computed(() => filter.value !== '' || filterRole.value !== '_all')

function applySearch() {
  filter.value = searchInput.value
  page.value = 1
}

function clearFilters() {
  searchInput.value = ''
  filter.value = ''
  filterRole.value = '_all'
  page.value = 1
}

watch(filterRole, () => { page.value = 1 })

const { data, isFetching, refetch } = useQuery({
  queryKey: computed(() => ['users', page.value, pageSize.value, filter.value, filterRole.value]),
  queryFn: () =>
    getUsers({
      page: page.value,
      size: pageSize.value,
      filter: filter.value || undefined,
      filter_role: filterRole.value !== '_all' ? filterRole.value : undefined,
    }),
})

const roleOptions: SelectOption[] = [
  { value: '_all', label: 'All roles' },
  { value: UserRole.Admin, label: 'Admin' },
  { value: UserRole.Supervisor, label: 'Supervisor' },
  { value: UserRole.Member, label: 'Member' },
]

const roleConfig: Record<UserRole, { label: string; dot: string; text: string }> = {
  [UserRole.Admin]: { label: 'Admin', dot: 'bg-indigo-500', text: 'text-indigo-600' },
  [UserRole.Supervisor]: { label: 'Supervisor', dot: 'bg-blue-500', text: 'text-blue-600' },
  [UserRole.Member]: { label: 'Member', dot: 'bg-gray-400', text: 'text-gray-500' },
}

const columns: Column<User>[] = [
  { key: 'name', label: 'Name' },
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Role' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: User) => router.push(VIEW_USERS(row.id))
const onDelete = (row: User) => console.log('delete', row)

const rowActions: RowAction[] = [
  { key: 'view', label: 'View', icon: 'lucide:eye' },
  { key: 'delete', label: 'Delete', icon: 'lucide:trash-2', variant: 'danger' },
]

const onAction = (key: string, row: User) => {
  if (key === 'view') onView(row)
  else if (key === 'delete') onDelete(row)
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Users</h1>
        <p class="text-sm text-gray-500 mt-1">Manage all users in your organization.</p>
      </div>
      <Button :to="CREATE_USERS" icon="lucide:plus">New user</Button>
    </div>

    <!-- Filters -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <form class="flex gap-2" @submit.prevent="applySearch">
        <Input v-model="searchInput" placeholder="Search by name or email…" class="w-72" />
        <Button type="submit" variant="secondary" icon="lucide:search">Search</Button>
      </form>

      <Select v-model="filterRole" :options="roleOptions" placeholder="All roles" />

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
      <template #role="{ value }">
        <div v-if="value" class="flex items-center gap-2">
          <span class="inline-block size-2.5 rounded-full" :class="roleConfig[value as UserRole]?.dot" />
          <span class="text-sm font-medium" :class="roleConfig[value as UserRole]?.text">
            {{ roleConfig[value as UserRole]?.label }}
          </span>
        </div>
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
