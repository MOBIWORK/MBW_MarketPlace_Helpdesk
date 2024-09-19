<template>
  <div class="flex flex-col">
    <LayoutHeader>
      <template #left-header>
        <div class="text-lg font-medium text-gray-900">Customers</div>
      </template>
      <!-- <template #right-header>
        <Button
          label="New customer"
          theme="gray"
          variant="solid"
          @click="isDialogVisible = !isDialogVisible"
        >
          <template #prefix>
            <LucidePlus class="h-4 w-4" />
          </template>
        </Button>
      </template> -->
    </LayoutHeader>
    <!-- <CustomerAgentList
      :rows="tickets?.data?.data || []"
      :columns="columns"
      :page-length="pageLength"
      :col-field-type="colFieldType"
      :options="{
        rowCount: tickets?.data?.row_count,
        totalCount: tickets?.data?.total_count,
      }"
      @update:page-length="updatePageLength"
      @event:field-click="processFieldClick"
      @event:export="
        (e) => {
          exportRows(e.export_type, e.export_all, e.selections);
        }
      "
    /> -->
    <!-- <ListView
      :columns="columns"
      :resource="customers"
      class="mt-2.5"
      doctype="HD Customer"
    >
      <template #name="{ data }">
        <div class="flex items-center gap-2">
          <Avatar :label="data.name" :image="data.image" size="sm" />
          <div class="line-clamp-1">{{ data.name }}</div>
        </div>
      </template>
    </ListView> -->
    <!-- <NewCustomerDialog
      v-model="isDialogVisible"
      @customer-created="handleCustomer"
    />
    <span v-if="isCustomerDialogVisible">
      <CustomerDialog
        v-model="isCustomerDialogVisible"
        :name="selectedCustomer"
        @customer-updated="handleCustomer(true)"
      />
    </span> -->
    <CustomerAgentList
      :rows="tickets?.data?.data || []"
      :columns="columns"
      :page-length="pageLength"
      :col-field-type="colFieldType"
      :options="{
        rowCount: tickets?.data?.row_count,
        totalCount: tickets?.data?.total_count,
      }"
      @update:page-length="updatePageLength"
      @event:field-click="processFieldClick"
      @event:export="
        (e) => {
          exportRows(e.export_type, e.export_all, e.selections);
        }
      "
    />
  </div>
</template>
<script setup lang="ts">
import { ref, computed } from "vue";
import { createResource, usePageMeta, Avatar } from "frappe-ui";
import { createListManager } from "@/composables/listManager";
import NewCustomerDialog from "@/components/desk/global/NewCustomerDialog.vue";
import { ListView } from "@/components";
import CustomerDialog from "./CustomerDialog.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import { CustomerAgentList } from "@/components/customer";
import { useStorage } from "@vueuse/core";
import { useUserStore } from "@/stores/user";
const { getUser } = useUserStore();

const isDialogVisible = ref(false);
const isCustomerDialogVisible = ref(false);
const selectedCustomer = ref(null);

let storage = useStorage("tickets_agent", {
  filtersToApply: {},
  filters: [],
  sorts: [],
  sortsToApply: "modified desc",
  columns: [],
  rows: [],
  pageLength: 20,
});

let columns = storage.value.columns ? storage.value.columns : [];
let rows = storage.value.rows ? storage.value.rows : [];

let filtersToApply = storage.value.filtersToApply;
let filters = ref(storage.value.filters);

let sorts = ref(storage.value.sorts);
let sortsToApply = storage.value.sortsToApply;

let pageLength = ref(storage.value.pageLength);
let pageLengthCount = pageLength.value;

const tickets = createResource({
  url: "helpdesk.api.doc.get_list_data",
  params: {
    doctype: "Customer",
    filters: filtersToApply,
    order_by: sortsToApply,
    page_length: pageLength.value,
    columns: columns.length ? columns : undefined,
    rows: rows.length ? rows : undefined,
  },
  auto: true,
  transform(data) {
    data.data.forEach((row) => {
      row.name = row.name.toString();
      let _assign = row._assign ? JSON.parse(row._assign) : null;
      row._assign = [];

      if (_assign && _assign.length) {
        _assign.forEach((assign) => {
          let _user = getUser(assign);
          row._assign.push({
            name: _user.name,
            label: _user.full_name,
            image: _user.user_image,
          });
        });
      } else {
        row._assign = {
          name: "",
          label: "Unassigned",
          image: "",
        };
      }
    });
  },
  onSuccess(data) {
    columns = data.columns;
    console.log("Column ", columns);
    rows = data.rows;
    console.log("Data ", data);
  },
});
const fields = computed(() => {
  return tickets?.data?.fields.filter((field) => {
    return colFieldType.value[field.value] == undefined;
  });
});

