<template>
  <div class="flex flex-col">
    <div class="flex justify-between py-[15px]">
      <div class="flex max-w-[50%] items-center gap-2">
        <CustomerAgentContact :contact="ticketContact" />
      </div>
      <div class="flex items-center gap-2">
        <div name="right-header" class="flex items-center gap-2">
          <RouterLink
            v-if="!configStore.preferKnowledgeBase"
            :to="{ name: CUSTOMER_PORTAL_NEW_TICKET }"
          >
            <Button
              class="bg-gray-900 text-white hover:bg-gray-800"
              label="New ticket"
              icon-right="plus"
            />
          </RouterLink>
        </div>
      </div>
    </div>
    <Tabs v-model="tabActive" :tabs="tabContent">
      <template #default="{ tab }">
        <div class="py-[20px]">
          <component :is="tab.content" />
        </div>
      </template>
    </Tabs>
  </div>
</template>

<script setup lang="ts">
import { LayoutHeader } from "@/components";
import { CUSTOMER_PORTAL_TICKET, CUSTOMER_PORTAL_NEW_TICKET } from "@/router";
import { Tabs } from "frappe-ui";
import { useConfigStore } from "@/stores/config";
import { ref, h } from "vue";
import CustomerAgentDetailRightTabGeneral from "./CustomerAgentDetailRightTabGeneral.vue";
import CustomerAgentDetailRightTabHistory from "./CustomerAgentDetailRightTabHistory.vue";
import CustomerAgentDetailRightTabTickets from "./CustomerAgentDetailRightTabTickets.vue";
import CustomerAgentDetailRightTabRatings from "./CustomerAgentDetailRightTabRatings.vue";
import CustomerAgentContact from "./CustomerAgentContact.vue";
const configStore = useConfigStore();
const props = defineProps({
  ticket: {
    type: String,
    required: true,
  },
  ticketContact: {
    type: Object,
    required: true,
  },
});
const tabContent = [
  {
    label: "General",
    content: () =>
      h(CustomerAgentDetailRightTabGeneral, {
        user_infor: props.ticket,
      }),
  },
  {
    label: "Tickets",
    content: h(CustomerAgentDetailRightTabTickets, {
      user_infor: props.ticket,
    }),
  },
  {
    label: "History",
    content: h(CustomerAgentDetailRightTabHistory, {
      user_infor: props.ticket,
    }),
  },
  {
    label: "Ratings",
    content: h(CustomerAgentDetailRightTabRatings, {
      user_infor: props.ticket,
    }),
  },
];
var tabActive = ref(0);
// const get_data_ = createResource({
//   url: "helpdesk.override.api.get_information_contact",
//   cache: ["Ticket", props.ticketId],
//   auto: true,
//   params: {
//     name: props.ticketId,
//   },
// });
</script>
