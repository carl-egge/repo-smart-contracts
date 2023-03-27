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
      alias: '/contracts',
      name: 'Contracts',
      component: ContractsTable
    },
    {
      path: '/contracts/:id',
      name: 'ContractDetails',
      component: Contract
    },
    // {
    //   path: '/archive',
    //   name: 'Archive',
    //   component: Archive
    // },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
