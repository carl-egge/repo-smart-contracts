import Vue from 'vue'
import Router from 'vue-router'

import ContractsTable from '@/components/ContractsTable'
import Contract from '@/components/Contract'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      alias: '/contracts',
      name: 'Contracts',
      component: ContractsTable
    },
    {
      path: '/contracts/:id',
      name: 'ContractDetails',
      component: Contract
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
