<template>
  <TransitionRoot
    ref="target"
    as="div"
    class="fixed z-40 h-screen overflow-auto bg-white"
    :show="notificationStore.visible"
    :style="{
      'box-shadow': '8px 0px 8px rgba(0, 0, 0, 0.1)',
      'max-width': '350px',
      'min-width': '350px',
      left: sidebarStore.width,
    }"
    enter="transition duration-200 ease-in-out transform"
    enter-from="-translate-x-full"
    enter-to="translate-x-0"
    leave="transition duration-200 ease-in-out transform"
    leave-from="translate-x-0"
    leave-to="-translate-x-full"
  >
    <span>
      <div
        class="sticky top-0 z-10 flex items-center justify-between border-b bg-white px-5 py-2.5"
      >
        <span class="text-lg font-medium">Notifications</span>
        <span>
          <Button
            theme="blue"
            variant="ghost"
            @click="() => notificationStore.clear.submit()"
          >
            <template #icon>
              <LucideCheckCheck class="h-4 w-4" />
            </template>
          </Button>
          <Button
            theme="gray"
            variant="ghost"
            @click="() => notificationStore.toggle()"
          >
            <template #icon>
              <LucideX class="h-4 w-4" />
            </template>
          </Button>
        </span>
      </div>
      <div class="divide-y text-base">
        <RouterLink
          v-for="n in notificationStore.data"
          :key="n.name"
          class="flex cursor-pointer items-start gap-3.5 px-5 py-2.5 hover:bg-gray-100"
          :to="getRoute(n)"
          @click="() => notificationStore.toggle()"
        >
          <UserAvatar :user="n.user_from" />
          <span>
            <div class="mb-2 leading-5">
              <component :is="getBody(n)" v-bind="n" />
            </div>
            <div class="flex items-center gap-2">
              <div class="text-sm text-gray-600">
                {{ dayjs(n.creation).fromNow() }}
              </div>
              <div
                v-if="!n.read"
                class="h-1.5 w-1.5 rounded-full bg-gray-900"
              />
            </div>
          </span>
        </RouterLink>
      </div>
    </span>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import { TransitionRoot } from "@headlessui/vue";
import { dayjs } from "@/dayjs";
import { Notification } from "@/types";
import { useSidebarStore } from "@/stores/sidebar";
import { useNotificationStore } from "@/stores/notification";
import { UserAvatar } from "@/components";
import NotificationsMention from "./NotificationsMention.vue";

const notificationStore = useNotificationStore();
const sidebarStore = useSidebarStore();
const target = ref(null);
onClickOutside(target, () => {
  if (notificationStore.visible) {
    notificationStore.toggle();
  }
});

function getBody(n: Notification) {
  switch (n.notification_type) {
    case "Mention":
      return NotificationsMention;
  }
}

function getRoute(n: Notification) {
  switch (n.notification_type) {
    case "Mention":
      return {
        name: "TicketAgent",
        params: {
          ticketId: n.reference_ticket,
        },
        hash: "#" + n.reference_comment,
      };
  }
}
</script>