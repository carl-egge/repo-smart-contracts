<template>
  <div>
    <h3>
      {{ this.title }}
      <span class="fs-6 text-secondary">
        ({{ this.contract.id }})
        <button
          class="btn btn-outline-secondary"
          style="
            --bs-btn-padding-y: 0.2rem;
            --bs-btn-padding-x: 0.3rem;
            --bs-btn-font-size: 0.3rem;
          "
          @click="copyToClipBoard(contract.id)"
        >
          <copy-icon></copy-icon>
        </button>
      </span>
    </h3>
    <div class="mx-2 my-4">
      <div class="container px-0 mx-0">
        <div class="row justify-content-start align-items-center">
          <div class="ml-0 col-2">
            <div class="dropdown">
              <button
                class="btn btn-outline-secondary dropdown-toggle btn-sm"
                type="button"
                id="dropdownMenuButton1"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Version: {{ this.version }}
              </button>
              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                <li v-for="vers in contract.versions" :key="vers.vid">
                  <a class="dropdown-item" @click="changeVersion(vers.vid)"
                    >Version: {{ vers.vid }}</a
                  >
                </li>
              </ul>
            </div>
          </div>
          <div class="col-6">
            <b>Version Timestamp:</b>
            {{ this.timestamp }} (UTC)
          </div>
          <div class="col-4">
            <button
              type="button"
              class="btn btn-outline-secondary btn-sm"
              @click="deleteContractVersion()"
            >
              Delete Version {{ this.version }}
            </button>
          </div>
        </div>
      </div>

      <br />

      <div class="p-2 code-section">
        <!-- Title -->
        <div class="container my-3 mx-0 px-0">
          <div class="row g-3 align-items-center">
            <div class="col-2 mx-2">
              <label for="titleTextInput" class="form-label"
                ><b>Title:</b></label
              >
            </div>
            <div class="col-8">
              <input
                type="text"
                id="titleTextInput"
                class="form-control"
                v-model="title"
                :disabled="disabletitle"
              />
            </div>
            <div class="col-auto">
              <button
                class="btn btn-outline-secondary"
                style="
                  --bs-btn-padding-y: 0.2rem;
                  --bs-btn-padding-x: 0.3rem;
                  --bs-btn-font-size: 0.3rem;
                "
                @click="copyToClipBoard(contract.title)"
              >
                <copy-icon></copy-icon>
              </button>
              <button
                class="btn btn-outline-secondary"
                style="
                  --bs-btn-padding-y: 0.2rem;
                  --bs-btn-padding-x: 0.3rem;
                  --bs-btn-font-size: 0.3rem;
                "
                @click="edit('title')"
              >
                <edit-icon></edit-icon>
              </button>
            </div>
          </div>
        </div>
        <!-- Description -->
        <div class="container my-3 mx-0 px-0">
          <div class="row g-3 align-items-center">
            <div class="col-2 mx-2">
              <label for="descriptionTextInput" class="form-label"
                ><b>Description:</b></label
              >
            </div>
            <div class="col-8">
              <input
                type="text"
                id="descriptionTextInput"
                class="form-control"
                v-model="description"
                :disabled="disabledesc"
              />
            </div>
            <div class="col-auto">
              <button
                class="btn btn-outline-secondary"
                style="
                  --bs-btn-padding-y: 0.2rem;
                  --bs-btn-padding-x: 0.3rem;
                  --bs-btn-font-size: 0.3rem;
                "
                @click="copyToClipBoard(contract.description)"
              >
                <copy-icon></copy-icon>
              </button>
              <button
                class="btn btn-outline-secondary"
                style="
                  --bs-btn-padding-y: 0.2rem;
                  --bs-btn-padding-x: 0.3rem;
                  --bs-btn-font-size: 0.3rem;
                "
                @click="edit('desc')"
              >
                <edit-icon></edit-icon>
              </button>
            </div>
          </div>
        </div>
        <p>
          <b>Sourcecode:</b>
          <span class="fs-6 text-end text-secondary">
            <button
              class="btn btn-outline-secondary"
              style="
                --bs-btn-padding-y: 0.2rem;
                --bs-btn-padding-x: 0.3rem;
                --bs-btn-font-size: 0.3rem;
              "
              @click="copyToClipBoard(sourcecode)"
            >
              <copy-icon></copy-icon>
            </button>
          </span>
        </p>
        <prism-editor
          class="my-editor height-300"
          v-model="sourcecode"
          :highlight="highlighter"
          line-numbers
        ></prism-editor
        ><br />
        <p>
          <b>Bytecode:</b>
          <span class="fs-6 text-end text-secondary">
            <button
              class="btn btn-outline-secondary"
              style="
                --bs-btn-padding-y: 0.2rem;
                --bs-btn-padding-x: 0.3rem;
                --bs-btn-font-size: 0.3rem;
              "
              @click="copyToClipBoard(bytecode)"
            >
              <copy-icon></copy-icon>
            </button>
          </span>
        </p>
        <prism-editor
          class="my-editor height-300"
          v-model="bytecode"
          :highlight="highlighter"
          line-numbers
        ></prism-editor
        ><br />
        <p>
          <b>ABI:</b>
          <span class="fs-6 text-end text-secondary">
            <button
              class="btn btn-outline-secondary"
              style="
                --bs-btn-padding-y: 0.2rem;
                --bs-btn-padding-x: 0.3rem;
                --bs-btn-font-size: 0.3rem;
              "
              @click="copyToClipBoard(abi)"
            >
              <copy-icon></copy-icon>
            </button>
          </span>
        </p>
        <prism-editor
          class="my-editor height-300"
          v-model="abi"
          :highlight="highlighter"
          line-numbers
        ></prism-editor>
        <div class="row mt-4">
          <div class="col my-3">
            <button
              type="button"
              class="btn btn-outline-danger w-100"
              @click="deleteContract()"
            >
              Delete This Contact
            </button>
          </div>
          <div class="col my-3">
            <button
              type="submit"
              class="btn btn-outline-success w-100"
              @click="saveContract()"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ContractsService from "@/services/ContractsService";
