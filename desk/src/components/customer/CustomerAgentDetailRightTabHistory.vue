<template>
  <div class="flw-full flex-col pb-[20px] md:px-[10px]">
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
    >
      <template #group-header="{ group }">
        <span class="text-base font-medium leading-6 text-gray-900">
          {{ group.group }} ({{ group.rows.length }})
        </span>
      </template>
    </ListView>
  </div>
</template>

<script setup lang="ts">
import { ListView, Avatar, createResource } from "frappe-ui";
import { ref, h, computed } from "vue";
import { MultipleAvatar } from "@/components";

const list_data_tickets_time = ref([]);
const props = defineProps({
  user_infor: {
    type: String,
    required: true,
  },
});
const data = createResource({
  url: "helpdesk.override.api.get_data_tickets_time",
  params: {
    name: props.user_infor,
  },
  auto: true,
  onSuccess: (data) => {
    list_data_tickets_time.value = data;
  },
});
const columns = [
  {
    label: "ID",
    key: "id",
    width: "150px",
  },
  {
    label: "Title",
    key: "title",
  },
  {
    label: "creator",
    key: "creator",
  },
  {
    label: "Status",
    key: "status",
    width: "100px",
  },
];
const rows = list_data_tickets_time;
</script>
