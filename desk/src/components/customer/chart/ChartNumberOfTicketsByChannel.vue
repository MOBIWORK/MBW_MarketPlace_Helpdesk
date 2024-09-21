<template>
  <div class="md:px-[10px]">
    <!-- A1: Title and description -->
    <div class="border p-4">
      <p class="">Number of tickets by channel</p>
    </div>

    <!-- A2: Chart (biểu đồ) -->
    <div class="border p-4">
      <!-- <div id="doughnut-chart" style="width: 100%; height: 300px"></div> -->
      <div
        v-if="data"
        id="doughnut-chart"
        style="min-width: 260px; min-height: 260px"
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
  url: "helpdesk.override.api.get_data_number_of_ticket_by_channel",
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

  const chartData = res_data[2]; // Mảng dữ liệu biểu đồ từ API
  const chartDataLegend = res_data[1];
  const totalTickets = res_data[0]; // Tổng số phiếu từ API
  const option = {
    tooltip: {
      trigger: "item",
    },
    legend: {
      bottom: "0",
      left: "center",
      formatter: (name) => {
        const item = chartDataLegend
          ? chartDataLegend.find((d) => d.name === name)
          : null;
        if (item) {
          const convert_percent = item.percent.toFixed(0);
          // Sử dụng rich text key để định dạng phần value
          return `{bold|${item.value}} ${item.name} (${convert_percent}%)`;
        }
        return name;
      },
      textStyle: {
        rich: {
          bold: {
            fontWeight: "bold", // Làm đậm phần value
            color: "#000", // Màu sắc cho phần đậm (tùy chỉnh)
          },
        },
      },
    },
    series: [
      {
        name: "Tickets",
        type: "pie",
        radius: ["50%", "70%"],
        center: ["50%", "50%"],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: "center",
          formatter: () =>
            `{title|Total Tickets}\n{value|${
              totalTickets ? totalTickets.total_tickets : ""
            }}`,
          rich: {
            title: {
              fontSize: 16,
              color: "#333",
              lineHeight: 30,
              padding: [0, 0, 15, 0], // Cách title 15px từ giá trị
            },
            value: {
              fontSize: 24,
              color: "#333",
              fontWeight: "bold",
            },
          },
        },
        data: chartData, // Dữ liệu được lấy từ API
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
  chartDom.value = document.getElementById("doughnut-chart");
  if (list_data.value) {
    initOrUpdateChart(); // Khởi tạo biểu đồ khi DOM đã sẵn sàng và có dữ liệu
  }
});
</script>
