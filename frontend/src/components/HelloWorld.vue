<template>
  <div>
    <h1>Fargate-Webapp-Frontend</h1>
    <ul>
      <li v-for="book in books" :key="book.isbn">{{ book.title }} by {{ book.author }}</li>
      <li v-if="error">{{ error }}</li>
    </ul>
    <footer>
      <p>This frontend is loading the list of books from a backend URL hosted in an AWS Fargate private subnet.</p>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: [],
      error: null
    };
  },
  created() {
    const backendUrl = process.env.VUE_APP_BACKEND_URL;
    fetch(`${backendUrl}/api/books`)
      .then(response => response.json())
      .then(data => {
        this.books = data.map(book => ({
          id: book[0],
          isbn: book[1],
          title: book[2],
          author: book[3]
        }));
      })
      .catch(error => {
        console.error('Error:', error);
        this.error = 'Failed to fetch books from the backend';
      });
  }
};
</script>

<style scoped>
footer {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #ccc;
  font-size: 0.9em;
  color: #666;
}
</style>
