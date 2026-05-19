<script setup lang="ts">
import { computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { getServiceOrder } from '@/services/queries'
import Button from '@/components/ui/Button.vue'
import { VIEW_SERVICE_ORDERS } from '@/utils/paths'
import { ServiceOrderStatus, WorkSessionStatus } from '@/utils/enums'

export type Props = {
  id: string
}

const { id } = defineProps<Props>()

const { data: serviceOrder } = useQuery({
  queryKey: ['service-orders', id],
  queryFn: () => getServiceOrder(id),
})

const formatTime = (iso: string) =>
  new Intl.DateTimeFormat('pt-BR', { timeStyle: 'short' }).format(new Date(iso))

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(iso))

const statusStyle: Record<
  ServiceOrderStatus,
  { label: string; dot: string; card: string; border: string; text: string; badge: string }
> = {
  [ServiceOrderStatus.NotStarted]: {
    label: 'Not Started',
    dot: 'bg-gray-400',
    card: 'bg-gray-50',
    border: 'border-gray-200',
    text: 'text-gray-600',
    badge: 'bg-gray-100 text-gray-600',
  },
  [ServiceOrderStatus.Pending]: {
    label: 'Pending',
    dot: 'bg-amber-400',
    card: 'bg-amber-50',
    border: 'border-amber-200',
    text: 'text-amber-700',
    badge: 'bg-amber-100 text-amber-700',
  },
  [ServiceOrderStatus.InProgress]: {
    label: 'In Progress',
    dot: 'bg-blue-500',
    card: 'bg-blue-50',
    border: 'border-blue-200',
    text: 'text-blue-700',
    badge: 'bg-blue-100 text-blue-700',
  },
  [ServiceOrderStatus.Suspended]: {
    label: 'Suspended',
    dot: 'bg-orange-400',
    card: 'bg-orange-50',
    border: 'border-orange-200',
    text: 'text-orange-700',
    badge: 'bg-orange-100 text-orange-700',
  },
  [ServiceOrderStatus.Completed]: {
    label: 'Completed',
    dot: 'bg-emerald-500',
    card: 'bg-emerald-50',
    border: 'border-emerald-200',
    text: 'text-emerald-700',
    badge: 'bg-emerald-100 text-emerald-700',
  },
  [ServiceOrderStatus.Cancelled]: {
    label: 'Cancelled',
    dot: 'bg-red-500',
    card: 'bg-red-50',
    border: 'border-red-200',
    text: 'text-red-700',
    badge: 'bg-red-100 text-red-700',
  },
}

const sessionStyle: Record<
  WorkSessionStatus,
  { label: string; dot: string; card: string; border: string; badge: string }
> = {
  [WorkSessionStatus.Started]: {
    label: 'Started',
    dot: 'bg-blue-500',
    card: 'bg-blue-50',
    border: 'border-blue-200',
    badge: 'bg-blue-100 text-blue-700',
  },
  [WorkSessionStatus.Paused]: {
    label: 'Paused',
    dot: 'bg-amber-400',
    card: 'bg-amber-50',
    border: 'border-amber-200',
    badge: 'bg-amber-100 text-amber-700',
  },
  [WorkSessionStatus.Resumed]: {
    label: 'Resumed',
    dot: 'bg-sky-500',
    card: 'bg-sky-50',
    border: 'border-sky-200',
    badge: 'bg-sky-100 text-sky-700',
  },
  [WorkSessionStatus.Completed]: {
    label: 'Completed',
    dot: 'bg-emerald-500',
    card: 'bg-emerald-50',
    border: 'border-emerald-200',
    badge: 'bg-emerald-100 text-emerald-700',
  },
  [WorkSessionStatus.Stopped]: {
    label: 'Stopped',
    dot: 'bg-red-500',
    card: 'bg-red-50',
    border: 'border-red-200',
    badge: 'bg-red-100 text-red-700',
  },
}

const currentStatusStyle = (s: ServiceOrderStatus) =>
  statusStyle[s] ?? statusStyle[ServiceOrderStatus.NotStarted]

// ─── Timeline grid computation ───────────────────────────────────────────────

const THRESHOLD_MS = 3 * 60 * 1000 // 3 minutes — events within this window share a row

