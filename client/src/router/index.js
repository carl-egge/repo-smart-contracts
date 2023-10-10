import Vue from 'vue';
import Router from 'vue-router';

import ContractsTable from '@/components/ContractsTable';
import Contract from '@/components/Contract';
import Archive from '@/components/Archive';
import About from '@/components/About';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      alias: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/contracts',
      name: 'Contracts',
      component: ContractsTable
    },
    {
      path: '/contracts/:id',
      name: 'ContractDetails',
      component: Contract
    },
    {
      path: '/flatcontracts',
      name: 'FlatContracts',
      component: ContractsTable
    },
    {
      path: '/flatcontracts/:id',
      name: 'FlatContractDetails',
      component: Contract
    },
    // {
    //   path: '/archive',
    //   name: 'Archive',
    //   component: Archive
    // },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
