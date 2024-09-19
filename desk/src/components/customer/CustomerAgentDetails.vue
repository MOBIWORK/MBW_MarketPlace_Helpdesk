<template>
  <div class="flex flex-col gap-3 px-6 pb-[25px]">
    <div
      v-for="s in sections"
      :key="s.label"
      class="flex items-center text-base leading-5"
    >
      <Tooltip :text="s.label">
        <div class="w-[126px] text-sm text-gray-600">{{ s.label }}</div>
      </Tooltip>
      <div class="flex items-center justify-between">
        <div v-if="s.value">{{ s.value }}</div>
        <!-- <Tooltip :text="s.tooltipValue">
          <Badge
            v-if="s.badgeText"
            class="-ml-1"
            :label="s.badgeText"
            variant="subtle"
            :theme="s.badgeColor"
          />
        </Tooltip> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Badge, Tooltip } from "frappe-ui";
import { dayjs } from "@/dayjs";
import { formatTime } from "@/utils";
import { dateFormat, dateTooltipFormat } from "@/utils";
import { computed } from "vue";

const props = defineProps({
  email: {
    type: String,
    required: true,
  },
  phone: {
    type: String,
    required: true,
  },
  website: {
    type: String,
    required: true,
  },
  address: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  contact: {
    type: String,
    required: true,
  },
});

// const firstResponseBadge = computed(() => {
//   let firstResponse = null;
//   if (!props.firstRespondedOn && dayjs().isBefore(dayjs(props.responseBy))) {
//     firstResponse = {
//       label: `Due in ${formatTime(dayjs(props.responseBy).diff(dayjs(), "s"))}`,
//       color: "orange",
//     };
//   } else if (dayjs(props.firstRespondedOn).isBefore(dayjs(props.responseBy))) {
//     firstResponse = {
//       label: `Fulfilled in ${formatTime(
//         dayjs(props.firstRespondedOn).diff(dayjs(props.ticketCreatedOn), "s")
//       )}`,
//       color: "green",
//     };
//   } else {
//     firstResponse = {
//       label: "Failed",
//       color: "red",
//     };
//   }
//   return firstResponse;
// });

// const resolutionBadge = computed(() => {
//   let resolution = null;
//   if (!props.resolutionDate && dayjs().isBefore(props.resolutionBy)) {
//     resolution = {
//       label: `Due in ${formatTime(
//         dayjs(props.resolutionBy).diff(dayjs(), "s")
//       )}`,
//       color: "orange",
//     };
//   } else if (dayjs(props.resolutionDate).isBefore(props.resolutionBy)) {
//     resolution = {
//       label: `Fulfilled in ${formatTime(
//         dayjs(props.resolutionDate).diff(dayjs(props.ticketCreatedOn), "s")
//       )}`,
//       color: "green",
//     };
//   } else {
//     resolution = {
//       label: "Failed",
//       color: "red",
//     };
//   }
//   return resolution;
// });
const sections = computed(() => [
  {
    label: "Email",
    value: props.email,
  },
  {
    label: "Phone",
    value: props.phone,
  },
  {
    label: "Website",
    value: props.website,
  },
  {
    label: "Address",
    value: props.address,
  },
  {
    label: "Description",
    value: props.description,
  },
  {
    label: "Primary Contact",
    value: props.contact,
  },
]);
</script>