type StatusEvent = {
  type: 'status'
  status: ServiceOrderStatus
  reason: string | null
  created_at: string
  timestamp: number
}

type SessionEvent = {
  type: 'session'
  sessionId: string
  status: WorkSessionStatus
  observations: string | null
  occurred_at: string
  timestamp: number
}

type AnyEvent = StatusEvent | SessionEvent

interface TimeSlot {
  time: string
  timestamp: number
  statusEvent: StatusEvent | null
  sessionEvents: Record<string, SessionEvent> // keyed by work_session id
}

const sessions = computed(() => serviceOrder.value?.work_sessions ?? [])

const timeSlots = computed<TimeSlot[]>(() => {
  const so = serviceOrder.value
  if (!so) return []

  const allEvents: AnyEvent[] = []

  for (const sh of so.status_histories) {
    allEvents.push({
      type: 'status',
      status: sh.status,
      reason: sh.reason,
      created_at: sh.created_at,
      timestamp: new Date(sh.created_at).getTime(),
    })
  }

  for (const ws of so.work_sessions) {
    for (const h of ws.histories) {
      allEvents.push({
        type: 'session',
        sessionId: ws.id,
        status: h.status,
        observations: h.observations,
        occurred_at: h.occurred_at,
        timestamp: new Date(h.occurred_at).getTime(),
      })
    }
  }

  allEvents.sort((a, b) => a.timestamp - b.timestamp)

  const slots: TimeSlot[] = []

  for (const event of allEvents) {
    const last = slots[slots.length - 1]
    const columnAlreadyTaken =
      event.type === 'status'
        ? last?.statusEvent !== null
        : last?.sessionEvents[event.sessionId] !== undefined
    const canMerge =
      last &&
      Math.abs(event.timestamp - last.timestamp) <= THRESHOLD_MS &&
      !columnAlreadyTaken

    if (canMerge) {
      if (event.type === 'status') {
        last.statusEvent = event
      } else {
        last.sessionEvents[event.sessionId] = event
      }
    } else {
      const isoStr = event.type === 'status' ? event.created_at : event.occurred_at
      const slot: TimeSlot = {
        time: formatTime(isoStr),
        timestamp: event.timestamp,
        statusEvent: null,
        sessionEvents: {},
      }
      if (event.type === 'status') {
        slot.statusEvent = event
      } else {
        slot.sessionEvents[event.sessionId] = event
      }
      slots.push(slot)
    }
  }

  return slots
})
</script>