const colFieldType = computed(() => {
  let obj = {};
  tickets?.data?.columns.forEach((column) => {
    obj[column.key] = column.type;
  });
  return obj;
});

function updatePageLength(value) {
  if (value == "loadMore") {
    pageLengthCount = tickets.data.data.length + pageLength.value;
  } else {
    pageLength.value = value;
    pageLengthCount = value;
    storage.value.pageLength = value;
  }

  apply();
}
function apply() {
  tickets.update({
    params: {
      order_by: sortsToApply,
      filters: filtersToApply,
      page_length: pageLengthCount,
      doctype: "Customer",
      columns: columns.length ? columns : undefined,
      rows: rows.length ? rows : undefined,
    },
  });

  tickets.reload();
}
function processFieldClick(event) {
  filters.value.push({
    field: filterableFields.data.find((f) => f.fieldname === event.name),
    operator: "is",
    value: event.value,
  });

  if (event.name == "_assign") {
    filtersToApply[event.name] = ["LIKE", `%${event.value}%`];
  } else {
    filtersToApply[event.name] = ["=", event.value];
  }
  storage.value.filters = filters.value;
  storage.value.filtersToApply = filtersToApply;

  apply();
}
const filterableFields = createResource({
  url: "helpdesk.api.doc.get_filterable_fields",
  cache: ["DocField", "Customer"],
  auto: true,
  params: {
    doctype: "Customer",
    append_assign: true,
  },
  transform: (data) => {
    return data
      .sort((fieldA, fieldB) => {
        const labelA = fieldA.label.toUpperCase();
        const labelB = fieldB.label.toUpperCase();
        if (labelA < labelB) {
          return -1;
        }
        if (labelA > labelB) {
          return 1;
        }

        return 0;
      })
      .map((field) => {
        return {
          label: field.label,
          value: field.fieldname,
          ...field,
        };
      });
  },
});

async function exportRows(export_type, export_all, selections) {
  let filters;
  let page_length;
  let fields = JSON.stringify(columns.map((f) => f.key));
  let order_by = sortsToApply;

  if (export_all) {
    filters = JSON.stringify(filtersToApply);
    page_length = tickets?.data?.total_count;
  } else {
    let filtersClone = { ...filtersToApply };
    filtersClone["name"] = ["IN", selections];
    filters = JSON.stringify(filtersClone);
    page_length = selections.length;
  }

  window.location.href = `/api/method/frappe.desk.reportview.export_query?file_format_type=${export_type}&title=Customer&doctype=Customer&fields=${fields}&filters=${filters}&order_by=${order_by}&page_length=${page_length}&start=0&view=Report&with_comment_count=1`;
}
// const emptyMessage = "No Customers Found";
// const columns = [
//   {
//     label: "Name",
//     key: "name",
//     width: "w-80",
//   },
//   {
//     label: "Email",
//     key: "email_id",
//     width: "w-80",
//   },
//   {
//     label: "Phone",
//     key: "mobile_no",
//     width: "w-80",
//   },
//   {
//     label: "Primary Contact Email",
//     key: "email_id",
//     width: "w-80",
//   },
// ];

// const customers = createListManager({
//   doctype: "HD Ticket",
//   fields: ["name"],
//   auto: true,
//   transform: (data) => {
//     for (const d of data) {
//       d.onClick = () => openCustomer(d.name);
//     }
//     return data;
//   },
// });

usePageMeta(() => {
  return {
    title: "Customers",
  };
});

// function openCustomer(id: string) {
//   selectedCustomer.value = id;
//   isCustomerDialogVisible.value = true;
// }
// function handleCustomer(updated = false) {
//   updated
//     ? (isCustomerDialogVisible.value = false)
//     : (isDialogVisible.value = false);
//   customers.reload();
// }
</script>
