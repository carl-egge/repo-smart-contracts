<template>
  <div>
    <b-container fluid>
      <b-row class="mb-3" align-v="center">
        <!-- Filter -->
        <b-col>
          <b-form-group label-for="filter-input">
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
        <template #cell(name)="data">
          <b>{{ data.value }}</b>
          <span class="path-sm">({{ data.item.path }})</span>
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
        <!-- <template #cell(id)="data">
          <router-link :to="'/contracts/' + data.value">
            {{ data.value }}
          </router-link>
        </template> -->

        <!-- Row: Repo -->
        <template #cell(repo.full_name)="data">
          <a :href="'https://github.com/' + data.value" target="_blank">
            {{ data.value }}
          </a> 
          <span class="icon-sm">
            <b-icon-box-arrow-up-right></b-icon-box-arrow-up-right>
          </span>
        </template>

        <!-- Row: Actions (Buttons) -->
        <template #cell(actions)="row">
          <!-- Update Button @click="$router.push('/contracts/' +row.item.id)"-->
          <b-button
            @click="$router.push('/contracts/' + row.item.id)"
            v-b-tooltip.hover :title="'ID: ' + row.item.id"
            variant="primary"
            size="sm"
          >
            <b-icon-three-dots></b-icon-three-dots>
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

      <!-- Pagination -->
      <b-row align-h="center" class="my-1 mb-5">
        
        <!-- Pagination: Set entries per page -->
        <b-col cols="auto">
            <b-form-group label-for="per-page-select">
              <b-input-group size="sm">
                <b-form-select
                  id="per-page-select"
                  v-model="perPage"
                  :options="pageOptions"
                  @change="handlePageSizeChange($event)"
                ></b-form-select>
  
                <b-input-group-append>
                  <b-button :disabled="true"> Per Page </b-button>
                </b-input-group-append>
              </b-input-group>
            </b-form-group>
        </b-col>

        <!-- Pagination: Switch between pages. -->
        <b-col md="5" class="mb-3">
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
        
        <!-- Go to page -->
        <b-col cols="auto">
          <b-form-group label-for="go-to-input">
            <b-input-group size="sm">
              <b-form-input
              id="go-to-input"
                v-model="goTo"
                type="number"
              ></b-form-input>
              
              <b-input-group-append>
                <b-button @click="jumpPage($event)"> Go to page </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
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
          key: "name",
          label: "Contract",
          sortable: true,
          sortDirection: "desc",
        },
        // {
        //   key: "id",
        //   label: "ID",
        //   sortable: true,
        //   class: "text-center",
        // },
        {
          key: "repo.full_name",
          label: "Repository",
          sortable: true,
        },
        {
          key: "language",
          label: "Language",
          sortable: true,
        },
        {
          key: "license",
          label: "License",
          sortable: true,
        },
        {
          key: "versions",
          label: "Quantity Of Versions",
          sortable: true,
          class: "text-center",
        },
        {
          key: "compilerversion",
          label: "Compiler Version",
          sortable: true,
          class: "text-center",
        },
        {
          key: "actions",
          label: "Details",
          class: "text-center py-0 align-middle",
        },
      ],

      // Table Settings
      isBusy: false,
      totalRows: 1,
      totalDBsize: 0,
      currentPage: 1,
      perPage: 25,
      pageOptions: [5, 25, 100, 200],
      sortBy: "",
      sortDesc: true,
      sortDirection: "desc",
      filter: null,
      filterOn: [],
      goTo: null,
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
      this.contracts = response.data.data;
      this.contracts.forEach((element) => {
        if (element.versions.length > 0) {
          element.compilerversion =
            element.versions.slice(-1)[0].compiler_version;
        } else {
          element.compilerversion = "N/A";
        }
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
      //this.totalRows = filteredItems.length;
      //this.currentPage = 1;
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

    /**
     * jumpPage
     *
     * go to specified page
     */
    jumpPage(value) {
      this.currentPage = this.goTo;
      this.getContracts();
    },
  },
};
</script>

<style>
#go-to-input {
  max-width: 70px;
}

#per-page-select {
  max-width: 70px;
}

#filter-input {
  min-width: 100px;
}

.btn-sm {
  padding: 0.2rem 0.35rem;
  font-size: 1.2rem;
  line-height: 1;
}

.page-link {
  color: black;
}

.page-item.active .page-link {
  z-index: 3;
  color: #fff;
  background-color: #6c757d;
  border-color: #6c757d;
}

.pagination a {
  color:chocolate;
}

.icon-sm {
  font-size: 0.65rem;
  vertical-align: 0.45em;
}

.path-sm {
  font-size: 0.8rem;
  color: grey;
  vertical-align: 0.3em;
}
</style>