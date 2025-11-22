/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    JAVA_BACKEND_URL: process.env.JAVA_BACKEND_URL || 'http://localhost:8080',
    DATABASE_PATH: process.env.DATABASE_PATH || '../databases/insider_risk.db',
  },
}

module.exports = nextConfig

