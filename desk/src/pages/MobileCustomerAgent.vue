<template>
  <div class="flex flex-col md:flex-col lg:flex-col xl:flex-row">
    <div class="w-full p-4 md:w-full xl:w-1/4">
      <CustomerAgentDetailLeft :ticket="ticket.data" />
    </div>
    <div class="w-full p-4 md:w-full xl:w-3/4">
      <CustomerAgentDetailRight
        :ticket="props.ticketId"
        :ticket-contact="ticket.data"
      />
    </div>
    <!-- <TicketAgentActivities
          ref="ticketAgentActivitiesRef"
          :activities="activities"
          @update="
            () => {
              ticket.reload();
            }
          "
          @email:reply="
            (e) => {
              communicationAreaRef.replyToEmail(e);
            }
          "
        /> -->
  </div>
</template>

<script setup lang="ts">
import { computed, ref, h, watch, onMounted, onUnmounted } from "vue";
import { useStorage } from "@vueuse/core";
import {
  Breadcrumbs,
  Dropdown,
  Switch,
  createResource,
  Dialog,
  FormControl,
} from "frappe-ui";

import {
  LayoutHeader,
  MultipleAvatar,
  AssignmentModal,
  CommunicationArea,
} from "@/components";
import { TicketAgentActivities, TicketAgentSidebar } from "@/components/ticket";
import {
  CustomerAgentDetailLeft,
  CustomerAgentDetailRight,
} from "@/components/customer";
import { IndicatorIcon } from "@/components/icons";

import { useTicketStatusStore } from "@/stores/ticketStatus";
import { useUserStore } from "@/stores/user";
import { createToast, setupCustomActions } from "@/utils";

const ticketStatusStore = useTicketStatusStore();
const { getUser } = useUserStore();
const ticketAgentActivitiesRef = ref(null);
const communicationAreaRef = ref(null);
const subjectInput = ref(null);
const isLoading = ref(false);

const props = defineProps({
  ticketId: {
    type: String,
    required: true,
  },
});

let storage = useStorage("ticket_agent", {
  showAllActivity: true,
});

const showFullActivity = ref(storage.value.showAllActivity);
const showAssignmentModal = ref(false);
const showSubjectDialog = ref(false);

const ticket = createResource({
  url: "helpdesk.override.api.get_information_contact",
  cache: ["Ticket", props.ticketId],
  auto: true,
  params: {
    name: props.ticketId,
  },
});

// const breadcrumbs = computed(() => {
//   let items = [{ label: "Tickets", route: { name: "TicketsAgent" } }];
//   items.push({
//     label: ticket.data?.subject,
//     route: { name: "TicketAgent" },
//   });
//   return items;
// });

// watch(
//   () => showFullActivity.value,
//   (value) => {
//     storage.value.showAllActivity = value;
//   }
// );

// const dropdownOptions = computed(() =>
//   ticketStatusStore.options.map((o) => ({
//     label: o,
//     value: o,
//     onClick: () => updateTicket("status", o),
//     icon: () =>
//       h(IndicatorIcon, {
//         class: ticketStatusStore.textColorMap[o],
//       }),
//   }))
// );

// const activities = computed(() => {
//   const emailProps = ticket.data.communications.map((email) => {
//     return {
//       type: "email",
//       key: email.creation,
//       sender: { name: email.user.email, full_name: email.user.name },
//       to: email.recipients,
//       cc: email.cc,
//       bcc: email.bcc,
//       creation: email.creation,
//       subject: email.subject,
//       attachments: email.attachments,
//       content: email.content,
//     };
//   });

//   const commentProps = ticket.data.comments.map((comment) => {
//     return {
//       name: comment.name,
//       type: "comment",
//       key: comment.creation,
//       commentedBy: comment.commented_by,
//       commenter: comment.user.name,
//       creation: comment.creation,
//       content: comment.content,
//     };
//   });

//   if (!showFullActivity.value) {
//     return [...emailProps, ...commentProps].sort(
//       (a, b) => new Date(a.creation) - new Date(b.creation)
//     );
//   }

//   const historyProps = [...ticket.data.history, ...ticket.data.views].map(
//     (h) => {
//       return {
//         type: "history",
//         key: h.creation,
//         content: h.action ? h.action : "viewed this",
//         creation: h.creation,
//         user: h.user.name + " ",
//       };
//     }
//   );

//   const sorted = [...emailProps, ...commentProps, ...historyProps].sort(
//     (a, b) => new Date(a.creation) - new Date(b.creation)
//   );

//   const data = [];
//   let i = 0;

//   while (i < sorted.length) {
//     const currentActivity = sorted[i];
//     if (currentActivity.type === "history") {
//       currentActivity.relatedActivities = [];
//       for (let j = i + 1; j < sorted.length + 1; j++) {
//         const nextActivity = sorted[j];
//         if (nextActivity && nextActivity.type === "history") {
//           currentActivity.relatedActivities.push(nextActivity);
//         } else {
//           data.push(currentActivity);
//           i = j - 1;
//           break;
//         }
//       }
//     } else {
//       data.push(currentActivity);
//     }
//     i++;
//   }

//   return data;
// });

// function updateTicket(fieldname: string, value: string) {
//   isLoading.value = true;
//   createResource({
//     url: "frappe.client.set_value",
//     params: {
//       doctype: "HD Ticket",
//       name: props.ticketId,
//       fieldname,
//       value,
//     },
//     auto: true,
//     onSuccess: () => {
//       isLoading.value = false;
//       ticket.reload();
//       createToast({
//         title: "Ticket updated",
//         icon: "check",
//         iconClasses: "text-green-600",
//       });
//     },
//     onError: (e) => {
//       isLoading.value = false;

//       const title =
//         e.messages && e.messages.length > 0
//           ? e.messages[0]
//           : "Failed to update ticket";

//       createToast({
//         title,
//         icon: "x",
//         iconClasses: "text-red-600",
//       });
//     },
//   });
// }
// onMounted(() => {
//   document.title = props.ticketId;
// });

// onUnmounted(() => {
//   document.title = "Helpdesk";
// });
</script>
