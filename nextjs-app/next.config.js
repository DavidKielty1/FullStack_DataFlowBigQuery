/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    JAVA_BACKEND_URL: process.env.JAVA_BACKEND_URL || 'http://localhost:8080',
    // DATABASE_PATH is server-side only, don't expose via env config
  },
}

module.exports = nextConfig

