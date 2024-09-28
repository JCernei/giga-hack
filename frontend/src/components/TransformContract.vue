<template>
  <div @dragover.prevent @drop="handleDrop" @dragenter="handleDragEnter" @dragleave="handleDragLeave">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">iLoveContracts</div>
      <ul class="nav-links">
        <li><a href="#">All Tools</a></li>
        <li><a href="#">Login</a></li>
        <li><a href="#">Sign up</a></li>
      </ul>
    </nav>

    <!-- Page Content -->
    <div class="content">
      <div class="header">
        <h1>Transform Sales Contracts into Invoices</h1>
        <p>Effortlessly convert your sales contracts into accurate invoices.</p>
      </div>

      <div class="upload-area">
        <p class="upload-title">Select sales contract</p>
        <button @click="triggerFileInput" class="upload-button">Select File</button>
        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />
        <p class="file-status">{{ fileName || 'or drop FILE here' }}</p>
      </div>

      <div v-if="fileName" class="convert-area">
        <button @click="convertContract" :disabled="isLoading" class="convert-button">
          {{ isLoading ? 'Converting...' : 'Convert to Invoice' }}
        </button>
      </div>

      <div v-if="invoiceLink" class="download-area">
        <p class="success-message">Invoice is ready!</p>
        <a :href="invoiceLink" class="download-button" download>Download Invoice</a>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      fileName: null,
      file: null,
      invoiceLink: null,
      isLoading: false,
      dragActive: false,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.fileName = file.name;
        this.file = file;
      } else {
        this.fileName = 'No file chosen';
        this.file = null;
      }
    },
    handleDrop(event) {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      if (file) {
        this.fileName = file.name;
        this.file = file;
      }
      this.dragActive = false;
    },
    handleDragEnter() {
      this.dragActive = true;
    },
    handleDragLeave() {
      this.dragActive = false;
    },
    async convertContract() {
      if (!this.file) return;

      this.isLoading = true;
      const formData = new FormData();
      formData.append('contract', this.file);

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/convert-contract', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.invoiceLink = `http://127.0.0.1:5000${response.data.invoiceUrl}`;
      } catch (error) {
        console.error('Error converting contract:', error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>


<style scoped>
/* General Layout */
body {
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.drag-active {
  background-color: #f0f8ff;
  border: 2px dashed #007bff;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 50px;
  background-color: #f1f1f1;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #ff5757;
}

.nav-links {
  display: flex;
  list-style: none;
}

.nav-links li {
  margin-left: 30px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 16px;
}

/* Content Area */
.content {
  text-align: center;
  margin-top: 80px;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 38px;
  font-weight: bold;
  color: #333;
}

.header p {
  color: #666;
  font-size: 18px;
  margin-bottom: 30px;
}

/* Upload Area */
.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
}

.upload-button {
  background-color: #e5322d;
  color: white;
  padding: 20px 50px;
  border: none;
  border-radius: 10px;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #bd060a;
}

.file-status {
  margin-top: 10px;
  color: #888;
}

/* Convert Button */
.convert-area {
  margin-top: 30px;
}

.convert-button {
  background-color: #e5322d;
  color: white;
  padding: 20px 50px;
  border: none;
  border-radius: 10px;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.convert-button:hover {
  background-color: #bd060a;
}

.convert-button[disabled] {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Success Message */
.success-message {
  color: #28a745;
  font-size: 18px;
  margin-top: 20px;
}

/* Download Button */
.download-button {
  background-color: #007bff;
  color: white;
  padding: 20px 50px;
  border: none;
  border-radius: 10px;
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
  display: inline-block;
  margin-top: 15px;
}

.download-button:hover {
  background-color: #0069d9;
}

</style>
