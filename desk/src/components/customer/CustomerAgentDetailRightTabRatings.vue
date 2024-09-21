<template>
  <div>
    <div class="flex flex-col md:flex-row">
      <div class="mb-[20px] flex-1 md:px-[10px]">
        <div class="border p-4">
          <p class="text-style-general-one">Average rating</p>
        </div>
        <div class="flex justify-center border md:p-[40px]">
          <span class="rating">{{
            list_data_average_ratings?.average_rating
          }}</span>
          <span class="text-left-rating">out of 5</span>
        </div>
      </div>
      <div class="flex-1 md:px-[10px]">
        <div class="flex justify-between border p-4">
          <p class="text-style-general-one">All rating</p>
          <p class="text-style-general-two">
            {{ list_data_average_ratings?.total_tickets }}
          </p>
        </div>
        <div class="list-point-rating mb-[20px] min-h-[154px] border p-4">
          <div
            v-for="(item, index) in list_data_all_ratings"
            :key="index"
            class="rating-row"
          >
            <!-- Hiển thị số sao tương ứng với point_rating -->
            <div class="stars">
              <svg
                v-for="n in getStarCount(item.point_rating)"
                :key="n"
                viewBox="0 0 24 24"
                class="star"
              >
                <polygon
                  points="12,17.27 18.18,21 16.54,13.97 22,9.24 14.81,8.63 12,2 9.19,8.63 2,9.24 7.46,13.97 5.82,21"
                  fill="currentColor"
                />
              </svg>
            </div>

            <!-- Hiển thị phần trăm total_tickets bên cạnh -->
            <div class="percentage-bar">
              <div
                class="percentage-fill"
                :style="{
                  width: getTicketPercentage(item.total_tickets) + '%',
                }"
              ></div>
            </div>
            <span class="text-xs"
              >{{ getTicketPercentage(item.total_tickets).toFixed(2) }}%</span
            >
          </div>
        </div>
      </div>
    </div>
    <div class="min-h-[680px] space-y-4 border-t-2 px-[10px]">
      <div
        v-for="item in paginatedData"
        :key="item.id"
        class="flex flex-col items-center space-y-4 border-b-[1px] p-4 md:flex-row md:space-y-0 md:space-x-4"
      >
        <!-- Star Rating and Text -->
        <div class="grow">
          <div class="flex items-center space-x-2">
            <StarRating v-model:rating="item.feedback_rating" :static="true" />
            <!-- Title and description -->
            <div class="font-semibold text-gray-700">- {{ item.feedback }}</div>
          </div>
          <p class="mt-2 text-gray-500">{{ item.feedback_extra }}</p>
          <div class="mt-2 flex text-sm text-gray-400">
            <a :href="`#${item.id}`" class="pr-1 text-blue-500 hover:underline">
              #{{ item.id }}
            </a>
            |
            <p class="pl-1 text-gray-700">{{ item.created }}</p>
          </div>
        </div>
        <div>
          <MultipleAvatar :avatars="formatAssign(item.assign)" />
        </div>
      </div>
      <!-- Pagination Controls -->
      <div class="mt-4 flex justify-center space-x-2 items-center">
        <button
          :disabled="currentPage === 1"
          class="px-4 py-2 bg-gray-300 rounded-md flex items-center justify-center"
          @click="prevPage"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            class="h-5 w-5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button
          :disabled="currentPage === totalPages"
          class="rounded-md bg-gray-300 px-4 py-2"
          @click="nextPage"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            class="h-5 w-5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watchEffect } from "vue";
import { createResource } from "frappe-ui";
import { MultipleAvatar } from "@/components";

const list_data_all_ratings = ref([]);
const list_data_average_ratings = ref([]);
const list_data_detail_list_ticket = ref([]);
const currentPage = ref(1);
const pageSize = 5; // Số item hiển thị mỗi trang
const props = defineProps({
  user_infor: {
    type: String,
    required: true,
  },
});

const data = createResource({
  url: "helpdesk.override.api.get_data_all_ratings",
  params: {
    name: props.user_infor,
  },
  auto: true,
  onSuccess: (data) => {
    list_data_all_ratings.value = data;
  },
});

const data1 = createResource({
  url: "helpdesk.override.api.get_data_average_ratings",
  params: {
    name: props.user_infor,
  },
  auto: true,
  onSuccess: (data) => {
    list_data_average_ratings.value = data;
  },
});

const data2 = createResource({
  url: "helpdesk.override.api.get_data_detail_list_ticket",
  params: {
    name: props.user_infor,
  },
  auto: true,
  onSuccess: (data) => {
    list_data_detail_list_ticket.value = data;
    currentPage.value = 1;
  },
});

// Tính tổng số total_tickets
const totalTickets = computed(() =>
  list_data_all_ratings.value.reduce(
    (total, item) => total + item.total_tickets,
    0
  )
);

// Trả về số ngôi sao dựa trên point_rating
const getStarCount = (point_rating) => Math.round(point_rating * 5);

// Tính phần trăm dựa trên total_tickets
const getTicketPercentage = (total_tickets) => {
  return (total_tickets / totalTickets.value) * 100;
};

const formatAssign = (assignString) => {
  try {
    const assignArray = JSON.parse(assignString);
    return assignArray.map((email) => ({
      name: email,
      image: null,
      label: email,
    }));
  } catch {
    return [];
  }
};

// Tính tổng số trang
const totalPages = computed(() => {
  return Math.ceil(list_data_detail_list_ticket.value.length / pageSize);
});

// Dữ liệu phân trang cho `list_data_detail_list_ticket`
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return list_data_detail_list_ticket.value.slice(start, start + pageSize);
});

// Điều hướng trang
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};
</script>

<style scoped>
.rating-row {
  display: flex;
  align-items: center;
}

.stars {
  display: flex;
  min-width: 95px;
}

.star {
  width: 16px;
  height: 16px;
  fill: #808080;
  margin-right: 3px;
}

.percentage-bar {
  width: 155px;
  height: 8px;
  background-color: #e0e0e0;
  margin-left: 6px;
  margin-right: 6px;
  position: relative;
}

.percentage-fill {
  height: 100%;
  background-color: #4caf50;
}

.percentage-text {
  font-size: 12px;
  color: #666;
}
.rating {
  font-size: 3rem;
  font-weight: bold;
  color: #333;
  margin-right: 4px;
}
.text-left-rating {
  font-size: 1rem;
  color: #777;
  padding-top: 35px;
}
.text-style-general-one {
  font-weight: bold;
  color: #000000;
}
.text-style-general-two {
  font-weight: bold;
  color: #333;
}
.list-point-rating {
  display: grid;
  justify-content: center;
}
</style>
