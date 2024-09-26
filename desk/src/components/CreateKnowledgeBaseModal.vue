<template>
  <Dialog v-model="show" :options="{ title: 'New article', size: '2xl' }">
    <template #body-title>
      <p class="text-xl font-semibold">New article</p>
    </template>
    <template #body-content>
      <div class="pb-5">
        <FormControl
          v-model="titlemess"
          :type="'text'"
          size="sm"
          variant="subtle"
          placeholder="Title"
          :disabled="false"
        />
      </div>

      <div class="pb-5">
        <FormControl
          v-model="category"
          type="autocomplete"
          :options="list_data_knowledge_base"
          size="sm"
          variant="subtle"
          placeholder="Category"
          :disabled="false"
        />
      </div>
      <div class="pb-5">
        <FormControl
          v-model="subcategory"
          type="autocomplete"
          :options="list_data_sub_category"
          size="sm"
          variant="subtle"
          placeholder="Sub-category"
          :disabled="false"
        />
      </div>
      <div class="mt-3">
        <p class="mb-8 text-xl font-semibold">Content</p>
        <FormControl
          v-model="contentmess"
          :value="props.content"
          style="min-height: 250px"
          :type="'text'"
          size="sm"
          variant="subtle"
          placeholder=""
          :disabled="false"
        />
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end gap-2">
        <button
          class="rounded-md bg-gray-100 px-5 py-1 font-semibold text-black transition-all duration-300 hover:bg-gray-200"
          @click="createArticle('button_create')"
        >
          Create
        </button>
        <button
          class="rounded-md bg-black px-5 py-1 font-semibold text-white transition-all duration-300 hover:bg-gray-800"
          @click="createArticle('button_publish')"
        >
          Publish
        </button>
      </div>
    </template>
  </Dialog>
  <SuccessNotification
    :show="showNotification"
    :message="notificationMessage"
    :type="notificationType"
  />
</template>

<script setup lang="ts">
import {
  TextEditor,
  createListResource,
  createResource,
  FormControl,
} from "frappe-ui";
import { ref, computed, nextTick, watch, onMounted } from "vue";
import { SuccessNotification } from "@/components";

const contentmess = ref();
const titlemess = ref();
const list_data_knowledge_base = ref([]);
const list_data_sub_category = ref([]);
const category = ref(null);
const subcategory = ref(null);
const emit = defineEmits(["apply"]);
const show = defineModel();
const showNotification = ref(false);
const notificationMessage = ref("");
const notificationType = ref("");

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
});
// Fetch data
const data_category = createResource({
  url: "helpdesk.override.api.get_data_list_category_knowledge_base",
  auto: true,
  onSuccess: (data) => {
    list_data_knowledge_base.value = data;
  },
});

watch(category, (newCategory) => {
  if (newCategory) {
    const data_sub_category = createResource({
      url: "helpdesk.override.api.get_data_list_sub_category_knowledge_base",
      params: {
        context_category: newCategory.value,
      },
      auto: true,
      onSuccess: (data) => {
        list_data_sub_category.value = data;
      },
    });
  }
});
function createArticle(type) {
  const param = {
    title: titlemess.value,
    category: category.value,
    subcategory: subcategory.value,
    content: props.content,
    published: type === "button_create" ? "button_create" : "button_publish",
  };
  const data_sub_category = createResource({
    url: "helpdesk.override.api.action_create_new_article",
    params: param,
    auto: true,
    onSuccess: (response) => {
      if (response.status === 200) {
        notificationMessage.value = "Article created successfully!";
        notificationType.value = "success";
      } else {
        notificationMessage.value = response.error;
        notificationType.value = "error";
      }
      showNotification.value = true;

      // Ẩn thông báo sau 3 giây
      setTimeout(() => {
        showNotification.value = false;
      }, 3000);
    },
    onError: (error) => {
      notificationMessage.value = "There was an error creating the article.";
      notificationType.value = "error";
      showNotification.value = true;

      setTimeout(() => {
        showNotification.value = false;
      }, 3000);
    },
  });
  emit("apply");
}
</script>
