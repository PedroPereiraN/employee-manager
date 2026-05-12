<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const collapsed = ref(false)

const paths: { to: string; label: string; icon: string }[] = [
  { to: '/dashboard', label: 'Dashboard', icon: 'lucide:layout-dashboard' },
  { to: '/positions', label: 'Positions', icon: 'lucide:briefcase' },
  { to: '/service-types', label: 'Service Types', icon: 'lucide:settings-2' },
  { to: '/employees', label: 'Employees', icon: 'lucide:users' },
  { to: '/service-orders', label: 'Service Orders', icon: 'lucide:clipboard-list' },
]
</script>

<template>
  <aside
    id="sidebar"
    aria-label="sidebar"
    :data-collapsed="collapsed"
    class="h-screen sticky top-0 left-0 flex flex-col bg-gray-900 text-gray-100 transition-all duration-300"
    :class="collapsed ? 'w-16' : 'w-60'"
  >
    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-5 border-b border-gray-700/60"
         :class="collapsed ? 'justify-center' : 'justify-between'">
      <div v-if="!collapsed" class="flex items-center gap-2 overflow-hidden">
        <Icon icon="lucide:building-2" class="shrink-0 text-indigo-400" width="22" height="22" />
        <span class="font-semibold text-sm tracking-wide truncate">Employee Manager</span>
      </div>
      <Icon v-else icon="lucide:building-2" class="text-indigo-400" width="22" height="22" />
      <button
        @click="collapsed = !collapsed"
        class="p-1.5 rounded-md text-gray-400 hover:text-gray-100 hover:bg-gray-700/60 transition-colors"
        :class="collapsed ? 'mx-auto' : ''"
        :aria-label="collapsed ? 'Expand sidebar' : 'Collapse sidebar'"
      >
        <Icon :icon="collapsed ? 'lucide:chevron-right' : 'lucide:chevron-left'" width="16" height="16" />
      </button>
    </div>

    <!-- Nav links -->
    <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto overflow-x-hidden">
      <RouterLink
        v-for="path in paths"
        :key="path.to"
        :to="path.to"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-400 hover:text-gray-100 hover:bg-gray-700/60 transition-colors group"
        :class="{ 'justify-center': collapsed }"
        active-class="!text-indigo-300 bg-indigo-500/15 hover:bg-indigo-500/20"
      >
        <Icon
          :icon="path.icon"
          class="shrink-0 transition-colors"
          width="18"
          height="18"
        />
        <span v-if="!collapsed" class="truncate">{{ path.label }}</span>
      </RouterLink>
    </nav>

    <!-- Footer -->
    <div class="px-2 py-3 border-t border-gray-700/60">
      <button
        class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
        :class="{ 'justify-center': collapsed }"
      >
        <Icon icon="lucide:log-out" class="shrink-0" width="18" height="18" />
        <span v-if="!collapsed" class="truncate">Logout</span>
      </button>
    </div>
  </aside>
</template>
