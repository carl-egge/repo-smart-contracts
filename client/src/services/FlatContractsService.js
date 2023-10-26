import Api from '@/services/Api'

export default {
  getAll(params) {
    return Api().get('flatcontracts/', { params })
  },
  get(id) {
    return Api().get(`flatcontracts/${id}`);
  },
}
