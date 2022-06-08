import Vue from 'vue'
import Router from 'vue-router'
//import HelloWorld from '@/components/HelloWorld'
import ContractsList from '@/components/ContractsList'
import Contract from '@/components/Contract'
import AddContract from '@/components/AddContract'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      alias: '/contracts',
      name: 'Contracts',
      component: ContractsList
    },
    {
      path: '/contracts/:id',
      name: 'ContractDetails',
      component: Contract
    },
    {
      path: '/add',
      name: 'AddContract',
      component: AddContract
    }
  ]
})
