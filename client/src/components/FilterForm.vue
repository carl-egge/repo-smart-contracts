<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset" v-if="show">
            <b-container fluid>
                <b-row>
                    <!-- Name -->
                    <b-form-group 
                        id="search-input-name" 
                        label="Contract:" 
                        label-for="input-name"
                        label-size="sm"
                        label-cols="auto"
                        class="col"
                        >
                        <b-form-input
                            id="input-name"
                            v-model="form.name"
                            placeholder="Search for a contract name"
                            class="min-width-50"
                        ></b-form-input>
                    </b-form-group>

                    <!-- Language -->
                    <b-form-group 
                        id="search-input-language"
                        label="Language:"
                        label-for="input-language"
                        label-size="sm"
                        label-cols="auto"
                        class="col"
                    >
                        <b-form-input
                            id="input-language"
                            v-model="form.language"
                            placeholder="Search for a programming language"
                            class="min-width-50"
                        ></b-form-input>
                    </b-form-group>
                    
                    <!-- Sha -->
                    <b-form-group
                        id="search-input-sha"
                        label="Git-Sha:"
                        label-for="input-sha"
                        label-size="sm"
                        label-cols="auto"
                        class="col"
                    >
                        <b-form-input
                            id="input-sha"
                            v-model="form.sha"
                            placeholder="Search for a git sha"
                            class="min-width-50"
                        ></b-form-input>
                    </b-form-group>
                </b-row>

                <b-row>    
                        <!-- License -->
                        <b-form-group 
                            id="search-input-license" 
                            label="License:" 
                            label-for="input-license"
                            label-size="sm"
                            label-cols="auto"
                            class="col"
                        >
                            <b-form-select
                                id="input-license"
                                v-model="form.license"
                                :options="licenses"
                                class="min-width-50"
                            ></b-form-select>
                        </b-form-group>
            
                        <!-- Repo -->
                        <b-form-group 
                            id="search-input-repo" 
                            label="Repository:" 
                            label-for="input-repo"
                            label-size="sm"
                            label-cols="auto"
                            class="col"
                        >
                            <b-form-input
                                id="input-repo"
                                v-model="form.repo"
                                placeholder="Search for a repository"
                                class="min-width-50"
                            ></b-form-input>
                        </b-form-group>
                        
                        <!-- Owner -->
                        <b-form-group 
                            id="search-input-owner" 
                            label="Owner:" 
                            label-for="input-owner"
                            label-size="sm"
                            label-cols="auto"
                            class="col"
                        >
                            <b-form-input
                                id="input-owner"
                                v-model="form.owner"
                                placeholder="Search for a repository owner (github username)"
                                class="min-width-50"
                            ></b-form-input>
                        </b-form-group>
                </b-row>

                <b-row>
                    <!-- AmountOfVersions -->
                    <b-form-group 
                        id="search-input-amountOfVersions" 
                        label="Amount Of Versions:" 
                        label-for="input-amountOfVersions"
                        label-size="sm"
                        label-cols="auto"
                        class="col col-3 col-xxl-1"
                    >
                        <b-form-input
                            id="input-amountOfVersions"
                            type="number"
                            min="0"
                            v-model="form.amountOfVersions"
                        ></b-form-input>
                    </b-form-group>
        
                    <!-- Pragma -->
                    <b-form-group 
                        id="search-input-pragma" 
                        label="Pragma:" 
                        label-for="input-pragma"
                        label-size="sm"
                        label-cols="auto"
                        class="col col-3 col-xxl-auto"
                        >
                        <b-form-input
                            id="input-pragma"
                            v-model="form.pragma"
                            placeholder="Search for a pragma version (e.g. 0.4.24)"
                            class="min-width-50"
                        ></b-form-input>
                    </b-form-group>
        
                    <!-- Size -->
                    <b-form-group 
                        id="search-input-size" 
                        label="Size:" 
                        label-for="input-size"
                        label-size="sm"
                        label-cols="auto"
                        class="col col-3 col-xxl-auto"
                    >
                        <b-form-input
                            id="input-size"
                            v-model="form.size"
                            placeholder="Search for a file size (can be range e.g. 1..1000)"
                            class="min-width-50"
                        ></b-form-input>
                    </b-form-group>
        
                    <!-- SearchAllVersions -->
                    <b-form-group 
                        id="search-input-searchAllVersions" 
                        v-slot="{ ariaDescribedby }"
                        label-size="sm"
                        label-cols="auto"
                        class="col col-3 col-xxl-1"
                    >
                        <b-form-checkbox
                            v-model="form.searchAllVersions"
                            id="input-searchAllVersions"
                            :value="true"
                            :unchecked-value="false"
                            :aria-describedby="ariaDescribedby"
                        >
                            Search all versions (default: search only latest version)
                        </b-form-checkbox>
                    </b-form-group>
                </b-row>
                <b-row align-h="center">
                    <b-col class="text-right">
                        <b-button type="submit" variant="primary" class="btn-filter">Search</b-button>
                    </b-col>
                    <b-col>
                        <b-button type="reset" variant="danger" class="btn-filter">Reset</b-button>
                    </b-col>
                </b-row>
            </b-container>
        </b-form>

        <!-- Form data result for testing -->
        <!-- <b-card class="mt-3" header="Form Data Result">
            <pre class="m-0">{{ form }}</pre>
        </b-card> -->

    </div>
  </template>
  
  <script>
    export default {
        data() {
            return {
                form: {
                    name: '',
                    language: '',
                    sha: '',
                    license: null,
                    repo: '',
                    owner: '',
                    amountOfVersions: null,
                    pragma: '',
                    size: '',
                    searchAllVersions: false
                },
                licenses: [
                    { text: 'GNU Affero General Public License v3.0', value: 'agpl-3.0' },
                    { text: 'Apache License 2.0', value: 'apache-2.0' },
                    { text: 'BSD 2-Clause \"Simplified\" License', value: 'bsd-2-clause' },
                    { text: 'BSD 3-Clause \"New\" or \"Revised\" License', value: 'bsd-3-clause' },
                    { text: 'Boost Software License 1.0', value: 'bsl-1.0' },
                    { text: 'Creative Commons Zero v1.0 Universal', value: 'cc0-1.0' },
                    { text: 'Eclipse Public License 2.0', value: 'epl-2.0' },
                    { text: 'GNU General Public License v2.0', value: 'gpl-2.0' },
                    { text: 'GNU General Public License v3.0', value: 'gpl-3.0' },
                    { text: 'GNU Lesser General Public License v2.1', value: 'lgpl-2.1' },
                    { text: 'MIT License', value: 'mit' },
                    { text: 'Mozilla Public License 2.0', value: 'mpl-2.0' },
                    { text: 'The Unlicense', value: 'unlicense' }
                ],
                show: true,
            }
        },
        methods: {
            onSubmit(event) {
                event.preventDefault()
                let params = this.constructSearchParams();
                this.$emit('search', params);
            },
            onReset(event) {
                event.preventDefault()
                // Reset our form values
                this.form.name = ''
                this.form.language = ''
                this.form.sha = ''
                this.form.license = null
                this.form.repo = ''
                this.form.owner = ''
                this.form.amountOfVersions = null
                this.form.pragma = ''
                this.form.size = ''
                this.form.searchAllVersions = false
                this.$emit('search', {});
                // Trick to reset/clear native browser form validation state
                this.show = false
                this.$nextTick(() => {
                    this.show = true
                })
            },
            constructSearchParams() {
                let params = {};
                if (this.form.name) {
                    params.name = this.form.name;
                }
                if (this.form.language) {
                    params.language = this.form.language;
                }
                if (this.form.sha) {
                    params.sha = this.form.sha;
                }
                if (this.form.license) {
                    params.license = this.form.license;
                }
                if (this.form.repo) {
                    params.repo = this.form.repo;
                }
                if (this.form.owner) {
                    params.owner = this.form.owner;
                }
                if (this.form.amountOfVersions) {
                    params.amountOfVersions = this.form.amountOfVersions;
                }
                if (this.form.pragma) {
                    params.pragma = this.form.pragma;
                }
                if (this.form.size) {
                    params.size = this.form.size;
                }
                if (this.form.searchAllVersions) {
                    params.searchAllVersions = this.form.searchAllVersions;
                }
                return params;
            }
        }
    }
  </script>

<style scoped>
.min-width-50 {
    min-width: 50px;
}

#input-amountOfVersions {
    width: 70px;
}

.btn-filter {
    width: 12vw;
}
</style>