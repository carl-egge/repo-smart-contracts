<template>
  <div>
    <h2>Contracts List</h2>
    <b-container fluid>
      <b-row
        v-for="item in contracts"
        :key="item.id"
        style="border-bottom: 1px solid #bbb"
      >
        <b-col cols="3">
          <strong>{{ item.title }}</strong>
        </b-col>
        <b-col cols="auto">
          (<router-link :to="'/contracts/' + item.id">{{ item.id }}</router-link
          >)
        </b-col>
        <b-col> Description: {{ item.description }} </b-col>
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
    };
  },
  mounted() {
    this.getContracts();
  },
  methods: {
    async getContracts() {
      const response = await ContractsService.getAll();
      this.contracts = response.data;
    },
  },
};
</script>

<style>
</style>