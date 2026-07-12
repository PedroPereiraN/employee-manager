<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Separator from '@/components/ui/Separator.vue'
import Button from '@/components/ui/Button.vue'
import SuccessModal from '@/components/ui/SuccessModal.vue'
import Select from '@/components/ui/Select.vue'
import type { SelectOption } from '@/components/ui/Select.vue'
import RegisterSelector from '@/components/ui/RegisterSelector.vue'
import { Icon } from '@iconify/vue'
import { useQuery } from '@tanstack/vue-query'
import {
  createServiceOrder,
  getEmployees,
  getServiceOrder,
  getServiceTypes,
} from '@/services/queries'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  REPORT_SERVICE_ORDER_PROGRESS,
  SERVICE_ORDERS,
  TIMELINE_SERVICE_ORDER,
} from '@/utils/paths'
import { ServiceOrderStatus, WorkSessionStatus } from '@/utils/enums'

export type Props = {
  id?: string
}

const router = useRouter()

const { id } = defineProps<Props>()

const { data: serviceOrder } = useQuery({
  queryKey: ['service-orders', id],
  queryFn: () => getServiceOrder(id!),
  enabled: computed(() => !!id),
})


const statusOptions: SelectOption[] = [
  { value: ServiceOrderStatus.NotStarted, label: 'Not Started' },
  { value: ServiceOrderStatus.Pending, label: 'Pending' },
  { value: ServiceOrderStatus.InProgress, label: 'In Progress' },
  { value: ServiceOrderStatus.Completed, label: 'Completed' },
]

const workSessionStatusOptions: SelectOption[] = [
  { value: WorkSessionStatus.Started, label: 'Started' },
  { value: WorkSessionStatus.Paused, label: 'Paused' },
  { value: WorkSessionStatus.Resumed, label: 'Resumed' },
  { value: WorkSessionStatus.Completed, label: 'Completed' },
  { value: WorkSessionStatus.Stopped, label: 'Stopped' },
]

const formState = ref<'new' | 'visualize'>('new')

if (id) {
  formState.value = 'visualize'
}

// --- Work sessions (managed with plain refs for dynamic nested arrays) ---

type WorkSessionHistoryInput = {
  status: string
  observations: string
  occurred_at: string
}

type WorkSessionInput = {
  employee_id: string
  histories: WorkSessionHistoryInput[]
}

const workSessions = ref<WorkSessionInput[]>([])

const addSession = () => {
  const histories: WorkSessionHistoryInput[] =
    status.value && status.value !== ServiceOrderStatus.NotStarted
      ? [{ status: '', observations: '', occurred_at: new Date().toISOString().slice(0, 16) }]
      : []
  workSessions.value.push({ employee_id: '', histories })
}

const removeSession = (index: number) => {
  workSessions.value.splice(index, 1)
}

const addHistory = (sessionIndex: number) => {
  workSessions.value[sessionIndex].histories.push({
    status: '',
    observations: '',
    occurred_at: new Date().toISOString().slice(0, 16),
  })
}

const removeHistory = (sessionIndex: number, historyIndex: number) => {
  workSessions.value[sessionIndex].histories.splice(historyIndex, 1)
}

// --- vee-validate for scalar fields ---

const schema = z.object({
  service_type_id: z.string().optional(),
  status: z.nativeEnum(ServiceOrderStatus),
  finished_at: z.string().nullish(),
  status_reason: z.string().nullish(),
  description: z.string().nullish(),
})

const { handleSubmit, errors, defineField, setValues, resetForm } = useForm({
  validationSchema: toTypedSchema(schema),
  initialValues: {
    status: ServiceOrderStatus.NotStarted,
    finished_at: new Date().toISOString().slice(0, 16),
  },
})

const showSuccessModal = ref(false)

