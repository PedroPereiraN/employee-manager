<script setup lang="ts">
import { computed, ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { getServiceOrderOverview } from '@/services/queries'
import { ServiceOrderStatus } from '@/utils/enums'
import { Icon } from '@iconify/vue'

// ─── Date helpers ─────────────────────────────────────────────────────────────

const toDateInput = (d: Date) => {
  const offset = d.getTimezoneOffset() * 60000
  return new Date(d.getTime() - offset).toISOString().slice(0, 10)
}

// ─── Date range state ─────────────────────────────────────────────────────────

type Period = '1w' | '1m' | '3m' | null

const activePeriod = ref<Period>('1w')

const now = new Date()
const defaultFrom = new Date()
defaultFrom.setDate(now.getDate() - 7)

const fromDate = ref(toDateInput(defaultFrom))
const toDate = ref(toDateInput(now))

const periodOptions: { value: Exclude<Period, null>; label: string }[] = [
  { value: '1w', label: '1 week' },
  { value: '1m', label: '1 month' },
  { value: '3m', label: '3 months' },
]

function applyPeriod(p: Exclude<Period, null>) {
  activePeriod.value = p
  const to = new Date()
  const from = new Date()
  if (p === '1w') from.setDate(to.getDate() - 7)
  else if (p === '1m') from.setMonth(to.getMonth() - 1)
  else from.setMonth(to.getMonth() - 3)
  fromDate.value = toDateInput(from)
  toDate.value = toDateInput(to)
}

function onDateInput() {
  activePeriod.value = null
}

// ─── Query ────────────────────────────────────────────────────────────────────

// Convert a local date string (YYYY-MM-DD) to a UTC naive ISO string for the backend.
// e.g. "2026-07-27" + "00:00:00" in UTC-3 → "2026-07-27T03:00:00"
const toUtcNaive = (localDateStr: string, time: string) =>
  new Date(`${localDateStr}T${time}`).toISOString().slice(0, 19)

const { data: overview, isLoading } = useQuery({
  queryKey: computed(() => ['service-orders-overview', fromDate.value, toDate.value]),
  queryFn: () =>
    getServiceOrderOverview({
      from_date: fromDate.value ? toUtcNaive(fromDate.value, '00:00:00') : undefined,
      to_date: toDate.value ? toUtcNaive(toDate.value, '23:59:59') : undefined,
    }),
})

// ─── Status config ────────────────────────────────────────────────────────────

const statusConfig: Record<
  string,
  { label: string; icon: string; bg: string; border: string; text: string }
> = {
  [ServiceOrderStatus.NotStarted]: {
    label: 'Not Started',
    icon: 'lucide:circle-dashed',
    bg: 'bg-gray-50',
    border: 'border-gray-200',
    text: 'text-gray-600',
  },
  [ServiceOrderStatus.Pending]: {
    label: 'Pending',
    icon: 'lucide:clock',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    text: 'text-amber-700',
  },
  [ServiceOrderStatus.InProgress]: {
    label: 'In Progress',
    icon: 'lucide:play-circle',
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    text: 'text-blue-700',
  },
  [ServiceOrderStatus.Suspended]: {
    label: 'Suspended',
    icon: 'lucide:pause-circle',
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    text: 'text-orange-700',
  },
  [ServiceOrderStatus.Completed]: {
    label: 'Completed',
    icon: 'lucide:check-circle-2',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    text: 'text-emerald-700',
  },
  [ServiceOrderStatus.Cancelled]: {
    label: 'Cancelled',
    icon: 'lucide:x-circle',
    bg: 'bg-red-50',
    border: 'border-red-200',
    text: 'text-red-700',
  },
}

const statusOrder = [
  ServiceOrderStatus.NotStarted,
  ServiceOrderStatus.Pending,
  ServiceOrderStatus.InProgress,
  ServiceOrderStatus.Suspended,
  ServiceOrderStatus.Completed,
  ServiceOrderStatus.Cancelled,
]
</script>

<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-sm text-gray-500 mt-1">Overview of service orders by period.</p>
    </div>

    <!-- Filters toolbar -->
    <div class="mb-6 flex flex-wrap items-center gap-3">
      <!-- Period preset buttons -->
      <div class="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
        <button
          v-for="opt in periodOptions"
          :key="opt.value"
          type="button"
          class="px-4 py-1.5 rounded-md text-sm font-medium transition-colors cursor-pointer"
          :class="
            activePeriod === opt.value
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-500 hover:text-gray-700'
          "
          @click="applyPeriod(opt.value)"
        >
          {{ opt.label }}
        </button>
      </div>

      <!-- Date range inputs -->
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-1.5">
          <Icon icon="lucide:calendar" class="size-3.5 text-gray-400 shrink-0" />
          <input
            type="date"
            v-model="fromDate"
            :max="toDate"
            class="text-sm text-gray-700 outline-none cursor-pointer w-32"
            @input="onDateInput"
          />
        </div>
        <span class="text-gray-400 text-sm">→</span>
        <div class="flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-1.5">
          <Icon icon="lucide:calendar" class="size-3.5 text-gray-400 shrink-0" />
          <input
            type="date"
            v-model="toDate"
            :min="fromDate"
            class="text-sm text-gray-700 outline-none cursor-pointer w-32"
            @input="onDateInput"
          />
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="flex items-center justify-center py-20 text-gray-400 text-sm">
      <Icon icon="lucide:loader-2" class="size-5 animate-spin mr-2" />
      Loading…
    </div>

    <template v-else-if="overview">
      <!-- Total card -->
      <div class="mb-6 rounded-2xl border border-gray-200 bg-white shadow-sm p-6 flex items-center gap-5">
        <div class="size-14 rounded-xl bg-indigo-100 flex items-center justify-center shrink-0">
          <Icon icon="lucide:clipboard-list" class="size-7 text-indigo-600" />
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Total service orders</p>
          <p class="text-4xl font-bold text-gray-900 mt-0.5">{{ overview.total }}</p>
        </div>
      </div>

      <!-- By status grid -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div
          v-for="status in statusOrder"
          :key="status"
          class="rounded-xl border p-5 flex items-center gap-4"
          :class="[statusConfig[status].bg, statusConfig[status].border]"
        >
          <div class="size-10 rounded-lg flex items-center justify-center shrink-0 bg-white/70">
            <Icon :icon="statusConfig[status].icon" class="size-5" :class="statusConfig[status].text" />
          </div>
          <div class="min-w-0">
            <p class="text-xs font-medium truncate" :class="statusConfig[status].text">
              {{ statusConfig[status].label }}
            </p>
            <p class="text-2xl font-bold text-gray-900 mt-0.5">
              {{ overview.by_status[status] ?? 0 }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
