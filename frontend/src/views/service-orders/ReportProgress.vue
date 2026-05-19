<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Separator from '@/components/ui/Separator.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'
import type { SelectOption } from '@/components/ui/Select.vue'
import { Icon } from '@iconify/vue'
import { useQuery } from '@tanstack/vue-query'
import { getEmployees, getServiceOrder, reportServiceOrderProgress } from '@/services/queries'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { VIEW_SERVICE_ORDERS } from '@/utils/paths'
import { ServiceOrderStatus, WorkSessionStatus } from '@/utils/enums'

export type Props = {
  id: string
}

const router = useRouter()

const { id } = defineProps<Props>()

const { data: serviceOrder } = useQuery({
  queryKey: ['service-orders', id],
  queryFn: () => getServiceOrder(id),
})

const { data: employeesData } = useQuery({
  queryKey: ['employees', { page: 1, size: 100 }],
  queryFn: () => getEmployees({ page: 1, size: 100 }),
})

const employeeOptions = computed<SelectOption[]>(
  () => employeesData.value?.items.map((e) => ({ value: e.id, label: e.name })) ?? [],
)

const statusOptions: SelectOption[] = [
  { value: ServiceOrderStatus.NotStarted, label: 'Not Started' },
  { value: ServiceOrderStatus.Pending, label: 'Pending' },
  { value: ServiceOrderStatus.InProgress, label: 'In Progress' },
  { value: ServiceOrderStatus.Suspended, label: 'Suspended' },
  { value: ServiceOrderStatus.Completed, label: 'Completed' },
  { value: ServiceOrderStatus.Cancelled, label: 'Cancelled' },
]

const workSessionStatusOptions: SelectOption[] = [
  { value: WorkSessionStatus.Started, label: 'Started' },
  { value: WorkSessionStatus.Paused, label: 'Paused' },
  { value: WorkSessionStatus.Resumed, label: 'Resumed' },
  { value: WorkSessionStatus.Completed, label: 'Completed' },
  { value: WorkSessionStatus.Stopped, label: 'Stopped' },
]

const statusConfig: Record<ServiceOrderStatus, { label: string; dot: string; text: string }> = {
  [ServiceOrderStatus.NotStarted]: { label: 'Not Started', dot: 'bg-gray-400', text: 'text-gray-500' },
  [ServiceOrderStatus.Pending]: { label: 'Pending', dot: 'bg-yellow-500', text: 'text-yellow-600' },
  [ServiceOrderStatus.InProgress]: { label: 'In Progress', dot: 'bg-blue-500', text: 'text-blue-600' },
  [ServiceOrderStatus.Suspended]: { label: 'Suspended', dot: 'bg-orange-500', text: 'text-orange-600' },
  [ServiceOrderStatus.Completed]: { label: 'Completed', dot: 'bg-green-500', text: 'text-green-600' },
  [ServiceOrderStatus.Cancelled]: { label: 'Cancelled', dot: 'bg-red-500', text: 'text-red-600' },
}

const workSessionStatusConfig: Record<WorkSessionStatus, { label: string; dot: string; text: string }> = {
  [WorkSessionStatus.Started]: { label: 'Started', dot: 'bg-blue-500', text: 'text-blue-600' },
  [WorkSessionStatus.Paused]: { label: 'Paused', dot: 'bg-yellow-500', text: 'text-yellow-600' },
  [WorkSessionStatus.Resumed]: { label: 'Resumed', dot: 'bg-blue-400', text: 'text-blue-500' },
  [WorkSessionStatus.Completed]: { label: 'Completed', dot: 'bg-green-500', text: 'text-green-600' },
  [WorkSessionStatus.Stopped]: { label: 'Stopped', dot: 'bg-red-500', text: 'text-red-600' },
}

const statusLabels: Record<ServiceOrderStatus, string> = {
  [ServiceOrderStatus.NotStarted]: 'Not Started',
  [ServiceOrderStatus.Pending]: 'Pending',
  [ServiceOrderStatus.InProgress]: 'In Progress',
  [ServiceOrderStatus.Suspended]: 'Suspended',
  [ServiceOrderStatus.Completed]: 'Completed',
  [ServiceOrderStatus.Cancelled]: 'Cancelled',
}

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(iso))

const formatDateOnly = (iso: string) =>
  new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium' }).format(new Date(iso))

// --- Work sessions ---

type WorkSessionHistoryInput = {
  status: string
  observations: string
  occurred_at: string
}

