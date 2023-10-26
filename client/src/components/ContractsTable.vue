<template>
  <div>
    <b-container fluid>
      <b-row class="mb-3" align-v="center">
        <!-- Filter -->
        <b-col>
          <b-button id="filter-button" :class="filterVisible ? null : 'collapsed'"
            :aria-expanded="filterVisible ? 'true' : 'false'" aria-controls="collapse-filter"
            @click="filterVisible = !filterVisible" variant="link"
            class="text-dark font-weight-bold text-decoration-none">
            <b-icon-caret-down-fill v-if="!filterVisible"></b-icon-caret-down-fill>
            <b-icon-caret-up-fill v-else></b-icon-caret-up-fill>
            Filter
          </b-button>
          <b-collapse id="collapse-filter" v-model="filterVisible" class="mt-2">
            <b-card bg-variant="light" class="mb-2">
              <FilterForm @search="updateSearchParams($event)" />
            </b-card>
          </b-collapse>
        </b-col>
        <!-- <b-col>
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
        </b-col> -->
      </b-row>

      <!-- Main table element -->
      <b-table :items="contracts" :fields="fields" :filter="filter" :filter-included-fields="filterOn"
        :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" :sort-direction="sortDirection" :busy="isBusy" stacked="md"
        hover show-empty head-variant="light">
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
          <b-button @click="jumpDetailsPage(row.item.id)" v-b-tooltip.hover :title="'ID: ' + row.item.id"
            variant="primary" size="sm">
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
              <b-form-select id="per-page-select" v-model="perPage" :options="pageOptions"
                @change="handlePageSizeChange($event)"></b-form-select>

              <b-input-group-append>
                <b-button :disabled="true"> Per Page </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
        </b-col>

        <!-- Pagination: Switch between pages. -->
        <b-col md="5" class="mb-3">
          <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" align="fill" size="sm"
            class="my-0" @change="handlePageChange($event)"></b-pagination>
        </b-col>

        <!-- Go to page -->
        <b-col cols="auto">
          <b-form-group label-for="go-to-input">
            <b-input-group size="sm">
              <b-form-input id="go-to-input" v-model="goTo" min="0" type="number"></b-form-input>

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
import FlatContractsService from "@/services/FlatContractsService";
import FilterForm from "@/components/FilterForm";

export default {
  name: "contracts",
  components: {
    FilterForm,
  },
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

      filterVisible: false,
      searchParams: {},

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
    this.$watch(() => this.$route.path, (to, from) => {
      // console.log('route path has changed from ' + from + ' to ' + to)
      this.getContracts();
    })
  },
  methods: {
    /**
     * getContracts
     *
     * API call to get the list of contracts
     */
    async getContracts() {
      this.isBusy = true;
      const paginationParams = this.getPaginationParams(
        this.currentPage,
        this.perPage
      );
      const params = {
        ...paginationParams,
        ...this.searchParams,
      };
      // Get route name
      const routeName = this.$route.name;
      let response = {}
      if (routeName == "Contracts") {
        response = await ContractsService.getAll(params);
      } else if (routeName == "FlatContracts") {
        response = await FlatContractsService.getAll(params);
      } else {
        console.log("Error detecting route")
      }
      // this.totalRows = parseInt(response.headers["x-total-db-size"]);
      this.totalRows = parseInt(response.data.totalCount);
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
     * jumpDetailsPage
     * 
     * router push to Contract Details Page depending on the route name
     */
    jumpDetailsPage(item_id) {
      const routeName = this.$route.name;
      if (routeName == "Contracts") {
        this.$router.push("/contracts/" + item_id);
      } else if (routeName == "FlatContracts") {
        this.$router.push("/flatcontracts/" + item_id);
      } else {
        console.log("Error detecting route")
      }
    },

    /**
     * updateSearchParams
     * 
     * update search params
     */
    updateSearchParams(params) {
      this.searchParams = params;
      this.getContracts();
    },

    /**
     * getPaginationParams
     *
     * calculate params for getContracts
     */
    getPaginationParams(page, pageSize) {
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

#filter-button {
  font-size: large;
  padding-top: 0px;
  padding-bottom: 0px;
}

#filter-button:focus {
  box-shadow: none;
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
  color: chocolate;
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