watch(serviceOrder, (so) => {
  if (so) {
    setValues({
      service_type_id: so.service_type?.id ?? undefined,
      description: so.description ?? undefined,
      status: so.status,
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  const sessions = workSessions.value
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

  createServiceOrder({
    service_type_id: values.service_type_id || null,
    description: values.description || null,
    status: values.status,
    finished_at: values.status === ServiceOrderStatus.Completed ? values.finished_at || null : null,
    status_reason: values.status_reason || null,
    work_sessions: sessions,
  })
    .then(() => {
      showSuccessModal.value = true
    })
    .catch((error) => {
      console.error(error)
    })
})

function handleCreateAnother() {
  showSuccessModal.value = false
  workSessions.value = []
  resetForm()
}

const [serviceTypeId] = defineField('service_type_id')
const [status] = defineField('status')
const [finishedAt, finishedAtAttrs] = defineField('finished_at')
const [statusReason, statusReasonAttrs] = defineField('status_reason')
const [description, descriptionAttrs] = defineField('description')

// --- Display configs ---

const statusConfig: Record<ServiceOrderStatus, { label: string; dot: string; text: string }> = {
  [ServiceOrderStatus.NotStarted]: {
    label: 'Not Started',
    dot: 'bg-gray-400',
    text: 'text-gray-500',
  },
  [ServiceOrderStatus.Pending]: { label: 'Pending', dot: 'bg-yellow-500', text: 'text-yellow-600' },
  [ServiceOrderStatus.InProgress]: {
    label: 'In Progress',
    dot: 'bg-blue-500',
    text: 'text-blue-600',
  },
  [ServiceOrderStatus.Suspended]: {
    label: 'Suspended',
    dot: 'bg-orange-500',
    text: 'text-orange-600',
  },
  [ServiceOrderStatus.Completed]: {
    label: 'Completed',
    dot: 'bg-green-500',
    text: 'text-green-600',
  },
  [ServiceOrderStatus.Cancelled]: { label: 'Cancelled', dot: 'bg-red-500', text: 'text-red-600' },
}

const workSessionStatusConfig: Record<
  WorkSessionStatus,
  { label: string; dot: string; text: string }
> = {
  [WorkSessionStatus.Started]: { label: 'Started', dot: 'bg-blue-500', text: 'text-blue-600' },
  [WorkSessionStatus.Paused]: { label: 'Paused', dot: 'bg-yellow-500', text: 'text-yellow-600' },
  [WorkSessionStatus.Resumed]: { label: 'Resumed', dot: 'bg-blue-400', text: 'text-blue-500' },
  [WorkSessionStatus.Completed]: {
    label: 'Completed',
    dot: 'bg-green-500',
    text: 'text-green-600',
  },
  [WorkSessionStatus.Stopped]: { label: 'Stopped', dot: 'bg-red-500', text: 'text-red-600' },
}

const statusReasonConfig: Record<ServiceOrderStatus, { title: string; description: string }> = {
  [ServiceOrderStatus.NotStarted]: {
    title: 'Observations about the order',
    description: 'Add any initial observations about this order.',
  },
  [ServiceOrderStatus.Pending]: {
    title: 'Observations about what is pending',
    description: 'Describe what is pending or blocking the order.',
  },
  [ServiceOrderStatus.InProgress]: {
    title: 'Observations about the order progress',
    description: 'Describe the current progress of the order.',
  },
  [ServiceOrderStatus.Suspended]: {
    title: 'Reason for suspending the order',
    description: 'Explain why the order has been suspended.',
  },
  [ServiceOrderStatus.Completed]: {
    title: 'Observations about the order completion',
    description: 'Add any final observations about the completed order.',
  },
  [ServiceOrderStatus.Cancelled]: {
    title: 'Reason for cancelling the order',
    description: 'Explain why the order has been cancelled.',
  },
}

const statusReasonTitle = computed(
  () => statusReasonConfig[status.value as ServiceOrderStatus]?.title ?? 'Status Reason',
)
const statusReasonDescription = computed(
  () =>
    statusReasonConfig[status.value as ServiceOrderStatus]?.description ??
    'Explain the reason for the selected status.',
)

const formatDate = (iso: string) =>
  new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium', timeStyle: 'short' }).format(
    new Date(iso),
  )

const formatDateOnly = (iso: string) =>
  new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium' }).format(new Date(iso))
</script>

<template>
  <div class="p-8">
    <SuccessModal
      :open="showSuccessModal"
      title="Service order created successfully!"
      description="The new service order has been registered."
      :listPath="SERVICE_ORDERS"
      secondaryLabel="Create another order"
      @secondary="handleCreateAnother"
      @close="showSuccessModal = false"
    />
    <div>
      <h1 class="text-2xl font-bold text-gray-900">
        {{ formState === 'new' ? 'New service order' : `Order #${serviceOrder?.order_number}` }}
      </h1>
      <p class="text-sm text-gray-500 mt-1">
        {{ formState === 'new' ? 'Create a new service order.' : 'Service order details.' }}
      </p>
    </div>

    <form @submit.prevent="onSubmit">
      <div class="py-6 flex flex-col gap-5">
        <!-- General fields -->
        <div class="grid grid-cols-3 gap-4">
          <Fieldset id="service_type_id" label="Service Type" :error="errors.service_type_id">
            <RegisterSelector
              v-model="serviceTypeId as string"
              :display-value="serviceOrder?.service_type?.name"
              :columns="[{ key: 'name', label: 'Name' }]"
              :query-key="['service-types']"
              :query-fn="(p) => getServiceTypes(p)"
              placeholder="Select service type…"
              search-placeholder="Search by name…"
              modal-title="Select Service Type"
              :disabled="formState === 'visualize'"
            />
          </Fieldset>

          <Fieldset id="status" label="Status" :error="errors.status">
            <Select
              v-model="status as string"
              :options="statusOptions"
              placeholder="Select status…"
              :disabled="formState === 'visualize'"
            />
          </Fieldset>

          <Fieldset
            v-if="formState === 'new' && status === ServiceOrderStatus.Completed"
            id="finished_at"
            label="Finished at"
            :error="errors.finished_at"
          >
            <Input
              id="finished_at"
              type="datetime-local"
              v-model="finishedAt"
              v-bind="finishedAtAttrs"
            />
          </Fieldset>

          <template v-if="formState === 'visualize' && serviceOrder">
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
                :model-value="
                  serviceOrder.total_hours != null
                    ? (Math.floor(serviceOrder.total_hours * 100) / 100).toFixed(2)
                    : '—'
                "
                disabled
              />
            </Fieldset>
          </template>
        </div>

        <Separator />

        <!-- Status Reason -->
        <div class="flex items-end justify-between">
          <div>
            <h2 class="text-xl font-bold text-gray-900">
              {{ formState === 'new' ? statusReasonTitle : 'Status History' }}
            </h2>
            <p class="text-sm text-gray-500 mt-1">
              {{
                formState === 'new'
                  ? statusReasonDescription
                  : 'Status change history for this order.'
              }}
            </p>
          </div>
          <Button
            v-if="formState === 'visualize' && id"
            type="button"
            variant="outline"
            icon="lucide:git-branch"
            :to="TIMELINE_SERVICE_ORDER(id)"
          >
            Deep visualization
          </Button>
        </div>

        <!-- New mode: single reason textarea -->
        <template v-if="formState === 'new'">
          <Textarea
            v-model="statusReason"
            v-bind="statusReasonAttrs"
            placeholder="Reason for the current status (optional)…"
          />
        </template>

        <!-- Visualize mode: status history list -->
        <template v-if="formState === 'visualize' && serviceOrder">
          <div v-if="serviceOrder.status_histories.length === 0" class="text-sm text-gray-400">
            No status history.
          </div>
          <div v-else class="flex flex-col gap-2">
            <div
              v-for="history in serviceOrder.status_histories"
              :key="history.id"
              class="flex items-center gap-3 text-sm"
            >
              <span
                class="inline-block size-2.5 rounded-full"
                :class="statusConfig[history.status]?.dot"
              />
              <span :class="statusConfig[history.status]?.text">
                {{ statusConfig[history.status]?.label }}
              </span>
              <span class="text-gray-400 text-xs">{{ formatDate(history.created_at) }}</span>
              <span v-if="history.reason" class="text-gray-500 text-xs"
                >— {{ history.reason }}</span
              >
            </div>
          </div>
        </template>

        <Separator />

        <!-- Work Sessions -->
        <div class="rounded-xl border border-blue-100 bg-blue-50/50 p-5 flex flex-col gap-5">
          <div>
            <h2 class="text-lg font-bold text-gray-900">Work Sessions</h2>
            <p class="text-sm text-gray-500 mt-0.5">Employees and their session histories.</p>
          </div>

          <!-- New mode: editable sessions -->
          <template v-if="formState === 'new'">
            <div v-if="workSessions.length === 0" class="text-sm text-gray-400 text-center py-4">
              No sessions added yet.
            </div>
            <div v-if="workSessions.length > 0" class="flex flex-col gap-4">
              <div
                v-for="(session, si) in workSessions"
                :key="si"
                class="bg-white border border-blue-100 rounded-lg p-4 flex flex-col gap-4 shadow-sm"
              >
                <div class="flex items-center justify-between">
                  <span class="text-sm font-semibold text-gray-800">Session {{ si + 1 }}</span>
                  <button
                    type="button"
                    class="cursor-pointer text-red-400 hover:text-red-600 transition-colors"
                    title="Remove session"
                    @click="removeSession(si)"
                  >
                    <Icon icon="lucide:trash-2" class="size-4" />
                  </button>
                </div>

                <div class="grid grid-cols-3 gap-4">
                  <Fieldset :id="`session-${si}-employee`" label="Employee">
                    <RegisterSelector
                      v-model="session.employee_id"
                      :columns="[{ key: 'name', label: 'Name' }]"
                      :query-key="['employees']"
                      :query-fn="(p) => getEmployees(p)"
                      placeholder="Select employee…"
                      search-placeholder="Search by name…"
                      modal-title="Select Employee"
                    />
                  </Fieldset>
                </div>

                <!-- Histories -->
                <div class="flex flex-col gap-3">
                  <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Histories</span>

                  <div
                    v-if="session.histories.length === 0"
                    class="text-xs text-gray-400 py-2 text-center"
                  >
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
                      <Fieldset
                        :id="`session-${si}-history-${hi}-observations`"
                        label="Observations"
                      >
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

                  <!-- Add history button -->
                  <button
                    type="button"
                    class="cursor-pointer flex items-center gap-1.5 text-xs text-blue-500 hover:text-blue-700 transition-colors self-start"
                    @click="addHistory(si)"
                  >
                    <Icon icon="lucide:circle-plus" class="size-3.5" />
                    Add history
                  </button>
                </div>
              </div>
            </div>

            <!-- Add session button -->
            <button
              type="button"
              class="cursor-pointer flex items-center gap-1.5 text-sm text-blue-500 hover:text-blue-700 transition-colors self-start font-medium"
              @click="addSession"
            >
              <Icon icon="lucide:plus" class="size-4" />
              Add session
            </button>
          </template>

          <!-- Visualize mode: readonly sessions -->
          <template v-if="formState === 'visualize' && serviceOrder">
            <div
              v-if="serviceOrder.work_sessions.length === 0"
              class="text-sm text-blue-400 text-center py-6"
            >
              No work sessions yet.
            </div>
            <div v-else class="flex flex-col gap-3">
              <div
                v-for="session in serviceOrder.work_sessions"
                :key="session.id"
                class="bg-white border border-blue-100 rounded-lg p-4 shadow-sm"
              >
                <div class="flex items-center justify-between mb-3">
                  <div>
                    <span class="text-sm font-semibold text-gray-800">{{
                      session.employee.name
                    }}</span>
                    <span
                      v-if="session.total_hours != null"
                      class="ml-2 text-xs text-blue-600 font-medium"
                    >
                      {{ (Math.floor(session.total_hours * 100) / 100).toFixed(2) }}h current total
                      hours
                    </span>
                  </div>
                  <span class="text-xs text-gray-400">
                    Registered at {{ formatDate(session.created_at) }}
                  </span>
                </div>
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
                    <span class="text-gray-400 text-xs ml-auto">{{
                      formatDate(history.occurred_at)
                    }}</span>
                    <span v-if="history.observations" class="text-gray-500 text-xs">
                      — {{ history.observations }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>

        <Separator />

        <!-- Description -->
        <div>
          <h2 class="text-xl font-bold text-gray-900">Description</h2>
          <p class="text-sm text-gray-500 mt-1">Additional details about this service order.</p>
        </div>
        <Textarea
          v-model="description"
          v-bind="descriptionAttrs"
          placeholder="Describe the service to be performed…"
          :disabled="formState === 'visualize'"
        />
      </div>

      <Separator />
      <div class="px-6 py-4 flex justify-end gap-2">
        <Button variant="outline" :to="SERVICE_ORDERS">Cancel</Button>
        <Button
          v-if="formState === 'visualize' && id"
          type="button"
          icon="lucide:send"
          :to="REPORT_SERVICE_ORDER_PROGRESS(id)"
        >
          Report progress
        </Button>
        <Button type="submit" icon="lucide:plus" v-if="formState === 'new'"
          >Create service order</Button
        >
      </div>
    </form>
  </div>
</template>
