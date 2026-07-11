<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'

interface Props {
  open: boolean
  title: string
  description?: string
  listPath: string
  secondaryLabel?: string
  secondaryTo?: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  secondary: []
  close: []
}>()

const router = useRouter()
const viewAllBtn = ref<HTMLButtonElement | null>(null)

watch(
  () => props.open,
  (val) => {
    if (val) nextTick(() => viewAllBtn.value?.focus())
  },
)

function handleSecondaryClick() {
  emit('close')
  if (props.secondaryTo) {
    router.push(props.secondaryTo)
  } else {
    emit('secondary')
  }
}

function goToList() {
  emit('close')
  router.push(props.listPath)
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="open"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
      >
        <div
          class="bg-white rounded-2xl shadow-xl w-full max-w-md mx-4 p-8 flex flex-col items-center gap-6"
        >
          <div class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center">
            <Icon icon="lucide:check" width="32" height="32" class="text-green-600" />
          </div>

          <div class="text-center">
            <h2 class="text-xl font-bold text-gray-900">{{ title }}</h2>
            <p v-if="description" class="text-sm text-gray-500 mt-1">{{ description }}</p>
          </div>

          <div class="flex flex-col sm:flex-row gap-3 w-full">
            <button
              type="button"
              class="flex-1 flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold rounded-lg transition-colors cursor-pointer bg-transparent hover:bg-gray-100 active:bg-gray-100 text-gray-700 border border-gray-400"
              @click="handleSecondaryClick"
            >
              <Icon :icon="secondaryTo ? 'lucide:eye' : 'lucide:plus'" width="16" height="16" />
              {{ secondaryLabel ?? 'Create another' }}
            </button>

            <button
              ref="viewAllBtn"
              type="button"
              class="flex-1 flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold rounded-lg transition-colors cursor-pointer bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              @click="goToList"
            >
              <Icon icon="lucide:list" width="16" height="16" />
              View all
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
