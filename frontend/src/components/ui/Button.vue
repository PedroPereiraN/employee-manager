<script setup lang="ts">
import { Icon } from '@iconify/vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  type?: 'button' | 'submit' | 'reset'
  icon?: string
  disabled?: boolean
}

const { variant = 'primary', type = 'button', icon, disabled = false } = defineProps<Props>()

const variantClasses: Record<NonNullable<Props['variant']>, string> = {
  primary: 'bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white',
  secondary: 'bg-white hover:bg-gray-50 active:bg-gray-100 text-gray-700 border border-gray-300',
  danger: 'bg-red-600 hover:bg-red-700 active:bg-red-800 text-white',
  ghost: 'bg-transparent hover:bg-gray-100 active:bg-gray-200 text-gray-700',
}
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-lg transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
    :class="variantClasses[variant]"
  >
    <Icon v-if="icon" :icon="icon" width="16" height="16" />
    <slot />
  </button>
</template>