type WorkSessionInput = {
  employee_id: string
  histories: WorkSessionHistoryInput[]
}

// New histories keyed by existing work session id
const existingSessionNewHistories = ref<Record<string, WorkSessionHistoryInput[]>>({})

const addExistingHistory = (wsId: string) => {
  existingSessionNewHistories.value[wsId].push({
    status: '',
    observations: '',
    occurred_at: new Date().toISOString().slice(0, 16),
  })
}

const removeExistingHistory = (wsId: string, index: number) => {
  existingSessionNewHistories.value[wsId].splice(index, 1)
}

const newSessions = ref<WorkSessionInput[]>([])

const addSession = () => {
  const histories: WorkSessionHistoryInput[] =
    status.value && status.value !== ServiceOrderStatus.NotStarted
      ? [{ status: '', observations: '', occurred_at: new Date().toISOString().slice(0, 16) }]
      : []
  newSessions.value.push({ employee_id: '', histories })
}

const removeSession = (index: number) => {
  newSessions.value.splice(index, 1)
}

const addHistory = (sessionIndex: number) => {
  newSessions.value[sessionIndex].histories.push({
    status: '',
    observations: '',
    occurred_at: new Date().toISOString().slice(0, 16),
  })
}

const removeHistory = (sessionIndex: number, historyIndex: number) => {
  newSessions.value[sessionIndex].histories.splice(historyIndex, 1)
}

// --- Form ---

const schema = z.object({
  status: z.nativeEnum(ServiceOrderStatus, { message: 'Status is required' }),
  status_reason: z.string().nullish(),
})

const { handleSubmit, errors, defineField, setValues } = useForm({
  validationSchema: toTypedSchema(schema),
})

watch(serviceOrder, (so) => {
  if (!so) return
  setValues({ status: so.status })
  const map: Record<string, WorkSessionHistoryInput[]> = {}
  so.work_sessions.forEach((ws) => { map[ws.id] = [] })
  existingSessionNewHistories.value = map
}, { immediate: true })

const [status] = defineField('status')
const [statusReason, statusReasonAttrs] = defineField('status_reason')

const statusReasonTitle = computed(() => {
  const label = status.value ? statusLabels[status.value as ServiceOrderStatus] : null
  return label ? `Justify why the order is ${label}` : 'Status Reason'
})

const onSubmit = handleSubmit(async (values) => {
  const sessions = newSessions.value
    .filter((s) => s.employee_id)
    .map((s) => ({
      employee_id: s.employee_id,
      histories: s.histories
        .filter((h) => h.status)
        .map((h) => ({
          status: h.status,
          observations: h.observations || null,
          occurred_at: h.occurred_at,
        })),
    }))

  const newHistories = Object.entries(existingSessionNewHistories.value).flatMap(
    ([wsId, histories]) =>
      histories
        .filter((h) => h.status)
        .map((h) => ({
          work_session_id: wsId,
          status: h.status,
          observations: h.observations || null,
          occurred_at: h.occurred_at,
        })),
  )

  reportServiceOrderProgress({
    service_order_id: id,
    status: values.status,
    status_reason: values.status_reason || null,
    work_sessions: sessions,
    new_histories: newHistories.length > 0 ? newHistories : undefined,
  })
    .then(() => router.push(VIEW_SERVICE_ORDERS(id)))
    .catch(console.error)
})
</script>

