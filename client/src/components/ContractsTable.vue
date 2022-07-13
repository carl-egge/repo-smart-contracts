<template>
  <div>
    <h2>All Smart Contracts</h2>
    <b-container fluid>
      <!-- Add New Button -->
      <b-row>
        <b-col lg="2" md="2" sm="12">
          <b-button
            @click="$router.push('/add')"
            variant="warning"
            class="mb-3"
          >
            Create Contract
          </b-button>
        </b-col>

        <!-- Filter -->
        <b-col lg="5" md="5" sm="8">
          <b-form-group
            label="Filter"
            label-for="filter-input"
            label-cols-sm="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-3"
          >
            <b-input-group size="sm">
              <b-form-input
                id="filter-input"
                v-model="filter"
                type="search"
                placeholder="Search on current page"
              ></b-form-input>

              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">
                  Clear
                </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
        </b-col>

        <!-- Pagination: Set entries per page -->
        <b-col lg="3" md="3" sm="4">
          <b-form-group
            label="Per page"
            label-for="per-page-select"
            label-cols-sm="6"
            label-cols-md="4"
            label-cols-lg="3"
            label-align-sm="right"
            label-size="sm"
            class="mb-3"
          >
            <b-form-select
              id="per-page-select"
              v-model="perPage"
              :options="pageOptions"
              size="sm"
              @change="handlePageSizeChange($event)"
            ></b-form-select>
          </b-form-group>
        </b-col>
      </b-row>

      <!-- Main table element -->
      <b-table
        :items="contracts"
        :fields="fields"
        :filter="filter"
        :filter-included-fields="filterOn"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
        :busy="isBusy"
        stacked="md"
        hover
        show-empty
        head-variant="light"
        @filtered="onFiltered"
      >
        <!-- Row: Title (format bold) -->
        <template #cell(title)="data">
          <b>{{ data.value }}</b>
        </template>

        <!-- Row: Versions Quantity -->
        <template #cell(versions)="data">
          {{ data.value.length }}
        </template>

        <!-- Row: Compiler Version -->
        <template #cell(compilerversion)="data">
          {{ data.value }}
        </template>

        <!-- Row: ID -->
        <template #cell(id)="data">
          <router-link :to="'/contracts/' + data.value">
            {{ data.value }}
          </router-link>
        </template>

        <!-- Row: Actions (Buttons) -->
        <template #cell(actions)="row">
          <!-- Update Button @click="$router.push('/contracts/' +row.item.id)"-->
          <b-button
            @click="$router.push('/contracts/' + row.item.id)"
            variant="primary"
            class="mx-1 mb-xl-0 mb-1"
          >
            <b-icon-pencil></b-icon-pencil>
          </b-button>

          <!-- Delete Button -->
          <b-button
            @click="destroyContract(row.item)"
            variant="danger"
            class="mx-1 mb-xl-0 mb-1"
          >
            <b-icon-trash></b-icon-trash>
          </b-button>
        </template>

        <!-- Loading Spinner when fetching data -->
        <template #table-busy>
          <div class="text-center text-secondary my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>

      <!-- Pagination: Switch between pages. -->
      <b-row align-h="center">
        <b-col class="my-1 mb-5" md="5">
          <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            align="fill"
            size="sm"
            class="my-0"
            @change="handlePageChange($event)"
          ></b-pagination>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import ContractsService from "@/services/ContractsService";
export default {
  name: "contracts",
  data() {
    return {
      contracts: [],

      fields: [
        {
          key: "title",
          label: "Contract name",
          sortable: true,
          sortDirection: "desc",
        },
        {
          key: "id",
          label: "ID",
          sortable: true,
          class: "text-center",
        },
        {
          key: "source",
          label: "Source",
          sortable: true,
        },
        {
          key: "versions",
          label: "Quantity versions",
          sortable: true,
          class: "text-center",
        },
        {
          key: "compilerversion",
          label: "Compiler Version",
          sortable: true,
          class: "text-center",
        },
        { key: "actions", label: "Actions", class: "text-center" },
      ],

      // Table Settings
      isBusy: false,
      totalRows: 1,
      totalDBsize: 0,
      currentPage: 1,
      perPage: 5,
      pageOptions: [5, 10, 25, 100],
      sortBy: "",
      sortDesc: true,
      sortDirection: "desc",
      filter: null,
      filterOn: [],
    };
  },
  mounted() {
    this.getContracts();
  },
  methods: {
    /**
     * getContracts
     *
     * API call to get the list of contracts
     */
    async getContracts() {
      this.isBusy = true;
      const params = this.getRequestParams(this.currentPage, this.perPage);
      const response = await ContractsService.getAll(params);
      this.totalRows = parseInt(response.headers["x-total-db-size"]);
      this.contracts = response.data;
      this.contracts.forEach((element) => {
        element.compilerversion =
          element.versions[element.latestVersion - 1].content.compilerversion;
      });
      this.isBusy = false;
    },

    /**
     * getRequestParams
     *
     * calculate params for getContracts
     */
    getRequestParams(page, pageSize) {
      let params = {};
      if (page) {
        params["skip"] = (page - 1) * pageSize;
      }
      if (pageSize) {
        params["limit"] = pageSize;
      }
      return params;
    },

    /**
     * destroyContract
     *
     * API call to delete contract after confirmation
     */
    async destroyContract(contract) {
      if (confirm("Do you really want to delete " + contract.title + "?")) {
        const response = await ContractsService.delete(contract.id);
        if (response.status == "204") {
          this.$parent.makeToast(
            "204 :: Success",
            "The contract was deleted.",
            "success"
          );
          this.getContracts();
        } else {
          this.$parent.makeToast(
            "422 :: Error",
            "Something went wrong.",
            "danger"
          );
          this.getContracts();
        }
      } else {
        this.$parent.makeToast("Error", "Contract was not deleted.", "danger");
      }
    },

    async deleteContract() {
      const response = await ContractsService.delete(this.contract.id);
      if (response.status == "204") {
        this.$parent.makeToast(
          "204 :: Success",
          "The contract was deleted.",
          "success"
        );
        this.$router.push("/");
      } else {
        this.$parent.makeToast(
          "422 :: Error",
          "Something went wrong.",
          "danger"
        );
        this.getContract(this.contract.id);
      }
    },

    /**
     * onFiltered
     *
     * Trigger pagination to update the number of buttons/pages due to filtering
     */
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },

    /**
     * handlePaginationChange
     *
     * Trigger pagination to request new objects
     */
    handlePageChange(value) {
      this.currentPage = value;
      this.getContracts();
    },

    /**
     * handlePageSizeChange
     *
     * update contracts if Pagination size is changed
     */
    handlePageSizeChange(value) {
      this.perPage = value;
      this.currentPage = 1;
      this.getContracts();
    },
  },
};
</script>

<style>
</style>