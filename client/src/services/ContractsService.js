import Api from '@/services/Api'

export default {
  getAll(params) {
    return Api().get('api/contracts', { params })
  },
  get(id) {
    return Api().get(`api/contracts/${id}`);
  },
  create(data) {
    return Api().post('api/contracts', data);
  },
  update(id, data) {
    return Api().put(`api/contracts/${id}`, data);
  },
  delete(id) {
    return Api().delete(`api/contracts/${id}`);
  },
  deleteVers(id, vers) {
    return Api().delete(`api/contracts/${id}?vers=${vers}`);
  },
}
