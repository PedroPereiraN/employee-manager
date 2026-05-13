<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { RouterLink } from 'vue-router'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost'
  type?: 'button' | 'submit' | 'reset'
  icon?: string
  disabled?: boolean
  to?: string | object
}

const { variant = 'primary', type = 'button', icon, disabled = false, to } = defineProps<Props>()

const variantClasses: Record<NonNullable<Props['variant']>, string> = {
  primary: 'bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white',
  secondary: 'bg-white hover:bg-gray-50 active:bg-gray-100 text-gray-700 border border-gray-300',
  outline:
    'bg-transparent hover:bg-gray-100 active:bg-gray-100 text-gray-700 border border-gray-400',
  danger: 'bg-red-600 hover:bg-red-700 active:bg-red-800 text-white',
  ghost: 'bg-transparent hover:bg-gray-100 active:bg-gray-200 text-gray-700',
}
</script>

<template>
  <component
    :is="to ? RouterLink : 'button'"
    :to="to"
    :type="to ? undefined : type"
    :disabled="to ? undefined : disabled"
    class="flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-lg transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
    :class="variantClasses[variant]"
  >
    <Icon v-if="icon" :icon="icon" width="16" height="16" />
    <slot />
  </component>
</template>
