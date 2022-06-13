<template>
  <div>
    <h2>Contracts List</h2>
    <div v-for="item in contracts" :key="item.id">
      <p>
        <span>
          <b>{{ item.title }}</b>
        </span>
        <br />
        <span>Description: {{ item.description }}</span>
        <br />
        <span>ID: {{ item.id }}</span>
      </p>
    </div>
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