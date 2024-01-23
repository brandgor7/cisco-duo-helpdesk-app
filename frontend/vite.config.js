import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173, // set the port to match the one exposed in your Dockerfile
    hmr: {
      // Necessary for hot module replacement in a Docker environment
      clientPort: 5173,
      host: '0.0.0.0',
    },
  },
});
