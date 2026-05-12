<script setup lang="ts">
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
      <svg class="w-3 h-3 shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      {{ error }}
    </span>
  </fieldset>
</template>