<template>
  <div class="p-8">

    <!-- Header -->
    <div class="mb-8 flex items-start justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">
          Timeline
          <span class="text-gray-400 font-normal ml-1">— Order #{{ serviceOrder?.order_number }}</span>
        </h1>
        <p class="text-sm text-gray-500 mt-1">
          Chronological view of status changes and work session events.
        </p>

        <div v-if="serviceOrder" class="flex items-center gap-3 mt-3">
          <span
            class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium"
            :class="currentStatusStyle(serviceOrder.status).badge"
          >
            <span
              class="inline-block size-1.5 rounded-full"
              :class="currentStatusStyle(serviceOrder.status).dot"
            />
            {{ currentStatusStyle(serviceOrder.status).label }}
          </span>
          <span v-if="serviceOrder.service_type" class="text-xs text-gray-400">
            {{ serviceOrder.service_type.name }}
          </span>
        </div>
      </div>
      <Button variant="outline" :to="VIEW_SERVICE_ORDERS(id)">Back to order</Button>
    </div>

    <!-- Loading -->
    <div v-if="!serviceOrder" class="flex items-center justify-center py-20 text-gray-400 text-sm">
      Loading…
    </div>

    <!-- Grid container (scrollable horizontally) -->
    <div v-else class="overflow-x-auto rounded-2xl border border-gray-200 shadow-sm">
      <div class="min-w-max bg-white">

        <!-- Column headers -->
        <div
          class="grid border-b border-gray-200 bg-gray-50"
          :style="`grid-template-columns: 80px 1fr repeat(${sessions.length}, minmax(220px, 1fr))`"
        >
          <!-- Time header -->
          <div class="px-4 py-3 flex items-center">
            <span class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Time</span>
          </div>

          <!-- Status history header -->
          <div class="px-4 py-3 border-l border-gray-200">
            <p class="text-xs font-semibold text-gray-700 uppercase tracking-wide">Status History</p>
            <p class="text-xs text-gray-400 mt-0.5">
              {{ serviceOrder.status_histories.length }} event{{ serviceOrder.status_histories.length !== 1 ? 's' : '' }}
            </p>
          </div>

          <!-- One header per work session -->
          <div
            v-for="session in sessions"
            :key="session.id"
            class="px-4 py-3 border-l border-gray-200"
          >
            <div class="flex items-center gap-2">
              <div class="size-7 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                <span class="text-xs font-bold text-blue-600">
                  {{ session.employee.name.charAt(0).toUpperCase() }}
                </span>
              </div>
              <div class="min-w-0">
                <p class="text-xs font-semibold text-gray-700 truncate">{{ session.employee.name }}</p>
                <p class="text-xs text-gray-400">{{ formatDate(session.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- No events -->
        <div
          v-if="timeSlots.length === 0"
          class="flex items-center justify-center py-16 text-sm text-gray-400"
        >
          No events recorded yet.
        </div>

        <!-- Time slot rows -->
        <div
          v-for="(slot, i) in timeSlots"
          :key="slot.timestamp"
          class="grid"
          :class="i < timeSlots.length - 1 ? 'border-b border-gray-100' : ''"
          :style="`grid-template-columns: 80px 1fr repeat(${sessions.length}, minmax(220px, 1fr))`"
        >
          <!-- Time label -->
          <div class="px-4 py-4 flex items-start pt-5">
            <span class="text-xs font-mono text-gray-400 tabular-nums">{{ slot.time }}</span>
          </div>

          <!-- Status history cell -->
          <div class="px-4 py-3 border-l border-gray-100 flex items-center min-h-[72px]">
            <div
              v-if="slot.statusEvent"
              class="w-full rounded-xl border p-3"
              :class="[
                statusStyle[slot.statusEvent.status]?.card ?? 'bg-gray-50',
                statusStyle[slot.statusEvent.status]?.border ?? 'border-gray-200',
              ]"
            >
              <span
                class="inline-flex items-center gap-1.5 text-xs font-semibold px-2 py-0.5 rounded-full mb-1.5"
                :class="statusStyle[slot.statusEvent.status]?.badge ?? 'bg-gray-100 text-gray-600'"
              >
                <span
                  class="size-1.5 rounded-full"
                  :class="statusStyle[slot.statusEvent.status]?.dot ?? 'bg-gray-400'"
                />
                {{ statusStyle[slot.statusEvent.status]?.label ?? slot.statusEvent.status }}
              </span>
              <p v-if="slot.statusEvent.reason" class="text-xs text-gray-600 leading-relaxed mt-1">
                "{{ slot.statusEvent.reason }}"
              </p>
              <p v-else class="text-xs text-gray-300 italic mt-1">No reason provided.</p>
            </div>
          </div>

          <!-- Session cells -->
          <div
            v-for="session in sessions"
            :key="session.id"
            class="px-4 py-3 border-l border-gray-100 flex items-center min-h-[72px]"
          >
            <div
              v-if="slot.sessionEvents[session.id]"
              class="w-full rounded-xl border p-3"
              :class="[
                sessionStyle[slot.sessionEvents[session.id].status]?.card ?? 'bg-gray-50',
                sessionStyle[slot.sessionEvents[session.id].status]?.border ?? 'border-gray-200',
              ]"
            >
              <span
                class="inline-flex items-center gap-1.5 text-xs font-semibold px-2 py-0.5 rounded-full mb-1.5"
                :class="sessionStyle[slot.sessionEvents[session.id].status]?.badge ?? 'bg-gray-100 text-gray-600'"
              >
                <span
                  class="size-1.5 rounded-full"
                  :class="sessionStyle[slot.sessionEvents[session.id].status]?.dot ?? 'bg-gray-400'"
                />
                {{ sessionStyle[slot.sessionEvents[session.id].status]?.label ?? slot.sessionEvents[session.id].status }}
              </span>
              <p
                v-if="slot.sessionEvents[session.id].observations"
                class="text-xs text-gray-600 leading-relaxed mt-1"
              >
                "{{ slot.sessionEvents[session.id].observations }}"
              </p>
              <p v-else class="text-xs text-gray-300 italic mt-1">No observations.</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>
