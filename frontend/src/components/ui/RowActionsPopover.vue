<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { PopoverArrow, PopoverContent, PopoverPortal, PopoverRoot, PopoverTrigger } from 'reka-ui'

export type RowAction = {
  key: string
  label: string
  icon: string
  variant?: 'default' | 'danger'
}

defineProps<{
  actions: RowAction[]
}>()

const emit = defineEmits<{
  action: [key: string]
}>()
</script>

<template>
  <PopoverRoot>
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
          v-for="action in actions"
          :key="action.key"
          class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg transition-colors cursor-pointer"
          :class="
            action.variant === 'danger'
              ? 'text-red-500 hover:bg-red-50'
              : 'text-gray-600 hover:bg-gray-100'
          "
          @click="emit('action', action.key)"
        >
          <Icon :icon="action.icon" width="15" height="15" />
          {{ action.label }}
        </button>
      </PopoverContent>
    </PopoverPortal>
  </PopoverRoot>
</template>
