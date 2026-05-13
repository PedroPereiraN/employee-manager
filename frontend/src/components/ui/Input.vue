<script setup lang="ts">
const model = defineModel()
</script>

<template>
  <input
    class="w-full px-4 py-2.5 rounded-lg border border-gray-400 bg-gray-100 text-gray-900 text-sm placeholder:text-gray-400 transition-all duration-200 focus:outline-none focus:bg-white focus:ring-3 disabled:bg-gray-50 disabled:text-gray-400 disabled:border-gray-300 disabled:cursor-not-allowed disabled:select-none"
    v-model="model"
  />
</template>
