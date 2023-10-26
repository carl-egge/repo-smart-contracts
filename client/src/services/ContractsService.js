import Api from '@/services/Api'

export default {
  getAll(params) {
    return Api().get('contracts/', { params })
  },
  get(id) {
    return Api().get(`contracts/${id}`);
  },
}
