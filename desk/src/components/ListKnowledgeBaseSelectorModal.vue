<template>
  <Dialog
    v-model="show"
    :options="{ title: 'List Knowledge Base', size: '2xl' }"
  >
    <template #body-content>
      <TextInput
        ref="searchInput"
        v-model="search"
        type="text"
        :placeholder="'List Knowledge'"
        @input="debouncedSearch"
      >
        <template #prefix>
          <FeatherIcon name="search" class="h-4 w-4 text-gray-500" />
        </template>
      </TextInput>
      <div
        v-if="filteredList.length"
        class="mt-4 grid max-h-[560px] grid-cols-1 overflow-y-auto"
      >
        <div
          v-for="template in filteredList"
          :key="template.category_level_three"
          class="flex cursor-pointer flex-col gap-2 p-2 hover:bg-gray-100"
          @click="emit('apply', template)"
        >
          <div class="border-b pb-2 text-base">
            {{ template.category_beadcrum }}
          </div>
        </div>
      </div>
      <div v-else class="mt-2">
        <div class="flex h-56 flex-col items-center justify-center">
          <div class="text-lg text-gray-500">
            {{ "No templates found" }}
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { TextEditor, createListResource, createResource } from "frappe-ui";
import { ref, computed, nextTick, watch, onMounted } from "vue";

const emit = defineEmits(["apply"]);
const show = defineModel();
const searchInput = ref("");

const search = ref("");
const list_data_knowledge_base = ref([]);
const filteredList = ref([]);

// Fetch data
const data = createResource({
  url: "helpdesk.override.api.get_data_list_knowledge_base",
  auto: true,
  onSuccess: (data) => {
    list_data_knowledge_base.value = data;
    // Set filteredList to the complete list on initial load
    filteredList.value = data;
  },
});

// Debounce function to limit search frequency
const debounce = (func, delay) => {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
};

// Method to perform the search
const performSearch = () => {
  const searchTerm = search.value.toLowerCase();
  filteredList.value = list_data_knowledge_base.value.filter((template) =>
    template.category_beadcrum.toLowerCase().includes(searchTerm)
  );
};

// Debounced version of the search method
const debouncedSearch = debounce(performSearch, 500);

// Focus search input when dialog is shown
watch(show, (value) => {
  if (value) {
    nextTick(() => searchInput.value?.el?.focus());
  }
});
</script>
