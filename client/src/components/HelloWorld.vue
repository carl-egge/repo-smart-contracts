<template>
  <div class="posts">
    <h1>Posts</h1>
    This file will list all the posts!

    <div v-for="post in posts" :key="post.id">
      <p>
        <span
          ><b>{{ post.title }}</b></span
        ><br />
        <span>Sourcecode: {{ post.sourcecode }}</span>
        <span>Version: {{ post.version }}</span>
      </p>
    </div>
  </div>
</template>

<script>
import PostsService from "@/services/PostsService";
export default {
  name: "posts",
  data() {
    return {
      posts: [],
    };
  },
  mounted() {
    this.getPosts();
  },
  methods: {
    async getPosts() {
      const response = await PostsService.fetchPosts();
      //alert(JSON.stringify(response));
      this.posts = response.data;
    },
  },
};
</script>
