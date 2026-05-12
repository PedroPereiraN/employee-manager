<script setup lang="ts">
import { Icon } from '@iconify/vue'

export type Props = {
  label: string
  id: string
  error?: string
}

const { id, label, error } = defineProps<Props>()
</script>

<template>
  <fieldset class="flex flex-col gap-1 border-none p-0 m-0">
    <label class="text-sm font-medium text-gray-700" :for="id">{{ label }}</label>
    <slot />
    <span class="text-xs text-red-500 flex items-center gap-1" v-if="error">
      <Icon icon="heroicons:exclamation-circle-solid" class="w-3 h-3 shrink-0" />
      {{ error }}
    </span>
  </fieldset>
</template>