<template>
  <div class="p-8">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">
        Report Progress — Order #{{ serviceOrder?.order_number }}
      </h1>
      <p class="text-sm text-gray-500 mt-1">
        Update the status and attach new session data to this service order.
      </p>
    </div>

    <div v-if="!serviceOrder" class="flex items-center justify-center py-20 text-gray-400 text-sm">
      Loading…
    </div>

    <form v-else @submit.prevent="onSubmit">
      <div class="py-6 flex flex-col gap-5">

        <!-- General fields -->
        <div class="grid grid-cols-3 gap-4">
          <Fieldset id="service_type" label="Service Type">
            <Input id="service_type" :model-value="serviceOrder.service_type?.name ?? '—'" disabled />
          </Fieldset>

          <!-- Current status (readonly) + new status (editable) side by side -->
          <Fieldset id="current_status" label="Current Status">
            <div class="flex items-center gap-2 h-9 px-3 border border-gray-200 rounded-md bg-gray-50">
              <span
                class="inline-block size-2.5 rounded-full"
                :class="statusConfig[serviceOrder.status]?.dot"
              />
              <span class="text-sm font-medium" :class="statusConfig[serviceOrder.status]?.text">
                {{ statusConfig[serviceOrder.status]?.label }}
              </span>
            </div>
          </Fieldset>

          <Fieldset id="status" label="New Status" :error="errors.status">
            <Select
              v-model="status as string"
              :options="statusOptions"
              placeholder="Select status…"
            />
          </Fieldset>

          <Fieldset id="started_at" label="Started at">
            <Input
              id="started_at"
              :model-value="serviceOrder.started_at ? formatDate(serviceOrder.started_at) : '—'"
              disabled
            />
          </Fieldset>
          <Fieldset id="finished_at" label="Finished at">
            <Input
              id="finished_at"
              :model-value="serviceOrder.finished_at ? formatDate(serviceOrder.finished_at) : '—'"
              disabled
            />
          </Fieldset>
          <Fieldset id="total_hours" label="Total hours">
            <Input
              id="total_hours"
              :model-value="serviceOrder.total_hours != null ? (Math.floor(serviceOrder.total_hours * 100) / 100).toFixed(2) : '—'"
              disabled
            />
          </Fieldset>
        </div>

        <Separator />

        <!-- Status Reason -->
        <div>
          <h2 class="text-xl font-bold text-gray-900">{{ statusReasonTitle }}</h2>
          <p class="text-sm text-gray-500 mt-1">Explain the reason for the selected status.</p>
        </div>
        <Textarea
          v-model="statusReason"
          v-bind="statusReasonAttrs"
          placeholder="Reason for the current status (optional)…"
        />

        <Separator />

        <!-- Work Sessions: existing (readonly) + new (editable) in one box -->
        <div class="rounded-xl border border-blue-100 bg-blue-50/50 p-5 flex flex-col gap-5">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-lg font-bold text-blue-900">Work Sessions</h2>
              <p class="text-sm text-blue-600/70 mt-0.5">Employees and their session histories.</p>
            </div>
            <Button type="button" variant="outline" icon="lucide:plus" @click="addSession">
              Add session
            </Button>
          </div>

          <!-- Existing sessions -->
          <template v-if="serviceOrder.work_sessions.length > 0">
            <div class="flex flex-col gap-3">
              <div
                v-for="session in serviceOrder.work_sessions"
                :key="session.id"
                class="bg-white border border-blue-100 rounded-lg p-4 shadow-sm flex flex-col gap-3"
              >
                <div class="flex items-center justify-between">
                  <span class="text-sm font-semibold text-gray-800">{{ session.employee.name }}</span>
                  <div class="flex items-center gap-3">
                    <span class="text-xs text-gray-400">{{ formatDate(session.created_at) }}</span>
                    <button
                      type="button"
                      class="text-blue-500 hover:text-blue-700 transition-colors"
                      title="Add history"
                      @click="addExistingHistory(session.id)"
                    >
                      <Icon icon="lucide:circle-plus" class="size-4" />
                    </button>
                  </div>
                </div>

                <!-- Existing histories (readonly) -->
                <div v-if="session.histories.length > 0" class="flex flex-col gap-1.5">
                  <div
                    v-for="history in session.histories"
                    :key="history.id"
                    class="flex items-center gap-2 text-sm"
                  >
                    <span
                      class="inline-block size-2 rounded-full"
                      :class="workSessionStatusConfig[history.status]?.dot"
                    />
                    <span :class="workSessionStatusConfig[history.status]?.text">
                      {{ workSessionStatusConfig[history.status]?.label }}
                    </span>
                    <span class="text-gray-400 text-xs ml-auto">{{ formatDate(history.occurred_at) }}</span>
                    <span v-if="history.observations" class="text-gray-500 text-xs">
                      — {{ history.observations }}
                    </span>
                  </div>
                </div>

                <!-- New histories for this existing session -->
                <div
                  v-if="existingSessionNewHistories[session.id]?.length > 0"
                  class="flex flex-col gap-2 pt-1 border-t border-gray-100"
                >
                  <div
                    v-for="(history, hi) in existingSessionNewHistories[session.id]"
                    :key="hi"
                    class="grid grid-cols-3 gap-3 items-end bg-gray-50 border border-gray-100 rounded-md p-3"
                  >
                    <Fieldset :id="`existing-${session.id}-history-${hi}-status`" label="Status">
                      <Select
                        v-model="history.status"
                        :options="workSessionStatusOptions"
                        placeholder="Select status…"
                      />
                    </Fieldset>
                    <Fieldset :id="`existing-${session.id}-history-${hi}-occurred_at`" label="Occurred at">
                      <Input
                        :id="`existing-${session.id}-history-${hi}-occurred_at`"
                        type="datetime-local"
                        v-model="history.occurred_at"
                      />
                    </Fieldset>
                    <Fieldset :id="`existing-${session.id}-history-${hi}-observations`" label="Observations">
                      <div class="flex gap-2 items-center">
                        <Input
                          :id="`existing-${session.id}-history-${hi}-observations`"
                          v-model="history.observations"
                          placeholder="Optional…"
                        />
                        <button
                          type="button"
                          class="text-red-400 hover:text-red-600 transition-colors shrink-0"
                          title="Remove history"
                          @click="removeExistingHistory(session.id, hi)"
                        >
                          <Icon icon="lucide:trash-2" class="size-4" />
                        </button>
                      </div>
                    </Fieldset>
                  </div>
                </div>
              </div>
            </div>

            <Separator v-if="newSessions.length > 0" />
          </template>

          <!-- New sessions (editable) -->
          <div v-if="newSessions.length === 0 && serviceOrder.work_sessions.length === 0" class="text-sm text-blue-400 text-center py-6">
            No sessions added yet. Click "Add session" to get started.
          </div>
          <div v-else-if="newSessions.length > 0" class="flex flex-col gap-4">
            <div
              v-for="(session, si) in newSessions"
              :key="si"
              class="bg-white border border-blue-100 rounded-lg p-4 flex flex-col gap-4 shadow-sm"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-semibold text-gray-800">New Session {{ si + 1 }}</span>
                <button
                  type="button"
                  class="text-red-400 hover:text-red-600 transition-colors"
                  title="Remove session"
                  @click="removeSession(si)"
                >
                  <Icon icon="lucide:trash-2" class="size-4" />
                </button>
              </div>

              <div class="grid grid-cols-3 gap-4">
                <Fieldset :id="`session-${si}-employee`" label="Employee">
                  <Select
                    v-model="session.employee_id"
                    :options="employeeOptions"
                    placeholder="Select employee…"
                  />
                </Fieldset>
              </div>

              <div class="flex flex-col gap-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Histories</span>
                  <button
                    type="button"
                    class="text-blue-500 hover:text-blue-700 transition-colors"
                    title="Add history"
                    @click="addHistory(si)"
                  >
                    <Icon icon="lucide:circle-plus" class="size-4" />
                  </button>
                </div>

                <div v-if="session.histories.length === 0" class="text-xs text-gray-400 py-2 text-center">
                  No histories added.
                </div>
                <div v-else class="flex flex-col gap-2">
                  <div
                    v-for="(history, hi) in session.histories"
                    :key="hi"
                    class="grid grid-cols-3 gap-3 items-end bg-gray-50 border border-gray-100 rounded-md p-3"
                  >
                    <Fieldset :id="`session-${si}-history-${hi}-status`" label="Status">
                      <Select
                        v-model="history.status"
                        :options="workSessionStatusOptions"
                        placeholder="Select status…"
                      />
                    </Fieldset>
                    <Fieldset :id="`session-${si}-history-${hi}-occurred_at`" label="Occurred at">
                      <Input
                        :id="`session-${si}-history-${hi}-occurred_at`"
                        type="datetime-local"
                        v-model="history.occurred_at"
                      />
                    </Fieldset>
                    <Fieldset :id="`session-${si}-history-${hi}-observations`" label="Observations">
                      <div class="flex gap-2 items-center">
                        <Input
                          :id="`session-${si}-history-${hi}-observations`"
                          v-model="history.observations"
                          placeholder="Optional…"
                        />
                        <button
                          type="button"
                          class="text-red-400 hover:text-red-600 transition-colors shrink-0"
                          title="Remove history"
                          @click="removeHistory(si, hi)"
                        >
                          <Icon icon="lucide:trash-2" class="size-4" />
                        </button>
                      </div>
                    </Fieldset>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <Separator />

        <!-- Description (readonly) -->
        <div>
          <h2 class="text-xl font-bold text-gray-900">Description</h2>
          <p class="text-sm text-gray-500 mt-1">Additional details about this service order.</p>
        </div>
        <Textarea :model-value="serviceOrder.description ?? ''" disabled />
      </div>

      <Separator />
      <div class="px-6 py-4 flex justify-end gap-2">
        <Button variant="outline" :to="VIEW_SERVICE_ORDERS(id)">Cancel</Button>
        <Button type="submit" icon="lucide:send">Report progress</Button>
      </div>
    </form>
  </div>
</template>
