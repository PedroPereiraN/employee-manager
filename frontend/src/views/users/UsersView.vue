<script setup lang="ts">
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import DataTable, { type Column } from '@/components/ui/DataTable.vue'
import RowActionsPopover, { type RowAction } from '@/components/ui/RowActionsPopover.vue'
import Button from '@/components/ui/Button.vue'
import { getUsers } from '@/services/queries'
import type { User } from '@/utils/api-types'
import { UserRole } from '@/utils/enums'
import { CREATE_USERS, VIEW_USERS } from '@/utils/paths'
import { useRouter } from 'vue-router'

const router = useRouter()

const page = ref(1)
const pageSize = ref(10)

const { data, isLoading } = useQuery({
  queryKey: ['users', page, pageSize],
  queryFn: () => getUsers({ page: page.value, size: pageSize.value }),
})

const columns: Column<User>[] = [
  { key: 'name', label: 'Name' },
  { key: 'email', label: 'Email' },
  { key: 'role', label: 'Role' },
  { key: 'created_at', label: 'Created at' },
  { key: 'actions', label: 'Actions' },
]

const roleConfig: Record<UserRole, { label: string; dot: string; text: string }> = {
  [UserRole.Admin]: { label: 'Admin', dot: 'bg-indigo-500', text: 'text-indigo-600' },
  [UserRole.Supervisor]: { label: 'Supervisor', dot: 'bg-blue-500', text: 'text-blue-600' },
  [UserRole.Member]: { label: 'Member', dot: 'bg-gray-400', text: 'text-gray-500' },
}

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(iso))

const onView = (row: User) => {
  router.push(VIEW_USERS(row.id))
}

const onDelete = (row: User) => {
  console.log('delete', row)
}

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