import CopyIcon from "@/components/copyIcon";
import EditIcon from "@/components/editIcon";
// import Prism Editor
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css"; // import the styles somewhere

// import highlighting library (you can use any library you want just return html string)
import { highlight, languages } from "prismjs/components/prism-core";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-tomorrow.css"; // import syntax highlighting styles

export default {
  components: {
    PrismEditor,
    CopyIcon,
    EditIcon,
  },
  data() {
    return {
      contract: {},
      version: 1,
      timestamp: "loading ...",
      sourcecode: "loading ...",
      bytecode: "loading ...",
      abi: "loading ...",
      title: "loading ...",
      description: "loading ...",
      disabledesc: true,
      disabletitle: true,
    };
  },
  mounted() {
    this.getContract(this.$route.params.id);
  },
  methods: {
    highlighter(code) {
      return highlight(code, languages.js); // languages.<insert language> to return html with markup
    },
    setCode(vid) {
      this.title = this.contract.title;
      this.description = this.contract.description;
      this.sourcecode = this.contract.versions[vid - 1].content.sourcecode
        ? this.contract.versions[vid - 1].content.sourcecode
        : "null";
      this.bytecode = this.contract.versions[vid - 1].content.bytecode
        ? this.contract.versions[vid - 1].content.bytecode
        : "null";
      this.abi = this.contract.versions[vid - 1].content.abi
        ? this.contract.versions[vid - 1].content.abi
        : "null";
      this.findTimestamp(this.version);
    },
    changeVersion(vid) {
      this.version = vid;
      this.setCode(vid);
    },
    findTimestamp(vid) {
      var tmp = new Date(this.contract.versions[vid - 1].created);
      this.timestamp = tmp.toLocaleDateString("de-DE", {
        hour: "numeric",
        minute: "numeric",
      });
    },
    edit(prop) {
      if (prop == "desc") {
        const temp = this.disabledesc;
        this.disabledesc = !temp;
      }
      if (prop == "title") {
        const temp = this.disabletitle;
        this.disabletitle = !temp;
      } else {
        return;
      }
    },
    async getContract(iden) {
      const response = await ContractsService.get(iden);
      this.contract = response.data;
      this.version = this.contract.latestVersion;
      this.setCode(this.version);
    },
    async saveContract() {
      const data = {
        title: this.title,
        description: this.description,
        sourcecode: this.sourcecode,
        bytecode: this.bytecode,
        abi: this.abi,
      };
      const response = await ContractsService.update(this.contract.id, data);
      this.getContract(this.$route.params.id);
    },
    async deleteContract() {
      await ContractsService.delete(this.contract.id);
      this.$router.push("/");
    },
    async deleteContractVersion() {
      if (this.contract.versions.length == 1) return this.deleteContract();
      await ContractsService.deleteVers(this.contract.id, this.version);
      this.getContract(this.contract.id);
    },
    async copyToClipBoard(textToCopy) {
      await navigator.clipboard.writeText(textToCopy);
    },
  },
};
</script>


<style scoped>
.height-300 {
  height: 300px;
}
.my-editor {
  /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
  background: #2d2d2d;
  color: #ccc;

  /* you must provide font-family font-size line-height. Example: */
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
  border-radius: 4px;
}

.code-section {
  border-radius: 4px;
  border: 1.5px solid #ccc;
}
</style>