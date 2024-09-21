<template>
  <div class="w-full flex-col pb-[20px] md:px-[10px]">
    <div class="border p-4">
      <p class="">Pending tickets ( {{ pendingTicketsCount }} )</p>
    </div>
    <div class="border p-4">
      <ListView
        class="h-auto"
        :columns="columns"
        :rows="rows"
        :options="{
          emptyState: {
            title: 'No Data',
            description: 'No data available',
          },
          getRowRoute: (row) => ({
            name: 'TicketAgent',
            params: { ticketId: row.name },
          }),
          showTooltip: true,
          resizeColumn: true,
        }"
        row-key="name"
      />
    </div>
  </div>
  <div class="flex flex-col md:grid md:grid-cols-2">
    <!-- Component A -->
    <div class="flex-1">
      <ChartNumberOfTicketsByChannel :user_infor="props.user_infor" />
    </div>
    <!-- Component B -->
    <div class="flex-1">
      <ChartNumberOfTicketsByStatus :user_infor="props.user_infor" />
    </div>
  </div>
</template>

<script setup lang="ts">
import ChartNumberOfTicketsByChannel from "./chart/ChartNumberOfTicketsByChannel.vue";
import ChartNumberOfTicketsByStatus from "./chart/ChartNumberOfTicketsByStatus.vue";
import { ListView, Avatar, createResource } from "frappe-ui";
import { ref, h, computed } from "vue";
import { MultipleAvatar } from "@/components";

const list_data_pending_tickets = ref([]);
const props = defineProps({
  user_infor: {
    type: String,
    required: true,
  },
});
const data = createResource({
  url: "helpdesk.override.api.get_data_pending_tickets",
  params: {
    name: props.user_infor,
  },
  auto: true,
  onSuccess: (data) => {
    list_data_pending_tickets.value = data;
  },
});
const pendingTicketsCount = computed(
  () => list_data_pending_tickets.value.length
);
const columns = [
  {
    label: "ID",
    key: "id",
    width: "50px",
  },
  {
    label: "Title",
    key: "title",
  },
  {
    label: "Created",
    key: "created",
  },
  {
    label: "Priority",
    key: "priority",
  },
  {
    label: "Assignee",
    key: "assigns",
    prefix: ({ row }) => {
      let list_assign = JSON.parse(row.assign) || [];
      let avatars = [];
      if (list_assign) {
        avatars = list_assign.map((item) => ({
          image: null,
          label: item,
          name: item,
        }));
      }

      return h(MultipleAvatar, {
        avatars: avatars,
      });
    },
  },
];
const rows = list_data_pending_tickets;
</script>
