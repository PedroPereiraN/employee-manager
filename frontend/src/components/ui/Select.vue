<script setup lang="ts">
import { Icon } from '@iconify/vue'
import {
  SelectContent,
  SelectItem,
  SelectItemIndicator,
  SelectItemText,
  SelectPortal,
  SelectRoot,
  SelectTrigger,
  SelectValue,
  SelectViewport,
} from 'reka-ui'

export type SelectOption = {
  value: string
  label: string
}

defineProps<{
  options: SelectOption[]
  placeholder?: string
}>()

const model = defineModel<string>()
</script>

<template>
  <SelectRoot v-model="model">
    <SelectTrigger
      class="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors cursor-pointer"
    >
      <SelectValue :placeholder="placeholder ?? 'Select…'" />
      <Icon icon="lucide:chevron-down" width="14" height="14" class="text-gray-400 shrink-0" />
    </SelectTrigger>

    <SelectPortal>
      <SelectContent
        position="popper"
        :side-offset="4"
        class="z-50 min-w-[var(--reka-select-trigger-width)] rounded-lg border border-gray-200 bg-white shadow-md overflow-hidden"
      >
        <SelectViewport class="p-1">
          <SelectItem
            v-for="option in options"
            :key="option.value"
            :value="option.value"
            class="flex items-center gap-2 px-3 py-1.5 rounded-md text-sm text-gray-700 cursor-pointer select-none hover:bg-indigo-50 hover:text-indigo-700 data-[highlighted]:bg-indigo-50 data-[highlighted]:text-indigo-700 data-[state=checked]:font-medium outline-none"
          >
            <SelectItemIndicator>
              <Icon icon="lucide:check" width="14" height="14" class="text-indigo-600" />
            </SelectItemIndicator>
            <SelectItemText>{{ option.label }}</SelectItemText>
          </SelectItem>
        </SelectViewport>
      </SelectContent>
    </SelectPortal>
  </SelectRoot>
</template>
