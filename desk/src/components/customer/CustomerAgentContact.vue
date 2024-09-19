<template>
  <div class="flex items-center justify-start py-[9px] px-[16px]">
    <Avatar
      size="md"
      class="h-[35px] w-[35px]"
      :image="contact?.image"
      :label="contact?.name"
    />
    <div class="flex flex-col">
      <div class="w-[242px] pl-[15px] text-md font-medium text-black">
        {{ contact?.name }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Tooltip, Avatar } from "frappe-ui";
import { EmailIcon, TicketIcon } from "@/components/icons/";

const props = defineProps({
  contact: {
    type: Object,
    required: true,
  },
});

// const emit = defineEmits(["email:open"]);

// function openEmailBox() {
//   emit("email:open", props.contact.email_id);
// }
</script>
