<template>
  <div @dragover.prevent @drop="handleDrop" @dragenter="handleDragEnter" @dragleave="handleDragLeave">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">
        <img src="../assets/pizza_logo.png" alt="logo" width="250">
      </div>
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

      <div v-if="!invoiceReady" class="upload-area">
        <p class="upload-title">Select sales contract</p>
        <button @click="triggerFileInput" class="upload-button">Select File</button>
        <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none" />
        <p class="file-status">{{ fileName || 'or drop FILE here' }}</p>
      </div>

      <div v-if="fileName && !invoiceReady" class="convert-area">
        <button @click="convertContract" :disabled="isLoading" class="convert-button">
          {{ isLoading ? 'Converting...' : 'Convert to Invoice' }}
        </button>

        <div v-if="isLoading">
          <div class="pizza-body">
            <div class='pizza'>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
              <div class='slice'></div>
            </div>
        </div>
      </div>
    </div>
      
      <div v-if="invoiceReady">
        <div class="download-area">
          <!-- <p class="success-message">Invoice is ready!</p> -->
          <a :href="invoiceLink" class="download-button" download>Download Invoice</a>
        </div>
        <button @click="newInvoice" class="new-invoice-button">New Invoice</button>
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
      invoiceReady: false,
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
        this.invoiceReady = true;
      } catch (error) {
        console.error('Error converting contract:', error);
      } finally {
        this.isLoading = false;
      }
    },
    newInvoice() {
      this.fileName = null;
      this.file = null;
      this.invoiceLink = null;
      this.invoiceReady = false;
    },
  },
};
</script>

<style scoped>
/* General Layout */
body {
  font-family: Arial, sans-serif;
  background-color: #ad0a0a;
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
  cursor: pointer;
}

.download-button:hover {
  background-color: #0069d9;
}

.new-invoice-button {
  background-color: #4CAF50;
  color: white; 
  padding: 12px 20px;
  border: none; 
  border-radius: 5px; 
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease;
  margin-top: 20px;
  display: block;
  width: 200px;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.new-invoice-button:hover {
  background-color: #45a049;
}

.new-invoice-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.5);
}

/* ------ */
.pizza-body {
  height: 25vh;
  align-items: center;
  display: flex;
  justify-content: center;
  margin: 0;
  overflow: hidden;
}

.pizza-body:before {
  content: "";
  position: absolute;
  top: 70%;
  left: 50%;
  transform: translateX(-50%) translateY(-50%);
  width: 15vmin;
  height: 2vmin;
  background: #8f242c;
  margin-top: 17.5vmin;
  filter: blur(10px);
  border-radius: 100%;
}
.pizza-body p {
  position: absolute;
  bottom: 10px;
  right: 10px;
  color: #fff;
  font-size: 10px;
}
.pizza-body .pizza {
  height: 20vmin;
  width: 20vmin;
  align-items: center;
  background: none;
  position: relative;
  -webkit-animation: rotate 13s linear infinite;
          animation: rotate 13s linear infinite;
}
@-webkit-keyframes rotate {
  to {
    transform: rotate(360deg);
  }
}
@keyframes rotate {
  to {
    transform: rotate(360deg);
  }
}
.pizza-body .pizza .slice {
  z-index: -1;
  overflow: visible;
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 10vmin 2.75vmin 0 2.75vmin;
  border-color: #ffdc73 transparent transparent transparent;
  left: 7.5vmin;
  top: 0;
  transform-origin: 50% 100%;
  transform: rotate(0deg);
  -webkit-animation: loading 1.8125s ease-in-out infinite;
          animation: loading 1.8125s ease-in-out infinite;
}
@-webkit-keyframes loading {
  0% {
    opacity: 1;
  }
  49% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  99% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@keyframes loading {
  0% {
    opacity: 1;
  }
  49% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  99% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
.pizza-body .pizza .slice:nth-of-type(2n):after {
  box-shadow: 0.5vmin 2.5vmin 0 #cc333f;
}
.pizza-body .pizza .slice:nth-of-type(4n):after {
  box-shadow: 0.5vmin 2.5vmin 0 #cc333f, 1.5vmin 5vmin 0 #cc333f;
}
.pizza-body .pizza .slice:nth-of-type(1) {
  transform: rotate(-27.75deg);
  -webkit-animation-delay: -0.0625s;
          animation-delay: -0.0625s;
}
.pizza-body .pizza .slice:nth-of-type(2) {
  transform: rotate(-55.5deg);
  -webkit-animation-delay: -0.125s;
          animation-delay: -0.125s;
}
.pizza-body .pizza .slice:nth-of-type(3) {
  transform: rotate(-83.25deg);
  -webkit-animation-delay: -0.1875s;
          animation-delay: -0.1875s;
}
.pizza-body .pizza .slice:nth-of-type(4) {
  transform: rotate(-111deg);
  -webkit-animation-delay: -0.25s;
          animation-delay: -0.25s;
}
.pizza-body .pizza .slice:nth-of-type(5) {
  transform: rotate(-138.75deg);
  -webkit-animation-delay: -0.3125s;
          animation-delay: -0.3125s;
}
.pizza-body .pizza .slice:nth-of-type(6) {
  transform: rotate(-166.5deg);
  -webkit-animation-delay: -0.375s;
          animation-delay: -0.375s;
}
.pizza-body .pizza .slice:nth-of-type(7) {
  transform: rotate(-194.25deg);
  -webkit-animation-delay: -0.4375s;
          animation-delay: -0.4375s;
}
.pizza-body .pizza .slice:nth-of-type(8) {
  transform: rotate(-222deg);
  -webkit-animation-delay: -0.5s;
          animation-delay: -0.5s;
}
.pizza-body .pizza .slice:nth-of-type(9) {
  transform: rotate(-249.75deg);
  -webkit-animation-delay: -0.5625s;
          animation-delay: -0.5625s;
}
.pizza-body .pizza .slice:nth-of-type(10) {
  transform: rotate(-277.5deg);
  -webkit-animation-delay: -0.625s;
          animation-delay: -0.625s;
}
.pizza-body .pizza .slice:nth-of-type(11) {
  transform: rotate(-305.25deg);
  -webkit-animation-delay: -0.6875s;
          animation-delay: -0.6875s;
}
.pizza-body .pizza .slice:nth-of-type(12) {
  transform: rotate(-333deg);
  -webkit-animation-delay: -0.75s;
          animation-delay: -0.75s;
}
.pizza-body .pizza .slice:before {
  content: "";
  position: absolute;
  height: 1.5vmin;
  width: 6vmin;
  background: #bbb083;
  top: -10.5vmin;
  left: -3vmin;
  border-radius: 100vmin 100vmin 0.5vmin 0.5vmin/50vmin 50vmin;
}
.pizza-body .pizza .slice:after {
  content: "";
  border-radius: 100%;
  position: absolute;
  width: 1.25vmin;
  height: 1.25vmin;
  background: #cc333f;
  left: -1vmin;
  top: -7vmin;
  z-index: 2;
}
</style>
