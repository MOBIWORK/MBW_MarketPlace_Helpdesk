<template>
  <div class="md:px-[10px]">
    <!-- A1: Title and description -->
    <div class="border p-4">
      <p class="">Number of tickets by status</p>
    </div>

    <!-- A2: Chart (biểu đồ) -->
    <div class="border p-4">
      <!-- <div id="doughnut-chart" style="width: 100%; height: 300px"></div> -->
      <div
        v-if="data"
        id="doughnut-chart-status"
        style="min-width: 310px; min-height: 310px"
      ></div>
      <div v-else><Spinner class="w-8" /></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import * as echarts from "echarts";
import { createResource, Spinner } from "frappe-ui";

const chartInstance = ref(null);
const chartDom = ref(null);
const list_data = ref();
// const data = [
//   { value: 1048, name: "Search Engine" },
//   { value: 735, name: "Direct" },
//   { value: 580, name: "Email" },
//   { value: 484, name: "Union Ads" },
//   { value: 300, name: "Video Ads" },
// ];
const props = defineProps({
  user_infor: {
    type: String,
    required: true,
  },
});
const data = createResource({
  url: "helpdesk.override.api.get_data_number_of_ticket_by_status",
  params: {
    name: props.user_infor,
  },
  auto: true,
  onSuccess: (data) => {
    list_data.value = data;
  },
});

// Hàm để khởi tạo hoặc cập nhật biểu đồ
const initOrUpdateChart = () => {
  var res_data = list_data.value;
  if (!chartInstance.value && chartDom.value) {
    // Khởi tạo biểu đồ nếu chưa tồn tại
    chartInstance.value = echarts.init(chartDom.value);
  }

  if (!res_data || !chartInstance.value) return;

  const chartData = res_data; // Mảng dữ liệu biểu đồ từ API
  const option = {
    // title: {
    //   text: "Referer of a Website",
    //   subtext: "Fake Data",
    //   left: "center",
    // },
    tooltip: {
      trigger: "item",
    },
    // legend: {
    //   orient: "vertical",
    //   left: "left",
    // },
    series: [
      {
        name: "Status",
        type: "pie",
        radius: "65%",
        data: chartData,
      },
    ],
  };

  // Set options cho biểu đồ
  chartInstance.value.setOption(option);
};

// Quan sát sự thay đổi của data để cập nhật biểu đồ khi có dữ liệu mới
watch(list_data, (newData) => {
  if (newData) {
    initOrUpdateChart(); // Chỉ khởi tạo hoặc cập nhật khi có dữ liệu
  }
});

// Đảm bảo biểu đồ được khởi tạo sau khi DOM đã sẵn sàng
onMounted(() => {
  chartDom.value = document.getElementById("doughnut-chart-status");
  if (list_data.value) {
    initOrUpdateChart(); // Khởi tạo biểu đồ khi DOM đã sẵn sàng và có dữ liệu
  }
});
</script>
